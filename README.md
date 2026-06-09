# Peer-to-Peer Battleship

My project is a terminal-based 3x3 Battleship game built in Python using socket programming. The application operates on a Peer-to-Peer model where a single script contains the logic to act as both the network host and the client. Communication between peers is managed over a TCP connection using serialized JSON payloads to route gameplay guesses, real-time chat messages, and game forfeits.

## Instructions for Build and Use

Steps to build and/or run the software:

1. Install Python: Ensure Python 3.x is installed on your operating system.
2. Save the Script: Clone or download the repository and locate the main.py file.
3. Open VS Code Terminals: Open the project directory in VS Code and initialize two independent terminal instances running side-by-side.

Instructions for using the software:

1. Initialize the Host (Peer 1): In one of the terminal windows, execute the program by running `python main.py`. When prompted, type `H` to select the Host role. The terminal will pause and display a message stating it is listening on port 5555.
2. Initialize the Connector (Peer 2): In the other terminal window, execute the program by running `python main.py`. When prompted, type `C` to connect. It will instantly connect to the waiting host.
3. Setup and Play: Both terminals will prompt you to input a secret row (0-2) and column (0-2) to hide your treasure. Take turns choosing options 1-3 to guess coordinates, text chat in real-time, or gracefully forfeit the match.
4. Server Re-use: If a match ends or a player quits, the connector terminal will shut down cleanly, while the host terminal loops back up to automatically listen for a fresh client connection.

## Development Environment

To recreate the development environment, you need the following software and standard libraries:

* Development IDE: Visual Studio Code
* Language Runtime: Python 3.x
* Socket Module: Standard Python library used for low-level networking and handling TCP/IP stream sockets.
* JSON Module: Standard Python library used to serialize dictionary payloads into strings before byte transmission, and deserialize them upon receipt.

## Useful Websites to Learn More

I found these websites useful in developing this software:

* [Python Socket Programming Tutorial](https://realpython.com/python-sockets/)
* [Python 3 Standard Library Documentation](https://docs.python.org/3/library/socket.html)
* [GeeksforGeeks - JSON Serialization in Python](https://www.geeksforgeeks.org/python/serializing-json-data-in-python/)

## Future Work

The following items I plan to fix, improve, and/or add to this project in the future:

* Expand Grid Dimensions: Scale the board size up from a 3x3 layout to a standard 10x10 grid with support for multiple multi-tiled naval ships.
* Implement Threading: Add multi-threading support to the socket listener so a host can handle background chat parsing simultaneously without locking the terminal line during a player's physical turn.
* Input Guess Validation: Build tracking arrays to catch and notify users if they accidentally guess the same grid coordinate more than once in a match.