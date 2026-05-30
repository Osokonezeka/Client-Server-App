import pytest
import sys
import pickle
from pathlib import Path
from unittest.mock import MagicMock, patch

src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path.resolve()))

import server
from models import User, Product, Order


@pytest.fixture(autouse=True)
def setup_server_data():
    """
    Fixture that runs before each test.
    Resets the object map and active clients counter to ensure test independence.
    """
    server.object_map.clear()
    server.initialize_data()
    server.active_clients = 0


class TestServerIntegration:
    """Integration tests focusing on data transmission and socket mocking."""

    def test_handle_client_successful_transmission(self):
        """
        Simulates a valid client request. Verifies if the server correctly
        serialized the objects (pickle) and sent them through the mocked socket.
        """
        mock_conn = MagicMock()
        mock_conn.recv.side_effect = [b"1111", b"Product", b""]

        server.handle_client(mock_conn, ('127.0.0.1', 55555))

        mock_conn.sendall.assert_any_call(b"OK")

        sendall_calls = mock_conn.sendall.call_args_list
        assert len(sendall_calls) >= 2
        pickled_data = sendall_calls[1][0][0]

        received_objects = pickle.loads(pickled_data)
        assert len(received_objects) == 4
        assert all(isinstance(obj, Product) for obj in received_objects)
        assert received_objects[0].name == "Product_Name_1"

    def test_handle_client_intentional_error_transmission(self):
        """
        Verifies the intentional error mechanism. If the client requests a
        non-existent class, the server should deliberately send a User object.
        """
        mock_conn = MagicMock()
        mock_conn.recv.side_effect = [b"2222", b"WrongClass", b""]

        server.handle_client(mock_conn, ('127.0.0.1', 55556))

        sendall_calls = mock_conn.sendall.call_args_list
        pickled_data = sendall_calls[1][0][0]

        received_objects = pickle.loads(pickled_data)
        assert len(received_objects) == 1
        assert isinstance(received_objects[0], User)
        assert received_objects[0].username == "Error_Trigger_User"

    @patch('server.MAX_CLIENTS', 0)
    def test_handle_client_refused_connection(self):
        """
        Verifies the integration of the client limit logic. We mock the MAX_CLIENTS
        variable to 0, which should result in an immediate connection refusal.
        """
        mock_conn = MagicMock()
        mock_conn.recv.return_value = b"3333"

        server.handle_client(mock_conn, ('127.0.0.1', 55557))

        mock_conn.sendall.assert_called_once_with(b"REFUSED")
