# Advanced Programming - Project (Client-Server)

Final project for the Advanced Programming course, implementing a multithreaded client-server application.

---

## 1. Team Composition and Responsibilities

* **Stanisław Grupiński (Sole Developer)** – Responsible for the entire project, including:
  * Server architecture, multithreading (`server.py`), connection limit implementation (`MAX_CLIENTS`), and logging configuration.
  * Client logic (`client.py`), stream processing using Python generators, and intentional casting error handling.
  * Data models (`models.py`), object serialization/deserialization mechanisms, and global configuration (`config.py`).
  * Automated testing (unit, integration, E2E) and project documentation (README).

---

## 2. Technical Instructions

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

## 3. Artificial Intelligence (AI) Usage Declaration

During the development of this project, Artificial Intelligence tools were used to support the creative process and ensure code quality.

### Tools and Models Used
* **Google Gemini 2.5 Pro** – assistance in planning the project architecture, generating code skeletons, and refactoring.

### Scope of AI Usage in the Project
* Planning the file structure and logical division of the application.
* Generating the initial skeleton of the multithreaded server and client logic.
* Reviewing code (e.g., transitioning from standard `print` statements to the Python `logging` module).
* Formulating proper Git commit messages based on Conventional Commits standards.

### Sample Prompts and Configuration Parameters
The following are actual prompts used in communication with the AI model during the development process:
1. **Architecture Planning:** *"Hello, please review this file and think about a blueprint of how this project should look like. Do not generate files, just give me your vision of this project."*
2. **Documentation Generation:** *"Based on all the project files and the provided PDF requirements, generate the README.md file."*
3. **Refactoring & Code Review:** *"What do you think about this file? [pasted client code with for-loop modifications]"*
4. **Git Operations Support:** *"Give me a short GitHub commit message, including the branch name and description."*