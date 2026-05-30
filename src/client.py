import socket
import pickle
import random
import time
import sys
from config import HOST, PORT
from models import *


def process_stream(collection, expected_class_name, client_id):
    """
    Simulates stream processing using generators (Python's equivalent to Java's Stream API).
    """

    def cast_object(obj):
        actual_class = type(obj).__name__
        if actual_class != expected_class_name:
            raise TypeError(f"Casting error! Expected class '{expected_class_name}', but got '{actual_class}'.")
        return obj

    stream = (cast_object(obj) for obj in collection)

    print(f"\n[Client {client_id}] --- Stream processing for class: {expected_class_name} ---")

    for _ in range(len(collection)):
        try:
            item = next(stream)
            print(f"[Client {client_id}] Successfully processed: {item}")
        except TypeError as e:
            print(f"[Client {client_id}] EXCEPTION CAUGHT: {e}")
        except StopIteration:
            break


def run_client():
    client_id = random.randint(1000, 9999)
    print(f"[Client {client_id}] Starting the client application...")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            client_socket.connect((HOST, PORT))
        except ConnectionRefusedError:
            print(f"[Client {client_id}] ERROR: The server is not responding. Make sure the server is running.")
            sys.exit(1)

        client_socket.sendall(str(client_id).encode('utf-8'))

        status = client_socket.recv(1024).decode('utf-8')
        print(f"[Client {client_id}] Received connection status: {status}")

        if status == "REFUSED":
            print(f"[Client {client_id}] The server refused the connection (MAX_CLIENTS exceeded). Terminating.")
            sys.exit(0)

        elif status == "OK":
            class_requests = ["User", "Product", "Order", "WrongClass"]

            for class_name in class_requests:
                time.sleep(1)
                print(f"\n[Client {client_id}] --> Requesting a collection of objects of class: {class_name}")
                client_socket.sendall(class_name.encode('utf-8'))

                data = client_socket.recv(4096)

                if not data:
                    print(f"[Client {client_id}] The server terminated the connection unexpectedly.")
                    break

                try:
                    collection = pickle.loads(data)
                except Exception as e:
                    print(f"[Client {client_id}] Error during deserialization: {e}")
                    continue

                process_stream(collection, class_name, client_id)

    print(f"\n[Client {client_id}] All requests completed. The application is terminating.")


if __name__ == "__main__":
    run_client()
