import numpy as np
import random
from weights import Alphabet
import pyglet
from colorama import init

init()

class Board:

    points = (0, 0, 0, 300, 400, 800, 1400, 1800, 2000, 0, 0)
    width = height = 4

    def __init__(self, dict = 'words_dictionary.json', alpha = None, letters = [], dimensions = None):
        self.words = {}
        self.letters_used = []
        self.board = []
        self.selected = [[False, False, False, False],
                         [False, False, False, False],
                         [False, False, False, False],
                         [False, False, False, False]]
        self.score = 0
        self.dict = Alphabet(dict)
        self.currentWord = ""

        if alpha is None:
            alpha = self.dict.letters

        weights = self.dict.generate_weights(alpha)

        if (letters == []):
            for i in range(Board.width):
                row = [
                    Square(
                        i,
                        j,
                        np.random.choice(
                            [*weights], 1, p=list(weights.values())
                        ).item(),
                    )
                    for j in range(Board.height)
                ]
                self.board += [row]
        else:
            index = 0
            for i in range(Board.width):
                row = []
                for j in range(Board.height):
                     row += [Square(i,j, letters[index])]
                     index += 1
                self.board += [row]

    def resetSelected(self):
        for i in range(self.width):
            for j in range(self.height):
                self.selected[i][j] = False

    def __str__(self):
        print('\n' * 100)

        string = '\nSCORE: ' + str(self.score)+ '\n'
        string += f"TOTAL WORDS FOUND: {len(self.words)}" + '\n'
        string += self.currentWord.upper() + '\n\n'
        for i in range(self.width):
            row = '   '
            for j in range(self.height):
                row += (
                    "\033[1;30;47m"
                    + str(self.board[i][j]).upper()
                    + '\033[0;37;40m '
                    if self.selected[i][j]
                    else f'{str(self.board[i][j])} '
                )
            string += row + '\n'

        return string

    def __repr__(self):
        return str(self.board)

    def check_word(self, word):
        return self.dict.check_word(word);

    def add_word(self):
        if self.currentWord not in self.words:
            self.words[self.currentWord] = self.letters_used
            self.score += Board.points[len(self.currentWord)]

        self.letters_used = []
        self.currentWord = ""
        self.resetSelected()

    def add_letter(self, coord):
        next = self.getSquare(coord[0], coord[1])
        if len(self.currentWord) > 0:
            curr = self.getSquare(self.letters_used[-1][0], self.letters_used[-1][1])
        else:
            curr = next

        if not self.selected[coord[0]][coord[1]]:
            self.letters_used += [coord]
            self.currentWord += self.getSquare(coord[0], coord[1]).letter
            self.selected[coord[0]][coord[1]] = True

    def getSquare(self, row, column):
        try:
            return self.board[row][column]
        except IndexError as e:
            print("IndexError")
            return null

    def numWords(self):
        return len(self.words)

    def statistics(self):
        pass

    def getOrderedList(self):
        listWords = list(self.words)
        listWords.sort(reverse = True, key = lambda word: len(word))
        return listWords

    def endGame(self, full, outputFile):
        print(f"SCORE: {str(self.score)}")
        print(f"TOTAL WORDS FOUND: {len(self.words)}")
        print()
        listWords = self.getOrderedList()
        if (outputFile == ""):
            num = len(listWords) if full else min(len(listWords), 20)
            for i in range(num):
                print(f"{str(i + 1)}: {listWords[i]}")
        else:
            with open(outputFile, 'w') as f:
                for item in self.getOrderedList():
                    f.write(item + '\n')
            print(f"Word list written to {outputFile}.")

        print()

class Square:

    inst = {}

    def __init__(self, row, column, letter):
        self.coord = (row, column)
        self.neighbors = []
        Square.inst[self.coord] = self
        self.generateNeighbors(row, column)
        self.letter = letter

    def __str__(self):
        return self.letter

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return (isinstance(other, Square) and self.coord == other.coord
        and self.letter == other.letter)

    def generateNeighbors(self, row, column):
        for i in range(max(0, row - 1), min(Board.width, row + 2)):
            for j in range(max(0, column - 1), min(Board.height, column + 2)):
                if (i,j) != self.coord:
                    self.neighbors += [(i,j)]
