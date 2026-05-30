import socket
import threading
import pickle
import time
import random
import logging
from config import HOST, PORT, MAX_CLIENTS
from models import User, Product, Order

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] (%(threadName)-10s) %(message)s',
    datefmt='%H:%M:%S'
)

object_map = {}
active_clients = 0
clients_lock = threading.Lock()


def initialize_data():
    """
    Creates 4 objects of each class and stores them in a map (dictionary).
    The key format is 'ClassName_Number' as requested in the project rules.
    """
    logging.info("Initializing data map...")
    for i in range(1, 5):
        object_map[f"User_{i}"] = User(i, f"Username_{i}")
        object_map[f"Product_{i}"] = Product(100 + i, f"Product_Name_{i}", i * 15.50)
        object_map[f"Order_{i}"] = Order(1000 + i, f"Item_Name_{i}", i * 2)

    for key, val in object_map.items():
        logging.info(f"  -> Created: {key}: {val}")


def handle_client(conn: socket.socket, addr):
    """
    Handles a single client connection in a dedicated thread.
    """
    global active_clients
    client_id = "UNKNOWN"
    accepted = False

    try:
        data = conn.recv(1024)
        if not data:
            return
        client_id = data.decode('utf-8')

        with clients_lock:
            if active_clients >= MAX_CLIENTS:
                logging.warning(f"Connection from Client {client_id} REFUSED (MAX_CLIENTS={MAX_CLIENTS} reached).")
                conn.sendall("REFUSED".encode('utf-8'))
                return
            else:
                active_clients += 1
                accepted = True
                logging.info(f"Connection from Client {client_id} ACCEPTED. Active clients: {active_clients}")
                conn.sendall("OK".encode('utf-8'))

        while True:
            data = conn.recv(1024)
            if not data:
                break

            requested_class = data.decode('utf-8')
            logging.info(f"Client {client_id} requested class: {requested_class}")

            time.sleep(random.uniform(0.5, 1.5))

            collection_to_send = [
                obj for key, obj in object_map.items() if key.startswith(f"{requested_class}_")
            ]

            if not collection_to_send:
                logging.warning(f"Class '{requested_class}' not found. Sending a deliberate error object.")
                collection_to_send = [User(999, "Error_Trigger_User")]

            serialized_data = pickle.dumps(collection_to_send)
            conn.sendall(serialized_data)
            logging.info(f"Sent collection of {len(collection_to_send)} objects to Client {client_id}.")

    except ConnectionResetError:
        logging.warning(f"Client {client_id} forcibly closed the connection.")
    except Exception as e:
        logging.error(f"Unexpected error while handling Client {client_id}: {e}", exc_info=True)

    finally:
        if accepted:
            with clients_lock:
                active_clients -= 1
            logging.info(f"Client {client_id} disconnected. Active clients: {active_clients}")
        conn.close()


def run_server():
    """
    Main server loop that initializes data and accepts incoming connections.
    """
    initialize_data()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen()

        logging.info(f"Server listening for connections on {HOST}:{PORT}...")
        logging.info(f"MAX_CLIENTS limit is currently set to: {MAX_CLIENTS}\n")

        while True:
            conn, addr = server_socket.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr), name=f"Client-{addr[1]}", daemon=True)
            thread.start()


if __name__ == "__main__":
    run_server()
