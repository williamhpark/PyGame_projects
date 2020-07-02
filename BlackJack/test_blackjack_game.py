import unittest
import blackjack_game

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')

class TestCard(unittest.TestCase):

    def test_card_print(self):
        card = Card()
        str = print(card)
        self.assert(str, )

class TestDeck(unittest.TestCase):

    def test_deck_print:
        deck = Deck()
        str = print(deck)

if name == 'main':
    unittest.main()
