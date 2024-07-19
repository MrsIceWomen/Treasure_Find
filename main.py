import random
import logging


class TreasureMap:
    def __init__(self, size):
        self.size = size
        self.treasure_location = self.generate_treasure_location()

    def generate_treasure_location(self):
        x = random.randint(1, self.size)
        y = random.randint(1, self.size)
        return x, y

    def is_treasure_at(self, x, y):
        return (x, y) == self.treasure_location

    def get_help(self, x, y):
        treasure_x, treasure_y = self.treasure_location
        distance = abs(treasure_x - x) + abs(treasure_y - y)
        if distance == 0:
            return 'You found the treasure!!!'
        elif distance <= 1:
            return 'Very hot!\n'
        elif distance <= 3:
            return 'Hot!\n'
        elif distance <= 5:
            return 'Warm!\n'
        elif distance <= 7:
            return 'Cold.\n'
        else:
            return 'Very cold.\n'


class Player:
    def __init__(self):
        self.attemps = 0
        self.coordinates = []

    def choose_coordinates(self, x, y):
        self.coordinates.append((x, y))
        self.attemps += 1
        print('Attempt №' + str(self.attemps))


class Game:
    def __init__(self):
        self.size = self.choose_size()
        self.max_attemps = self.size + 5
        self.map = TreasureMap(self.size)
        self.player = Player()
        logging.basicConfig(filename='log.txt', level=logging.INFO)

    def choose_size(self):
        while True:
            try:
                size = int(input('Choose the size of the map: '))
                if size > 4:
                    return size
                else:
                    raise ValueError('The size must be greater than 4')
            except ValueError:
                print('Invalid input. Please enter a number greater than 4.')

    def start(self):
        print('Welcome to the TreasureMap game!')
        print(f'The map is {self.size}x{self.size}.')
        print(f'You have {self.max_attemps} attempts to find the treasure.')
        print('You have to find the treasure by choosing coordinates.')
        print('Enter the coordinates one by one (first x, then y).')
        print('Good luck!\n')

        while self.player.attemps < self.max_attemps:
            try:
                x = self.get_x()
                y = self.get_y()
                self.player.choose_coordinates(x, y)
                print(f'You have {self.max_attemps - self.player.attemps} attemps.')
                logging.info(f'Player chose coordinates: ({x}, {y}).')
                if self.map.is_treasure_at(x, y):
                    print(self.map.get_help(x, y))
                    print('Congratulations! You win!')
                    print(f'It took you {self.player.attemps} attempts.')
                    break
                else:
                    clue = self.map.get_help(x, y)
                    print(clue)
                    logging.info(f'Clue: {clue}')
            except ValueError as e:
                print(f'Error: {e}')
        if self.player.attemps >= self.max_attemps:
            print('You lose! You have used all your attempts.')
            logging.info('Player lost the game.')

    def get_x(self):
        while True:
            try:
                x = int(input(f'Enter the x (1 to {self.size}): '))
                if 0 < x <= self.size:
                    return x
                else:
                    raise ValueError(f'The x must be between 1 and {self.size}.')
            except ValueError as e:
                print(f'Error: {e}')

    def get_y(self):
        while True:
            try:
                y = int(input(f'Enter the y (1 to {self.size}): '))
                if 0 < y <= self.size:
                    return y
                else:
                    raise ValueError(f'The y must be between 1 and {self.size}.')
            except ValueError as e:
                print(f'Error: {e}')


if __name__ == '__main__':
    game = Game()
    game.start()



import unittest

class TestTreasureMap(unittest.TestCase):
    def test_generate_treasure_location(self):
        map = TreasureMap(10)
        x, y = map.treasure_location
        self.assertTrue(0 < x <= 10 and 0 < y <= 10)

    def test_is_treasure_at(self):
        map = TreasureMap(10)
        x, y = map.treasure_location
        self.assertTrue(map.is_treasure_at(x, y))
        self.assertFalse(map.is_treasure_at(x + 1, y))

    def test_get_help(self):
        map = TreasureMap(10)
        x, y = map.treasure_location
        self.assertEqual(map.get_help(x, y), 'You found the treasure!!!')
        self.assertEqual(map.get_help(x, y + 1), 'Very hot!\n')
        self.assertEqual(map.get_help(x + 3, y), 'Hot!\n')
        self.assertEqual(map.get_help(x + 5, y), 'Warm!\n')
        self.assertEqual(map.get_help(x + 7, y), 'Cold.\n')
        self.assertEqual(map.get_help(x + 9, y), 'Very cold.\n')
        self.assertEqual(map.get_help(x + 4, y + 3), 'Cold.\n')
        self.assertEqual(map.get_help(x + 3, y + 3), 'Cold.\n')


class TestPlayer(unittest.TestCase):
    def test_choose_coordinates(self):
        player = Player()
        player.choose_coordinates(1, 1)
        self.assertEqual(player.coordinates, [(1, 1)])
        self.assertEqual(player.attemps, 1)
        player.choose_coordinates(2, 2)
        self.assertEqual(player.coordinates, [(1, 1), (2, 2)])
        self.assertEqual(player.attemps, 2)


class TestGame(unittest.TestCase):
    def test_game_initialisation(self):
        game = Game()
        self.assertIsInstance(game.map, TreasureMap)
        self.assertIsInstance(game.player, Player)

if __name__ == '__main__':
    unittest.main()