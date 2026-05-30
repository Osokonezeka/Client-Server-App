import socket
import pickle
import random
import time
import sys
import logging
from config import HOST, PORT

logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'
)


def process_stream(collection, expected_class_name, client_id):
    """
    Simulates stream processing using generators (Python's equivalent to Java's Stream API).
    """
    def cast_object(obj):
        # Verify the object's class matches the expected class.
        # This simulates strict type casting. If the types don't match, we deliberately
        # raise a TypeError to handle it further down the stream.
        actual_class = type(obj).__name__
        if actual_class != expected_class_name:
            raise TypeError(f"Casting error! Expected class '{expected_class_name}', but got '{actual_class}'.")
        return obj

    # Use a generator expression to create a lazy stream.
    # Unlike list comprehensions, this evaluates elements one-by-one only when requested.
    stream = (cast_object(obj) for obj in collection)

    logging.info(f"\n[Client {client_id}] --- Stream processing for class: {expected_class_name} ---")

    for _ in range(len(collection)):
        try:
            # Fetch the next item from the stream.
            # The actual evaluation (and potential casting error) happens here.
            item = next(stream)
            logging.info(f"[Client {client_id}] Successfully processed: {item}")
        except TypeError as e:
            # Gracefully catch the casting error raised by cast_object.
            # This demonstrates handling exceptions during stream processing.
            logging.warning(f"[Client {client_id}] EXCEPTION CAUGHT: {e}")
        except StopIteration:
            # Reached the end of the generator stream.
            break


def run_client():
    client_id = random.randint(1000, 9999)
    logging.info(f"[Client {client_id}] Starting the client application...")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            client_socket.connect((HOST, PORT))
        except ConnectionRefusedError:
            logging.error(f"[Client {client_id}] ERROR: The server is not responding. Make sure the server is running.")
            sys.exit(1)

        # Send the initial handshake containing the client ID.
        client_socket.sendall(str(client_id).encode('utf-8'))

        # Wait for the server's connection decision.
        status = client_socket.recv(1024).decode('utf-8')
        logging.info(f"[Client {client_id}] Received connection status: {status}")

        if status == "REFUSED":
            # Handle server refusal (e.g., MAX_CLIENTS reached).
            logging.warning(f"[Client {client_id}] The server refused the connection (MAX_CLIENTS exceeded). Terminating.")
            sys.exit(0)

        elif status == "OK":
            # List of classes to request. 'WrongClass' is intentionally included
            # to trigger a server-side deliberate error mechanism.
            class_requests = ["User", "Product", "Order", "WrongClass"]

            for class_name in class_requests:
                time.sleep(1)
                logging.info(f"\n[Client {client_id}] --> Requesting a collection of objects of class: {class_name}")
                client_socket.sendall(class_name.encode('utf-8'))

                # Receive the serialized collection.
                # A buffer size of 65536 is used to ensure we receive the complete pickled object.
                data = client_socket.recv(65536)
                
                if not data:
                    logging.warning(f"[Client {client_id}] The server terminated the connection unexpectedly.")
                    break

                try:
                    # Deserialize the byte stream back into Python objects.
                    # This relies on the 'models.py' definitions being available in the environment.
                    collection = pickle.loads(data)
                except Exception as e:
                    logging.error(f"[Client {client_id}] Error during deserialization: {e}")
                    continue

                # Pass the deserialized collection to the streaming logic.
                process_stream(collection, class_name, client_id)

    logging.info(f"\n[Client {client_id}] All requests completed. The application is terminating.")


if __name__ == "__main__":
    run_client()