import random
import time
battlefield_Player = []
battlefield_Computer = []
ship_names = ["the NiÃ±a", "the Pinta", "the Santa Maria", "the Titanic", "the Going Merry", "the Mayflower", "the Flying Cloud", "the Flying Dutchman", "the Golden Hinde", "the Kamikaze", "the Glass Cannon", "the Millennium Falcon", "the Black Pearl", "the Bumblebee"]

def chooseBoard():
    while True:
        try:
            chosen_size = int(input("How big do you want the battlefield to be (Ex: 4 = 4x4): "))
            if chosen_size < 2 or chosen_size > 18:
                print("Please choose a size between 2 and 18.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a number.")
    cols = chosen_size + 1
    header = [""] + [chr(ord('A')+i) for i in range(chosen_size)]
    battlefield = [header]
    battlefield_Player.clear()
    battlefield_Computer.clear()
    battlefield_Player.append(header)
    battlefield_Computer.append(header.copy())
    for i in range(1, chosen_size+1):
        battlefield_Player.append([str(i)] + ["~"]*chosen_size)
        battlefield_Computer.append([str(i)] + ["~"]*chosen_size)
    return chosen_size, battlefield
    
def ship_placement(chosen_size, battlefield):
    player_ship_names = []
    used_names = []
    for i in range(2):
        while True:
            choice = input(f"Do you want to name your ship #{i+1} manually? (yes/no): ").strip().lower()
            if choice == 'yes':
                name = input(f"Enter a name for your ship #{i+1}: ").strip()
                if name and name not in used_names:
                    player_ship_names.append(name)
                    used_names.append(name)
                    break
                elif name in used_names:
                    print("That name has already been used. Please choose another.")
                else:
                    print("Ship name cannot be empty. Please enter a valid name.")
            elif choice == 'no':
                name = random.choice([n for n in ship_names if n not in used_names])
                print(f"Randomly chosen name: {name}")
                player_ship_names.append(name)
                used_names.append(name)
                break
            else:
                print("Invalid choice. Please enter 'yes' or 'no'.")
    ships = []
    taken = []  
    for i in range(2):
        while True:
            choice = input(f"Do you want to place ship '{player_ship_names[i]}' manually? (yes/no): ").strip().lower()
            if choice == 'yes':
                while True:
                    print_Pboard()
                    time.sleep(1)
                    coord = input(f"Enter the starting coordinate for '{player_ship_names[i]}' (e.g., A1): ").upper().strip()
                    if len(coord) >= 2 and coord[0] in [chr(ord('A')+j) for j in range(chosen_size)] and coord[1:].isdigit() and 1 <= int(coord[1:]) <= chosen_size:
                        col = ord(coord[0]) - ord('A') + 1
                        row = int(coord[1:])
                        orientation = input("Horizontal or vertical? (h/v): ").strip().lower()
                        time.sleep(1)
                        if orientation == 'h' and col+1 <= chosen_size:
                            coords = [(row, col), (row, col+1)]
                        elif orientation == 'v' and row+1 <= chosen_size:
                            coords = [(row, col), (row+1, col)]
                        else:
                            print("Invalid orientation or out of bounds. Try again.")
                            time.sleep(1)
                            continue
                        if any(c in taken for c in coords):
                            print("Ships cannot overlap. Try again.")
                            time.sleep(1)
                            continue
                        ships.append({'name': player_ship_names[i], 'coords': coords, 'hits': []})
                        taken.extend(coords)
                        for r, c in coords:
                            battlefield[r][c] = "O"
                        time.sleep(1)
                        break
                    else:
                        print("Invalid input. Try again.")
                        time.sleep(1)
                break
            elif choice == 'no':
                while True:
                    time.sleep(1)
                    orientation = random.choice(['h', 'v'])
                    row = random.randint(1, chosen_size)
                    col = random.randint(1, chosen_size)
                    if orientation == 'h' and col+1 <= chosen_size:
                        coords = [(row, col), (row, col+1)]
                    elif orientation == 'v' and row+1 <= chosen_size:
                        coords = [(row, col), (row+1, col)]
                    else:   
                        continue
                    if all(c not in taken for c in coords):
                        ships.append({'name': player_ship_names[i], 'coords': coords, 'hits': []})
                        taken.extend(coords)
                        print(f"Ship '{player_ship_names[i]}' placed randomly.")
                        for r, c in coords:
                            battlefield[r][c] = "O"
                        time.sleep(1)
                        break
                break
            else:
                print("Invalid choice. Please enter 'yes' or 'no'.")
                time.sleep(1)
    return ships

def PrintBoard(battlefield):
    for row in battlefield:
        print(' '.join(str(cell) for cell in row))

