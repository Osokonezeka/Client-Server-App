# Advanced Programming - Project (Client-Server)

Final project for the Advanced Programming course, implementing a multithreaded client-server application.

---

## 1. Technical Instructions

The project was written in Python. Python is an interpreted language, therefore the code does not require explicit compilation before execution.

### Prerequisites
* Installed Python (version 3.8 or newer).
* Installed dependencies from the `requirements.txt` file (mainly the testing framework).

### Package Installation
In the terminal, navigate to the main project directory and run the following command:
`pip install -r requirements.txt`

### Running the Server
The server must be started first. To do this, execute the following command:
`python src/server.py`

### Connecting Clients
Once the server is active, open a new terminal session and run the client:
`python src/client.py`
*(You can run this script multiple times in separate windows to test parallel connections and the MAX_CLIENTS limit).*

### Running Tests
The project includes unit, integration, and E2E tests. To run all tests (using the pytest framework), type the following in the terminal:
`pytest tests/`

---

## 2. Artificial Intelligence (AI) Usage Declaration


### Tools and Models Used
* **Google Gemini** – assistance in planning the project architecture and preparing the file structure.

### Scope of AI Usage in the Project
* Planning the file structure and logical division of the application (`server.py`, `client.py`, `models.py` modules).
* Generating the README.md documentation skeleton.

### Sample Prompts and Configuration Parameters 
