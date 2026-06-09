import socket
import json
import sys

def create_grid():
    grid = [[" " for _ in range(3)] for _ in range(3)]
    print("\n--- Hide Your Treasure ---")
    
    while True:
        try:
            row = int(input("Enter row to hide treasure (0-2): "))
            col = int(input("Enter column to hide treasure (0-2): "))
            if 0 <= row <= 2 and 0 <= col <= 2:
                grid[row][col] = "T"
                return grid, (row, col)
            print("Invalid coordinates. Please choose numbers between 0 and 2.")
        except ValueError:
            print("Please enter valid integers.")

def print_game_boards(my_grid, tracking_grid):
    print("\n  [Your Board]      [Your Guesses]")
    print("   0   1   2          0   1   2")
    for i in range(3):
        print(f"{i}  {' | '.join(my_grid[i])}      {i}  {' | '.join(tracking_grid[i])}")
        if i < 2:
            print("  ---+---+---        ---+---+---")

def send_json_message(sock, message_dict):
    json_string = json.dumps(message_dict)
    sock.sendall(json_string.encode('utf-8'))

def receive_json_message(sock):
    raw_data = sock.recv(1024)
    if not raw_data:
        return None
    return json.loads(raw_data.decode('utf-8'))

def play_game(connection, is_my_turn):
    my_grid, my_treasure = create_grid()
    tracking_grid = [[" " for _ in range(3)] for _ in range(3)]
    game_over = False

    try:
        while not game_over:
            print_game_boards(my_grid, tracking_grid)
            
            if is_my_turn:
                print("\n--- YOUR TURN ---")
                print("Options: (1) Guess Coordinates, (2) Send Chat, (3) Forfeit Game")
                choice = input("Select an action (1-3): ").strip()
                
                if choice == '1':
                    try:
                        r = int(input("Enter target row (0-2): "))
                        c = int(input("Enter target column (0-2): "))
                        payload = {"type": "GUESS", "coordinates": [r, c]}
                        send_json_message(connection, payload)
                        
                        response = receive_json_message(connection)
                        if response and response.get("type") == "RESPONSE":
                            result = response.get("result")
                            print(f"\nResult of your guess: {result}!")
                            if result == "HIT":
                                tracking_grid[r][c] = "X"
                                print("Congratulations! You found their treasure and won the game!")
                                game_over = True
                            else:
                                tracking_grid[r][c] = "O"
                                is_my_turn = False
                    except ValueError:
                        print("Invalid numbers. You lost your turn focus.")
                        is_my_turn = False
                        
                elif choice == '2':
                    msg_text = input("Type your chat message: ")
                    payload = {"type": "CHAT", "message": msg_text}
                    send_json_message(connection, payload)
                    
                elif choice == '3':
                    payload = {"type": "QUIT", "message": "I am forfeiting the game."}
                    send_json_message(connection, payload)
                    print("\nYou forfeited the game.")
                    game_over = True
                    
            else:
                print("\n--- OPPONENT'S TURN ---")
                print("Waiting for opponent to make a move...")
                
                incoming = receive_json_message(connection)
                if incoming is None:
                    print("\nConnection lost. Opponent disconnected unexpectedly.")
                    break
                    
                msg_type = incoming.get("type")
                
                if msg_type == "GUESS":
                    r, c = incoming.get("coordinates")
                    print(f"\nOpponent guessed coordinates: Row {r}, Column {c}")
                    
                    if (r, c) == my_treasure:
                        send_json_message(connection, {"type": "RESPONSE", "result": "HIT"})
                        my_grid[r][c] = "X"
                        print("Oh no! The opponent found your treasure. You lose!")
                        game_over = True
                    else:
                        send_json_message(connection, {"type": "RESPONSE", "result": "MISS"})
                        my_grid[r][c] = "O"
                        is_my_turn = True
                        
                elif msg_type == "CHAT":
                    print(f"\n[CHAT RECEIVED]: {incoming.get('message')}")
                    
                elif msg_type == "QUIT":
                    print(f"\nOpponent message: {incoming.get('message')}")
                    print("Opponent has quit. You win by default!")
                    game_over = True

    except Exception as e:
        print(f"\nAn error occurred during network transmission: {e}")
    finally:
        connection.close()

def main():
    print("Welcome to Peer-to-Peer Battleship!")
    role = input("Do you want to (H)ost the game or (C)onnect to a peer? ").strip().lower()
    
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    port = 5555
    
    if role == 'h':
        my_socket.bind(('127.0.0.1', port))
        my_socket.listen(1)
        
        while True: 
            print(f"\nListening for a peer connection on port {port}...")
            try:
                connection, address = my_socket.accept()
                print(f"Connected to peer at {address}")
                
                play_game(connection, is_my_turn=True)
                
                print("Match concluded. Ready for a new opponent.")
            except KeyboardInterrupt:
                print("\nShutting down host server.")
                break
            except Exception as e:
                print(f"Error handling connection: {e}")
                
        my_socket.close()

    elif role == 'c':
        print(f"Connecting to peer on port {port}...")
        try:
            my_socket.connect(('127.0.0.1', port))
            print("Successfully connected to the host!")
            
            play_game(my_socket, is_my_turn=False)
            
        except ConnectionRefusedError:
            print("Could not connect. Make sure the host terminal is running first.")
        finally:
            my_socket.close()

if __name__ == "__main__":
    main()