def startMenu():
    print("WELCOME TO OUR BATTLESHIP GAME !!!!!!\n______________________________________________________")
    time.sleep(1)
    print("The objective of the Game is to sink the enemy's ship by guessing their location.")
    time.sleep(1)
    print("You will be prompted to choose the board size and ship placement.")
    time.sleep(1)
    print("GOOD LUCK!!!\n")
    time.sleep(1)

def reset_board(chosen_size):
    guesses = []
    header = [""] + [chr(ord('A')+i) for i in range(chosen_size)]
    battlefield = [header]
    for i in range(1, chosen_size+1):
        battlefield.append([str(i)] + ["~"]*chosen_size)
    return guesses, battlefield

def random_move(chosen_size, battlefield):
    playerrandom_row = random.randint(1, chosen_size)
    playerrandom_col = random.randint(1, chosen_size)
    computerrandom_row = random.randint(1, chosen_size)
    computerrandom_col = random.randint(1, chosen_size)

    return playerrandom_col, computerrandom_row, playerrandom_row, computerrandom_col

def p_move(chosen_size, guesses, battlefield):
    while True:
        choice = input(f"Would you like to manually guess or no? (yes/no): ").strip().lower()
        if choice == 'yes':
            coord = input(f"Enter your guess (e.g., A1 to {chr(ord('A')+chosen_size-1)}{chosen_size}): ").upper().strip()
            if len(coord) >= 2 and coord[0] in [chr(ord('A')+i) for i in range(chosen_size)] and coord[1:].isdigit():
                guess_col = ord(coord[0]) - ord('A') + 1
                guess_row = int(coord[1:])
                if 1 <= guess_row <= chosen_size and 1 <= guess_col <= chosen_size:
                    if (guess_row, guess_col) not in guesses:
                        guesses.append((guess_row, guess_col))
                        battlefield[guess_row][guess_col] = "X"
                        PrintBoard(battlefield)
                        return guess_row, guess_col
                    else:
                        print("You already guessed that spot. Try again.")
                        continue
            print("Invalid input. Please enter a valid coordinate like B3.")
        elif choice == 'no':
            while True:
                guess_row = random.randint(1, chosen_size)
                guess_col = random.randint(1, chosen_size)
                if (guess_row, guess_col) not in guesses:
                    print(f"Random guess: {chr(ord('A')+guess_col-1)}{guess_row}")
                    guesses.append((guess_row, guess_col))
                    battlefield[guess_row][guess_col] = "X"
                    PrintBoard(battlefield)
                    return guess_row, guess_col
        else:
            print("Invalid choice. Please enter 'yes' or 'no'.")

def comp_guess(chosen_size, guesses):
    while True:
        guess_row = random.randint(1, chosen_size)
        guess_col = random.randint(1, chosen_size)
        if (guess_row, guess_col) not in guesses:
            print(f"Computer guesses: {chr(ord('A')+guess_col-1)}{guess_row}")
            return guess_row, guess_col
        
def print_Pboard():
    for row in battlefield_Player:
        print(' '.join(str(cell) for cell in row))

def print_CompBoard():
    for row in battlefield_Computer:
        print(' '.join(str(cell) for cell in row))

def rand_ship(chosen_size, taken_coords):
    while True:
        orientation = random.choice(['h', 'v'])
        row = random.randint(1, chosen_size)
        col = random.randint(1, chosen_size)
        if orientation == 'h':
            if col + 1 > chosen_size:
                continue
            coords = [(row, col), (row, col+1)]
        else:
            if row + 1 > chosen_size:
                continue
            coords = [(row, col), (row+1, col)]
        if any(c in taken_coords for c in coords):
            continue
        return coords

def comp_ship(chosen_size):
    chosen_names = random.sample(ship_names, 2)
    ships = []
    taken_coords = []  
    for name in chosen_names:
        coords = rand_ship(chosen_size, taken_coords)
        ships.append({'name': name, 'coords': coords, 'hits': []})
        taken_coords.extend(coords)
    ship_dict = {ship['name']: ship for ship in ships}
    return ships, ship_dict

def hit_check(ships, guess_row, guess_col):
    for ship in ships:
        if (guess_row, guess_col) in ship['coords']:
            if (guess_row, guess_col) not in ship['hits']:
                ship['hits'].append((guess_row, guess_col))
            if sorted(ship['coords']) == sorted(ship['hits']):
                return 'sunk', ship['name']
            return 'hit', ship['name']
    return 'miss', None

