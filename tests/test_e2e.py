import pytest
import subprocess
import time
import socket
import sys
import pickle
from pathlib import Path

src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path.resolve()))

from config import HOST, PORT, MAX_CLIENTS
from models import User


def force_free_port(port):
    """
    Forcefully kills any process listening on the given port (works on macOS/Linux).
    Ensures the port is completely freed from any stuck/zombie server processes.
    """
    try:
        output = subprocess.check_output(["lsof", "-t", "-i", f":{port}"])
        pids = output.decode('utf-8').strip().split('\n')
        for pid in pids:
            if pid:
                subprocess.run(["kill", "-9", pid], check=False)
                print(f"\n[Test Setup] Killed ghost process (PID: {pid}) blocking port {port}")
        time.sleep(1)
    except subprocess.CalledProcessError:
        pass


def is_port_open(host, port, timeout=1.0):
    """Utility function to check if a network port is open and listening."""
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except (socket.timeout, ConnectionRefusedError):
        return False


@pytest.fixture(scope="module")
def running_server():
    """
    Fixture to start the background server, clear the port beforehand,
    and log its output to a file.
    """
    # Ensure the port is free before starting the server to avoid 'Address already in use' errors.
    force_free_port(PORT)

    server_script = src_path / "server.py"
    log_file_path = Path(__file__).parent / "server_e2e.log"

    # Start the server as a separate process and redirect its stdout/stderr to a log file.
    # This allows us to debug server issues if the E2E tests fail.
    with open(log_file_path, "w") as log_file:
        process = subprocess.Popen(
            [sys.executable, str(server_script)],
            stdout=log_file,
            stderr=subprocess.STDOUT
        )

        # Actively poll the server port instead of using a hardcoded sleep.
        # This makes the tests faster and more reliable.
        start_time = time.time()
        while not is_port_open(HOST, PORT):
            if time.time() - start_time > 5:
                pytest.fail("Server did not start within 5 seconds.")
            time.sleep(0.1)

        yield process

        # Ensure the server process is terminated after all tests in the module finish.
        process.terminate()
        process.wait()


class TestEndToEnd:
    """End-to-End tests simulating real client-server interactions over the network."""

    def test_e2e_successful_connection_and_request(self, running_server):
        """Checks the happy path: client connects, gets OK, and receives data."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5.0)
            
            # Simulate the initial handshake.
            s.connect((HOST, PORT))
            s.sendall(b"1111")
            status = s.recv(1024).decode('utf-8')
            
            # Simulate requesting a specific class of objects.
            s.sendall(b"User")
            data = s.recv(65536)
            
            assert status == "OK", f"Expected OK, but got {status}"
            assert data is not None
            assert len(data) > 0
            
            # Deserialize the received byte stream and verify the object structure.
            # This confirms that the entire serialization/deserialization pipeline works over the network.
            collection = pickle.loads(data)
            assert isinstance(collection, list)
            assert len(collection) > 0
            assert all(isinstance(item, User) for item in collection)

    def test_e2e_max_clients_limit(self, running_server):
        """Verifies that the server rejects clients exceeding the MAX_CLIENTS limit."""
        active_sockets = []

        try:
            # Exhaust the server's connection pool by connecting up to MAX_CLIENTS.
            for i in range(MAX_CLIENTS):
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(5.0)
                s.connect((HOST, PORT))
                s.sendall(f"200{i}".encode('utf-8'))

                status = s.recv(1024).decode('utf-8')
                assert status == "OK", f"Expected OK, got {status} for client {i}"
                active_sockets.append(s)

            # Attempt to connect one more client beyond the limit.
            s_refused = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s_refused.settimeout(5.0)
            s_refused.connect((HOST, PORT))
            s_refused.sendall(b"9999")

            status_refused = s_refused.recv(1024).decode('utf-8')
            
            # Verify the server correctly refuses the connection.
            assert status_refused == "REFUSED", f"Expected REFUSED, got {status_refused}"

            s_refused.close()

        finally:
            # Clean up all active sockets to avoid resource leaks.
            for s in active_sockets:
                s.close()
