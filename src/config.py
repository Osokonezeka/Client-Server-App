"""
Global configuration file for the Client-Server application.
"""

# The IP address the server will bind to.
# 127.0.0.1 means localhost (accessible only from the same machine).
HOST = '127.0.0.1'

# The port number the server will listen on.
PORT = 65432

# The maximum number of concurrent client connections the server will accept.
MAX_CLIENTS = 3