def game():
    startMenu()
    while True:
        chosen_size, _ = chooseBoard()
        user_guesses = []
        computer_guesses = []
        print("Player goes first.")
        player_ships = ship_placement(chosen_size, battlefield_Player)
        for ship in player_ships:
            for r, c in ship['coords']:
                battlefield_Player[r][c] = "O"
        comp_ships, _ = comp_ship(chosen_size)
        chances = 10
        game_over = False
        while chances > 0:
            print("\nYour turn! \n" \
            "Showing ENEMY BOARD:")
            time.sleep(1)
            print_CompBoard()
            while True:
                coord = input(f"Enter your guess (e.g., A1 to {chr(ord('A')+chosen_size-1)}{chosen_size}): ").upper().strip()
                if len(coord) >= 2 and coord[0] in [chr(ord('A')+i) for i in range(chosen_size)] and coord[1:].isdigit():
                    guess_col = ord(coord[0]) - ord('A') + 1
                    guess_row = int(coord[1:])
                    if 1 <= guess_row <= chosen_size and 1 <= guess_col <= chosen_size:
                        if (guess_row, guess_col) not in user_guesses:
                            user_guesses.append((guess_row, guess_col))
                            time.sleep(1)
                            hit = False
                            for ship in comp_ships:
                                if (guess_row, guess_col) in ship["coords"]:
                                    if (guess_row, guess_col) not in ship["hits"]:
                                        ship["hits"].append((guess_row, guess_col))
                                    hit = True
                                    if sorted(ship["hits"]) == sorted(ship["coords"]):
                                        print(f"You sunk the enemy's ship '{ship['name']}'!")
                                        battlefield_Computer[guess_row][guess_col] = "!"
                                        print_CompBoard()
                                    else:
                                        print(f"Hit! You hit the enemy's ship '{ship['name']}'!")
                                        battlefield_Computer[guess_row][guess_col] = "!"
                                        print_CompBoard()
                                    break
                            if not hit:
                                battlefield_Computer[guess_row][guess_col] = "X"
                                print("You missed!")
                                print_CompBoard()
                                time.sleep(1)
                            if all(sorted(ship["hits"]) == sorted(ship["coords"]) for ship in comp_ships):
                                print("You sunk all enemy ships! You win!")
                                print_CompBoard()
                                game_over = True
                                break
                            break
                        else:
                            print("You already guessed that spot. Try again.")
                            continue
                print("Invalid input. Please enter a valid coordinate like B3.")
            if game_over:
                break
            print("\nComputer's turn! \nShowing YOUR BOARD:")
            time.sleep(1)
            while True:
                comp_guess_row = random.randint(1, chosen_size)
                comp_guess_col = random.randint(1, chosen_size)
                if (comp_guess_row, comp_guess_col) not in computer_guesses:
                    computer_guesses.append((comp_guess_row, comp_guess_col))
                    time.sleep(1)
                    print(f"Computer guesses: {chr(ord('A')+comp_guess_col-1)}{comp_guess_row}")
                    time.sleep(1)
                    hit = False
                    for ship in player_ships:
                        if (comp_guess_row, comp_guess_col) in ship["coords"]:
                            if (comp_guess_row, comp_guess_col) not in ship["hits"]:
                                ship["hits"].append((comp_guess_row, comp_guess_col))
                            hit = True
                            if sorted(ship["hits"]) == sorted(ship["coords"]):
                                print(f"The computer sunk your ship '{ship['name']}'!")
                            else:
                                print(f"The computer hit your ship '{ship['name']}'!")
                            battlefield_Player[comp_guess_row][comp_guess_col] = "!"
                            break
                    if not hit:
                        if battlefield_Player[comp_guess_row][comp_guess_col] == "!":
                            battlefield_Player[comp_guess_row][comp_guess_col] = "!"
                        else:
                            battlefield_Player[comp_guess_row][comp_guess_col] = "X"
                        print("The computer missed!")
                    if all(sorted(ship["hits"]) == sorted(ship["coords"]) for ship in player_ships):
                        print_Pboard()
                        print("All your ships have been sunk! Computer wins!")
                        game_over = True
                        break
                    break
            print_Pboard()
            if game_over:
                break
            chances -= 1
            print(f"Chances left: {chances}")
            time.sleep(2)
        if not game_over:
            time.sleep(1)
            print("\nOut of chances! The enemy ships were at: ")
            for ship in comp_ships:
                coord_list = [f"{chr(ord('A')+c-1)}{r}" for r,c in ship['coords']]
                print(f"{ship['name']}: {coord_list}")
                for r, c in ship['coords']:
                    battlefield_Computer[r][c] = "O"
            print_CompBoard()
            user_guess_list = [f"{chr(ord('A')+c-1)}{r}" for r,c in user_guesses]
            print("Your guesses this round:", user_guess_list)
        while True:
            again = input("Play again? (yes/no): ").strip().lower()
            if again == 'yes':
                break
            elif again == 'no':
                print("Thanks for playing!")
                return
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")

if __name__ == "__main__":
    game()