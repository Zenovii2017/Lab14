from tic_tac_toe.arrays import Array2D


class Board:
    move_first_player = "x"
    move_second_player = "o"
    win_combination = [move_first_player, move_second_player]

    def __init__(self):
        """
        initialise class
        """
        self._game_board = Array2D(3, 3)
        self._last_move = []

    def __str__(self):
        """
        return str for print
        :return: str
        """
        to_print = "\n   0 1 2 \n   - - - \n"
        for j in range(self._game_board.num_cols()):
            to_print += str(j) + " "
            for i in range(self._game_board.num_rows()):
                value = self._game_board[i, j]
                if value is None:
                    value = " "
                to_print += "|{}".format(value)
            to_print += "|\n   - - - \n"
        return to_print

    def add_value(self, row, col, value):
        """
        set in board row and col value
        :param row: int
        :param col: int
        :param value: int
        :return:
        """
        self._game_board[row, col] = value

    def check_win(self):
        """
        check if someone win
        :return: list or None
        """

        def poz_value(row, col):
            """
            return pozition value
            :param row: int
            :param col: int
            :return: int or str or None
            """
            return self._game_board[row, col]

        def return_value(value):
            """
            return who is winner
            :param value: str or int
            :return: list
            """
            if value == Board.move_first_player:
                return [self._last_move, "first player win"]
            else:
                return [self._last_move, "second player win"]

        value = poz_value(0, 0)
        if value is not None:
            if poz_value(0, 1) == value and poz_value(0, 2) == value:
                return return_value(value)
            elif poz_value(1, 0) == value and poz_value(2, 0) == value:
                return return_value(value)
            elif poz_value(1, 1) == value and poz_value(2, 2) == value:
                return return_value(value)

        value = poz_value(0, 1)
        if value is not None:
            if poz_value(1, 1) == value and poz_value(2, 1) == value:
                return return_value(value)

        value = poz_value(2, 2)
        if value is not None:
            if poz_value(0, 2) == value and poz_value(1, 2) == value:
                return return_value(value)
            elif poz_value(2, 0) == value and poz_value(2, 1) == value:
                return return_value(value)

        value = poz_value(1, 0)
        if value is not None:
            if poz_value(1, 1) == value and poz_value(1, 2) == value:
                return return_value(value)

        value = poz_value(2, 0)
        if value is not None:
            if poz_value(1, 1) == value and poz_value(0, 2) == value:
                return return_value(value)

        for i in range(3):
            for j in range(3):
                if poz_value(i, j) is None:
                    return None

        return "draw"

    def first_player_move(self, row, col):
        """
        first player move
        :param row: int
        :param col: int
        :return: None
        """
        self._last_move = [row, col]
        self._game_board[row, col] = Board.move_first_player

    def second_player_move(self, row, col):
        """
        second player move
        :param row: int
        :param col: int
        :return: None
        """
        self._last_move = [row, col]
        self._game_board[row, col] = Board.move_second_player

    def is_good_move(self, row, col):
        """
        check if position is good or not for move
        :param row: int
        :param col: int
        :return: bool
        """
        if row < 0 or col < 0 or row > 3 or col > 3:
            return False
        return self._game_board[row, col] is None
