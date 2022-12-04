class InvalidInputError(Exception):
    """ Takes in an exception and passes it to its definition """
    pass

class Mancala:
    """ Creates a Mancala game object """
    def __init__(self):
        self._players = {}
        self._turn = 1

    def create_player(self, name):
        """ Creates players """
        if len(self._players) <= 2:     # if players are not over 2
            if self._players:       # if the dictionary is not empty, player index num is 2 otherwise its 1
                num = 2
            else:
                num = 1

            player = Player(name)       # create player object
            self._players[num] = player     # add player to dictionary
            num += 1
        else:
            return "already two players."

    def play_game(self, player_index, pit):
        """  update seeds number in each pit and store.
        checks ending state of game, if end reached,
        update seeds number in pit and store for players. """

        if pit < 0 or pit > 6:
            raise InvalidInputError

        if player_index == 1:       # if player1 set player to player1 and opponent to player2
            player = self._players.get(player_index)
            opponent = self._players.get(player_index + 1)
        else:
            player = self._players.get(player_index)        # otherwise set player to player2 and opponent to player1
            opponent = self._players.get(player_index - 1)

        pit_index = pit - 1                     # set pit index(minus one to account for index numbering)
        seeds = player.get_pits()[pit_index]    # set seeds to amount in chosen pit
        player.get_pits()[pit_index] = 0        # set the chosen pit to zero
        pits_left = len(player.get_pits()) - pit
        run = 0

        if pits_left + 1 != seeds:          # if last seed doesn't land in store, change turn
            self.change_turn()

        while seeds > 0:
            run += 1
            if run > 1: pit = 1     # if on second run set pit to 1

            # mechanics for player's pits
            while pit < len(player.get_pits()) and seeds > 0:
                player.change_pits(pit)
                pit += 1
                seeds -= 1
                if seeds == 0:      # if seeds in turn are zero
                    if player.get_pits()[pit - 1] == 1:     # and last pit in turn changed was empty
                        pos = len(opponent.get_pits()) - pit        # get opponent's pit opposite player's pit
                        player.change_store(opponent.get_pits()[pos] + 1)   # place seeds in player's store
                        opponent.get_pits()[pos] = 0        # set opponent's pit to zero
                        player.get_pits()[pit - 1] = 0      # set player's last pit changed to zero

            # mechanics for player's store
            if seeds > 0:
                player.change_store(1)
                seeds -= 1
                if seeds == 0:      # if no more seeds player takes another turn
                    print(f"player {player_index} take another turn")

            # mechanics for opponent's pits
            index = 0
            while index < len(opponent.get_pits()) and seeds > 0:
                opponent.change_pits(index)
                index += 1
                seeds -= 1

        self.check_status()

        return self.board()

    def check_status(self):
        """ Checks status of game """

        if sum(self._players[1].get_pits()) == 0 or sum(self._players[2].get_pits()) == 0:
            for index in self._players:
                player = self._players.get(index)
                pit = 0

                while pit < len(player.get_pits()):
                    player.change_store(player.get_pits()[pit])
                    player.get_pits()[pit] = 0
                    pit += 1

            return "Game is ended"

    def board(self):
        """ Creates board for output, takes no params """
        board = []

        for index in self._players:
            player = self._players.get(index)
            pit = 0

            while pit < len(player.get_pits()):
                board.append(player.get_pits()[pit])
                pit += 1
            board.append(player.get_store())

        return board

    def change_turn(self):
        """ Changes the player turn """
        if self._turn == 1:
            self._turn = 2
        else:
            self._turn = 1

    def print_board(self):
        """ Prints the current board information """
        for key in self._players:
            player = self._players.get(key)
            print(f"player{key}: ")
            print(f"store: {player.get_store()}")
            print(player.get_pits())

    def return_winner(self):
        """ returns winner if any of the game,
        otherwise returns game not ended or tie. """
        scores_dict = {}

        if sum(self._players[1].get_pits()) == 0 or sum(self._players[2].get_pits()) == 0:
            for key in self._players:
                player = self._players.get(key)
                scores_dict[key] = player.get_name(), player.get_store() + sum(player.get_pits())
        else:
            return "Game has not ended"

        if scores_dict[1][1] > scores_dict[2][1]:
            return f"Winner is player 1: {scores_dict[1][0]}"
        elif scores_dict[1][1] < scores_dict[2][1]:
            return f"Winner is player 2: {scores_dict[2][0]}"
        else:
            return "It's a tie"

class Player:
    """ Creates a player object """
    def __init__(self, player_name):
        """ The constructor for the player object """
        self._player_name = player_name
        self._store = 0
        self._pits = [4, 4, 4, 4, 4, 4]

    def get_name(self):
        """ returns player index """
        return self._player_name

    def get_store(self):
        """ returns player store """
        return self._store

    def get_pits(self):
        """ returns pits """
        return self._pits

    def change_store(self, num):
        """ change the value of store """
        self._store += num

    def change_pits(self, index):
        """ changes the value of pits """
        self._pits[index] += 1


def main():
    """ Defines an exception """
    try:
        game = Mancala()
        player1 = game.create_player("Lily")
        player2 = game.create_player("Lucy")
        print(game.play_game(1, 9))

    except (InvalidInputError):
        print("Invalid number for pit index")

if __name__ == "__main__": main()



# game = Mancala()
# player1 = game.create_player("Lily")
# player2 = game.create_player("Lucy")
# print(game.play_game(1, 3))
# game.play_game(1, 1)
# game.play_game(2, 3)
# game.play_game(2, 4)
# game.play_game(1, 2)
# game.play_game(2, 2)
# game.play_game(1, 1)
# game.print_board()
# print(game.return_winner())

# game = Mancala()
# player1 = game.create_player("Lily")
# player2 = game.create_player("Lucy")
# game.play_game(1, 1)
# game.play_game(1, 2)
# game.play_game(1, 3)
# game.play_game(1, 4)
# game.play_game(1, 5)
# game.play_game(1, 6)
# game.print_board()
# print(game.return_winner())

# player 1 take another turn
# [4, 4, 0, 5, 5, 5, 1, 4, 4, 4, 4, 4, 4, 0]
# player 2 take another turn
# player1:
# store: 10
# [0, 0, 2, 7, 7, 6]
# player2:
# store: 2
# [5, 0, 1, 1, 0, 7]
# Game has not ended
