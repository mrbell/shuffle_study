from random import random
from tkinter import N
import numpy as np


class IdealShuffler(object):
    def shuffle(self, deck):
        return ideal_shuffler(deck) 


class RiffleShuffler(object):
    def __init__(self, distro=None):
        self.distro = distro
    def shuffle(self, deck):
        return riffle_shuffler(deck, self.distro)


class PileShuffler(object):
    def __init__(self, n_piles=7):
        self.n_piles = n_piles
    def shuffle(self, deck):
        return pile_shuffler(deck, self.n_piles)


class RandomPickupPileShuffler(object):
    def __init__(self, n_piles=7):
        self.n_piles = n_piles
    def shuffle(self, deck):
        return random_pickup_pile_shuffler(deck, self.n_piles)


class PileThenRiffleShuffler(object):
    def __init__(self):
        self.n_calls = 0
    def shuffle(self, deck):
        if self.n_calls == 0:
            result = random_pickup_pile_shuffler(deck)
        else:
            result = riffle_shuffler(deck)
        self.n_calls += 1
        return result


class RiffleCutShuffler(object):
    def __init__(self, distro=None):
        self.n_calls = 0
        self.distro = distro
    def shuffle(self, deck):
        if (self.n_calls + 1) % 3 == 0:
            result = cut_shuffler(deck)
        else:
            result = riffle_shuffler(deck, self.distro)
        self.n_calls += 1
        return result


def ideal_shuffler(deck):
    """
    Completely randomly shuffle a deck.
    """
    shuffled_deck = np.array(deck)
    np.random.shuffle(shuffled_deck)
    return shuffled_deck


def cut_deck(deck, proportion=0.5):

    cards_in_deck = len(deck)
    ideal_cut_position = int(cards_in_deck * proportion)

    min_cut_position = int(ideal_cut_position * 0.8)
    max_cut_position = int(ideal_cut_position + (cards_in_deck - ideal_cut_position) * 0.2)

    cut_position = np.random.randint(min_cut_position, max_cut_position + 1)

    return [deck[:cut_position], deck[cut_position:]]
    

def cut_shuffler(deck):
    """
    Cut a deck once somewhere in the middle of the deck, randomly chosen, 
    then swap position of halves.
    """
    deck_halves = cut_deck(deck)

    return np.concatenate([deck_halves[1], deck_halves[0]])


def tri_cut_shuffler(deck):
    """
    Cut the deck into ~thirds then reverse order.
    """
    first_third, rest_of_deck = cut_deck(deck, proportion=0.33)
    second_third, third_third = cut_deck(rest_of_deck)

    return np.concatenate([third_third, second_third, first_third])


def make_piles(deck, n_piles=7):

    piles = [[] for _ in range(n_piles)]
    
    for i, d in enumerate(deck):
        pile = i % n_piles
        piles[pile].append(d)

    return piles


def pile_shuffler(deck, n_piles=7):
    """
    Put cards into n_stacks, then put the stacks together in random order.
    """
    piles = make_piles(deck, n_piles)    
        
    shuffled_deck = np.concatenate(piles)
    
    return shuffled_deck


def random_pickup_pile_shuffler(deck, n_piles=7):
    """
    Put cards into n_stacks, then put the stacks together in random order.
    """
    piles = make_piles(deck, n_piles) 
        
    np.random.shuffle(piles)
    shuffled_deck = np.concatenate(piles)
    
    return shuffled_deck


def riffle_shuffler(deck, distro=None):
    """
    A simulation of riffle shuffling a deck.
    """

    if distro is None:
        distro = lambda: np.random.poisson(0.5) + 1

    deck_halves = cut_deck(deck)
    half_indices = [0, 0]  # current position in each deck half
    
    half = np.random.randint(2)  # which half gets added to the shuffled deck first
    
    # How far into the first half is the second half introduced
    offset = np.random.randint(1, int(len(deck_halves[half]) * 0.1))
    
    half_indices[half] = offset
    
    shuffled_deck = list(deck_halves[half][:offset])
    
    while all(hi <= len(h) for (hi, h) in zip(half_indices, deck_halves)):
        half = (half + 1) % 2
        number_from_this_half = distro()
        start_card = half_indices[half] 
        stop_card = min([
            start_card + number_from_this_half, 
            len(deck_halves[half]) + 1
        ])
        
        shuffled_deck.extend(list(deck_halves[half][start_card:stop_card]))
        
        half_indices[half] = stop_card
    
    half = (half + 1) % 2
    shuffled_deck.extend(list(deck_halves[half][
        half_indices[half]:(len(deck_halves[half])+1)
    ]))
    
    return np.array(shuffled_deck)


if __name__ == "__main__":
    fresh_deck = np.arange(60)

    print("Ideal shuffle")
    print(ideal_shuffler(fresh_deck))
    print()

    print("Cut shuffle")
    print(cut_shuffler(fresh_deck))
    print()

    print("Tricut shuffler")
    print(tri_cut_shuffler(fresh_deck))
    print()

    print("Pile shuffle")
    print(pile_shuffler(fresh_deck))
    print()

    print("Riffle shuffle")
    print(riffle_shuffler(fresh_deck))
    print()
