from Game import Game
from play_game import play_game


def player_vs_computer():
    print("Please choose your opponent:\n")
    print("1 - Random")
    print("2 - MiniMax\n")
    match int(input("Choice: ")):
        case 1:
            play_game(Game(algorithm=1))
        case 2:
            play_game(Game(algorithm=2))
        case _:
            print("Invalid choice. Please try again.\n")
            player_vs_computer()


def main():
    print("Please choose what you want to do:\n")
    print("1 - Player vs Player")
    print("2 - Player vs Computer\n")
    choice = input("Choice: ")

    if choice == "1":
        play_game(Game())
    elif choice == "2":
        player_vs_computer()
    else:
        print("Invalid choice. Please try again.\n")
        main()


if __name__ == '__main__':
    print("Welcome to Ataxx!")
    main()
