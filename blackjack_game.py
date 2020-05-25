'''
AUTHOR : Duong Vu Tuan Minh
APP: Blackjack game
DATE: 14/5/2020
'''

import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}

playing = True

class Card:                        
    def __init__(self,rank, suit):
        self.rank = rank 
        self.suit = suit
    
    def __str__(self):
        return f"{self.rank} of {self.suit}"

class Deck:
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                #for each suit and rank, make a card
                card = Card(rank, suit)  #creating an instance of a class
                self.deck.append(card) #append the made card into the deck
    
    def shuffle(self):
        random.shuffle(self.deck) #shuffle the deck up
    
    def deal(self):
        popped_card = self.deck.pop() #pop one card out of the deck, save the value of the card inside a variable
        return popped_card

class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.ace = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[str(card.rank)]
        if card.rank == "Ace":
            self.ace += 1

    def adjust_for_ace(self):
        if self.ace:
            self.value -= 10
            self.ace -= 1

class Chips:
    def __init__(self, chips_amount):
        self.total = chips_amount
        self.bet = 0

    def win_bet(self):
        self.total += self.bet
    
    def lose_bet(self):
        self.total -= self.bet

def take_bet(chips):
    while True:
        try:
            chips.bet = int(input("Place a bet!\n"))
        except:
            print('Sorry this is not a valid bet!!')
        else:
            if chips.bet > chips.total:
                print(f'The bet amount must not exceed {chips.total}')
            else:
                break

def hit(taker, deck): #hit means that the player or dealer add a card to their hand, adjust if they got an ace
    taker.add_card(deck.deal())
    taker.adjust_for_ace()

def hit_or_stand(taker, deck): #this is the player choice, once the player choose to stand, the dealer continues hitting until it reachs 17. Whenever the player choose to stand, all the cards of the dealer are shown to the screen 
    global playing

    while True:
        x = input('\nDo you want to hit or stand?\n\t1. Hit\n\t2. Stand\n')
        if x == "1":
            print("Player hits!!")
            hit(taker, deck)
        elif x == '2':
            print('The player stands. Dealer pushs!!!')
            playing = False
        else: 
            print('Please choose hit or stand by entering the number!!')
        break

def show_some(player, dealer):
    print("\nDealer's hand: ")
    print('<hidden card>')
    print(f'{str(dealer.cards[1])}')
    print("\nPlayer's hand:", *player.cards, sep = '\n')

def show_all(player, dealer):
    print("\nDealer's hand:\n", *dealer.cards, sep = '\n')
    print(f"Dealer's value: {dealer.value}")
    print("\nPlayer's hand:", *player.cards, sep = '\n')
    print(f"Player's value: {player.value}")

#different winning scenarios
def player_win(chips):
    print("Player wins!")
    chips.win_bet()
def player_bust(chips):
    print('Player busts')
    chips.lose_bet()
def dealer_win(chips):
    print("Dealer wins!")
    chips.lose_bet()
def dealer_bust(chips):
    print("Dealer busts!")
    chips.win_bet()
def push():
    print("It's a tie!!")


if __name__ == "__main__":
    chips_amount = int(input("Let's buy some chips? How much chips do you want to buy?\n"))
    chips = Chips(chips_amount)
    print(f'{chips.total} bought! Transaction completed!!!')
    while True:
        deck = Deck()
        deck.shuffle()

        player = Hand()
        player.add_card(deck.deal())
        player.add_card(deck.deal())

        dealer = Hand()
        dealer.add_card(deck.deal())
        dealer.add_card(deck.deal())

        take_bet(chips)

        show_some(player, dealer)

        while playing:
            hit_or_stand(player,deck)
            show_some(player, dealer)

            if player.value > 21:
                player_bust(chips)
                break
            
        if player.value <= 21:

            while dealer.value < 17:
                hit(dealer, deck)
            show_all(player, dealer) #you can put this show_all() inside the while loop if you want to see the dealer's cards change each times.

            if dealer.value > 21:       
                dealer_bust(chips)
            elif player.value > dealer.value:
                player_win(chips)
            elif dealer.value > player.value:
                dealer_win(chips)
            else:
                push()

        print(f"\nEnd game! The total chips: {chips.total}")
        choice = input("Rematch?")
        if choice[0].lower() == 'y':
            playing = True
            continue
        else:
            print('See you next time at the casino!!')
            break

