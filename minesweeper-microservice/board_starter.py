import time
import random

def read_board_file(file_path):
    with open(file_path, 'r') as file:
        data = file.read().strip()
    return [int(i) for i in data.split()]

def create_board(width, height, num_bombs):
    board = [0] * (width * height)
    bomb_positions = random.sample(range(width * height), num_bombs)
    for pos in bomb_positions:
        board[pos] = 1
    return board

def write_board_to_file(file_path, board):
    with open(file_path, 'w') as file:
        file.write(' '.join(map(str, board)))

def main():
    # this filepath is relative to this repository. Any changes to be made to the filepath can be done here
    file_path = 'board.txt'
    last_content = None

    # while loop ensures the polling is constant and will work until the user terminates the script
    while True:
        try:
            current_content = read_board_file(file_path)
            if current_content != last_content:
                width, height, num_bombs = current_content
                board = create_board(width, height, num_bombs)
                write_board_to_file(file_path, board)
                last_content = current_content
                print("Success")
        except Exception as e:
            print(f"Polling: {e}")
        
        time.sleep(3)  # Wait for 3 second for the example

        # A delay of 0.5 is introduced so that the terminal is not checking the file unnecessarily. Adjust time as needed
        # time.sleep(0.5)  # Wait for 0.5 second before checking the file again

if __name__ == '__main__':
    main()
