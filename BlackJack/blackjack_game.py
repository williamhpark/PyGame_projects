import random

'''
A GAME OF BLACKJACK
'''

'''
Global variables
'''

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
             'Queen':10, 'King':10, 'Ace':11}

playing = True

'''
Class definitions
'''

# Card class

class Card:

    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f'{self.rank} of {self.suit}'

# Deck class

class Deck:

    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))

    def __str__(self):
        deck_comp = ''
        for card in self.deck:
            deck_comp += '\n' + card.__str__()
        return "The deck has: " + deck_comp

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        return self.deck.pop(0)

# Hand class

class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value
        self.aces = 0    # add an attribute to keep track of aces

    def adjust_for_ace(self):
        if self.value <= 10:
            self.value += 11
        else:
            self.value += 1
    
    def add_card(self,card):
        self.cards.append(card)
        if card.rank == 'Ace':
            self.aces += 1
            self.adjust_for_ace()
        else:
            self.value += values[card.rank]

# Chips class

class Chips:

    def __init__(self,total=100):
        while True:
            try:
                self.total = int(input("How many chips do you have to play with?: "))
            except:
                print("Invalid, please enter an ineteger.")
                continue
            else:
                print('\n')
                break
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet

'''
Custom Exception class
'''

class BustedException(Exception):
    pass

'''
Function definitions
'''

# Function for taking bets

def take_bet(chips):
    while True:
        try:
            chips.bet = int(input(f"How many chips do you want to bet? (Available: {chips.total}): "))
            assert(chips.bet <= chips.total)
        except ValueError:
            print("Invalid, please enter an integer.")
            continue
        except AssertionError:
            print(f"Invalid, you do not have enough chips to make this bet. You have {chips.total} chips.")
            continue
        else:
            print('\n')
            return chips.bet

# Function for taking hits

def hit(deck,hand):
    hand.add_card(deck.deal())

# Function prompting hit or stand

def hit_or_stand(deck,hand):
    global playing  # to control an upcoming while loop

    while True:
        choice = input("Would you like to hit or stand? H or S: ").capitalize()
        if choice[0] == 'H':
            hit(deck,hand)
            print('\n')
            break
        elif choice[0] == 'S':
            playing = False
            print('\n')
            break
        else:
            print("Invalid, please enter H or S.")
            continue

# Functions to display hands

# does not show the dealer's first card
def show_some(player,dealer):
    print("DEALER'S HAND:")
    print("<hidden card>")
    for i in range(1,len(dealer.cards)):
        print(dealer.cards[i])
    print('\n')
    print("PLAYER'S HAND:")
    for card in player.cards:
        print(card)
    print('\n')

# shows all cards
def show_all(player,dealer):
    print("DEALER'S HAND:")
    for card in dealer.cards:
        print(card)
    print(f"Dealer's hand value: {dealer.value}")
    print('\n')
    print("PLAYER'S HAND:")
    for card in player.cards:
        print(card)
    print(f"Player's hand value: {player.value}")
    print('\n')

# Functions for end of game scenarios

def player_busts(player,dealer,chips):
    if player.value > 21:
        show_all(player,dealer)
        print("PLAYER BUSTED!\n")
        chips.lose_bet()
        raise BustedException
    else:
        pass

def player_wins(player,dealer,chips):
    if dealer.value < 21 and player.value > dealer.value:
        show_all(player,dealer)
        print("PLAYER WINS!\n")
        chips.win_bet()
    else:
        pass

def dealer_busts(player,dealer,chips):
    if dealer.value > 21:
        show_all(player,dealer)
        print("PLAYER WINS! DEALER BUSTED!\n")
        chips.win_bet()
    else:
        pass

def dealer_wins(player,dealer,chips):
    if dealer.value <=21 and dealer.value > player.value:
        show_all(player,dealer)
        print("DEALER WINS!\n")
        chips.lose_bet()
    else:
        pass

def push(player,dealer):
    if dealer.value == player.value:
        show_all(player,dealer)
        print("Player and dealer tie! It's a push.\n")
    else:
        pass

'''
GAME CODE
'''

chips = Chips()

while True:

    # Print an opening statement
    print("Welcome to Blackjack!")

    # Create & shuffle the deck, deal two cards to each player
    deck = Deck()
    deck.shuffle()
    # create player and dealer hands
    p_hand = Hand()
    d_hand = Hand()
    # first card deal
    hit(deck,p_hand)
    hit(deck,d_hand)
    # second card deal
    hit(deck,p_hand)
    hit(deck,d_hand)

    # Prompt the Player for their bet
    take_bet(chips)

    try:
        while playing:  # recall this variable from our hit_or_stand function

            # Show cards (but keep one dealer card hidden)
            show_some(p_hand,d_hand)

            # Prompt for Player to Hit or Stand
            hit_or_stand(deck,p_hand)

            # If player's hand exceeds 21, run player_busts() and break out of loop
            player_busts(p_hand,d_hand,chips)

    except BustedException:
        pass

    while d_hand.value < 17:
        hit(deck,d_hand)

    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
    if p_hand.value <= 21:

        # Run different winning scenarios
        # player wins
        player_wins(p_hand,d_hand,chips)
        # dealer_busts
        dealer_busts(p_hand,d_hand,chips)
        # dealer wins
        dealer_wins(p_hand,d_hand,chips)
        # push
        push(p_hand,d_hand)

    # Inform Player of their chips total
    print(f"Chip total: {chips.total}")

    # Ask to play again
    play_again = input("Would you like to play again? Y or N: ").upper()
    if play_again[0] == 'Y':
        if chips.total == 0:
            print("Sorry, you don't have any money :(")
            break
        else:
            playing = True
            #clear page
            print('\n'*5)
            continue
    else:
        print("\nThank you for playing!")
        break
