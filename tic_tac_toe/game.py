from binary_search_tree.linkedbst import LinkedBST
from tic_tac_toe.board import Board
import random
import sys

sys.setrecursionlimit(150000)


class Game:
    """
    represent game in tic tac toe
    """
    def __init__(self):
        self._board = Board()

    def _build_tree(self):
        """
        build tree with random move for computer
        :return: None
        """

        def recurse(p):
            """
            make new board for branch
            :param p: BSTNode
            :return: None
            """
            if p is not None and p.data.check_win() is None:
                new_board = Board()
                for i in range(3):
                    for j in range(3):
                        new_board.add_value(i, j,
                                            p.data._game_board[i, j])
                move1_x = random.randint(0, 2)
                move1_y = random.randint(0, 2)
                move2_x = random.randint(0, 2)
                move2_y = random.randint(0, 2)

                while not new_board.is_good_move(move1_x, move1_y):
                    move1_x = random.randint(0, 2)
                    move1_y = random.randint(0, 2)
                new_board.second_player_move(move1_x, move1_y)

                if new_board.check_win() is None:
                    while not new_board.is_good_move(move2_x,
                                                     move2_y) or (
                            move1_x == move2_x and move1_y == move2_y):
                        move2_x = random.randint(0, 2)
                        move2_y = random.randint(0, 2)
                    new_board.first_player_move(move2_x, move2_y)

                self._builded_tree._add_right(p, new_board)
                recurse(self._builded_tree.super_find(new_board))

                if new_board.check_win() is None:
                    for i in range(3):
                        for j in range(3):
                            new_board.add_value(i, j,
                                                p.data._game_board[i, j])

                    move1_x = random.randint(0, 2)
                    move1_y = random.randint(0, 2)
                    move2_x = random.randint(0, 2)
                    move2_y = random.randint(0, 2)
                    while not new_board.is_good_move(move1_x, move1_y):
                        move1_x = random.randint(0, 2)
                        move1_y = random.randint(0, 2)

                    new_board.second_player_move(move1_x, move1_y)
                    if new_board.check_win() is None:
                        while not new_board.is_good_move(move2_x,
                                                         move2_y) or (
                                move1_x == move2_x and move1_y == move2_y):
                            move2_x = random.randint(0, 2)
                            move2_y = random.randint(0, 2)
                        new_board.first_player_move(move2_x, move2_y)

                    self._builded_tree._add_left(p, new_board)
                    recurse(self._builded_tree.super_find(new_board))
            return None

        self._builded_tree = LinkedBST()
        self._builded_tree.add(self._board)
        recurse(self._builded_tree.find(self._board))

    def search_max(self):
        """
        calculate which move computer is better
        :return: None
        """
        def recurse(item):
            """
            calculate how many points have branch
            :param item: BSTNode
            :return: int
            """
            if item is None:
                return 0
            if item.data.check_win() is not None and item.right is None and item.left is None:
                if item.data.check_win() == "draw":
                    return 0
                elif item.data.check_win()[1] == "first player win":
                    return -1
                else:
                    return 1
            else:
                try:
                    item.right
                    try:
                        item.left
                        return recurse(item.right) + recurse(item.left)
                    except:
                        return recurse(item.right)
                except:
                    try:
                        item.left
                        return recurse(item.left)
                    except:
                        return 0

        item = self._builded_tree._root
        left_item = item.left
        rigth_item = item.right
        print(recurse(left_item), recurse(rigth_item))
        if recurse(left_item) >= recurse(rigth_item):
            return "left"
        else:
            return "right"

    def move_computer(self):
        """
        generate computer move
        :return: None
        """
        self._build_tree()
        max = self.search_max()
        if max == "left" and self._builded_tree._root.left is not None:
            self._board = self._builded_tree._root.left.data
            row = self._builded_tree._root.left.data._last_move[0]
            col = self._builded_tree._root.left.data._last_move[1]
            if self._board._game_board[row, col] == "x":
                self._board.add_value(row, col, None)
        elif self._builded_tree._root.right is not None:
            self._board = self._builded_tree._root.right.data
            row = self._builded_tree._root.right.data._last_move[0]
            col = self._builded_tree._root.right.data._last_move[1]
            if self._board._game_board[row, col] == "x":
                self._board.add_value(row, col, None)

    def run(self):
        """
        run game
        :return: None
        """
        def check_win():
            """
            check if someone win
            :return: None
            """
            if self._board.check_win() is not None:
                if self._board.check_win() == "draw":
                    print("Draw!")
                elif self._board.check_win()[1] == "first player win":
                    print("You win!")
                else:
                    print("You lose!")
                sys.exit()

        print("Hello!")
        print("Let`s play game/ You will be move first because if you move "
              "second you will lose")

        while not self._board.check_win():
            move1 = int(input("Input your row move: "))
            move2 = int(input("Input your col move: "))

            while not self._board.is_good_move(move1, move2):
                move1 = int(input("Reinput your row move: "))
                move2 = int(input("Reinput your col move: "))

            self._board.first_player_move(move1, move2)
            check_win()
            print("Your move\n", self._board)
            self.move_computer()
            print("Computer move\n", self._board)
            check_win()


def main():
    """
    main function
    :return: None
    """
    game = Game()
    game.run()


if __name__ == '__main__':
    main()
