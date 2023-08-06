"""
    Opening leads for Card Player class.

    Returns  a card_player_components PlayedCard which includes
    name: str
    reason: str
"""

from .card_player_components import SelectedCard


def opening_lead_card(suit_cards, contract):
    """Return the opening lead from a list of cards given the contract."""
    cards = sorted(suit_cards, key=lambda x: x.order, reverse=True)
    for card in cards:
        if card.value == 9:  # T is regarded as an honour
            card.is_honour = True

    (card, selection_code) = _select_card_from_suit(cards, contract)
    return SelectedCard(card.name, selection_code)

def _are_adjacent(card_1, card_2):
    """Return True if the cards are adjacent."""
    if abs(card_1.value - card_2.value) == 1:
        return True
    return False

def _select_card_from_suit(cards, contract):
    """Return the correct card from the selected suit."""
    # Suits with 4 or more cards
    if len(cards) >= 4:
        return _select_card_from_long_suit(cards, contract)

    # Suits with 3 cards
    if len(cards) == 3:
        return _select_card_from_triplet(cards, contract)

    # Doubletons
    if len(cards) == 2:
        return _select_card_from_doubleton(cards)

    # Singletons
    return (cards[0], '015')

def _select_card_from_long_suit(cards, contract):
    """Return the correct card from a long card suit."""

    if contract.is_nt:
        return _select_card_for_nt_contract(cards)

    # Suit headed by an A
    if cards[0].rank == 'A':
        return (cards[0], '013')

    # Suit headed by KQ
    if cards[0].rank == 'K' and cards[1].rank == 'Q':
        return (cards[0], '003')

    # Suit headed by 2 touching honours and next or next but one
    if (cards[0].is_honour and _are_adjacent(cards[0], cards[1])
            and cards[2].value >= cards[1].value - 2):
        return(cards[0], '003')

    # Suit headed by an honour: top of two touching cards
    if (cards[1].is_honour and _are_adjacent(cards[1], cards[2])):
        return (cards[1], '009')

    # With 4 rags, lead second highest
    if not cards[0].is_honour:
        return (cards[1], '014')

    # With an honour, lead fourth highest
    return (cards[3], '004')

def _select_card_for_nt_contract(cards):
    """Return the correct card from a long card suit in a NT contract."""

    # Suit headed by an honour: top of two touching cards
    if (cards[1].is_honour and _are_adjacent(cards[1], cards[2])):
        return (cards[1], '009')

    if (cards[2].is_honour and _are_adjacent(cards[2], cards[3])):
        return (cards[2], '009')

    # Lead fourth highest
    return (cards[3], '004')

def _select_card_from_triplet(cards, contract):
    """Return the correct card from a three card suit."""

    # Suit headed by A and no K in a NT contract
    if contract.is_nt:
        if cards[0].rank == 'A' and cards[1].rank != 'K':
            return (cards[2], '007')

    # Suit headed by an honour and are_adjacent card
    if cards[0].is_honour and _are_adjacent(cards[0], cards[1]):
        return (cards[0], '003')

    # Suit headed by an honour: top of two touching cards
    if (cards[1].is_honour and _are_adjacent(cards[1], cards[2])):
        return (cards[1], '008')

    # Suit headed by a QT
    if (cards[0].rank == 'Q' and cards[1].rank == 'T' and cards[2].value < 8):
        return (cards[2], '011')

    # Suit headed by two honours
    if (cards[0].is_honour and cards[1].is_honour):
        return (cards[2], '010')

    # Suit headed by an A
    if cards[0].rank == 'A':
        return (cards[0], '012')

    # Suit headed by a single honour
    if (cards[0].is_honour and not cards[1].is_honour):
        return (cards[2], '007')

    # Return middle card
    return (cards[1], '005')

def _select_card_from_doubleton(cards):
    """Return the correct card from a two card suit."""
    if cards[0].rank == 'A' and cards[1].rank == 'K':
        return (cards[1], '002')
    return (cards[0], '001')