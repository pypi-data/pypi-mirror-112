"""Test opening lead cards."""

from ..source.opening_lead_card import opening_lead_card
from bridgeobjects import Card, Contract


HOLDING_SUIT_CONTRACT = {
    # Based on Klinger's Basic Bridge p138-9
    '95': ('9', '001'),
    '953': ('5', '005'),
    '96532': ('6', '014'),
    'T9': ('T', '001'),
    'T6': ('T', '001'),
    'T93': ('T', '003'),
    'T63': ('3', '007'),
    'T632': ('2', '004'),
    'T983': ('T', '003'),
    'T973': ('T', '003'),
    'T963': ('3', '004'),
    'JT': ('J', '001'),
    'J5': ('J', '001'),
    'JT6': ('J', '003'),
    'J52': ('2', '007'),
    'J542': ('2', '004'),
    'J9876': ('7', '004'),
    'J7542': ('4', '004'),
    'JT94': ('J', '003'),
    'JT84': ('J', '003'),
    'JT74': ('4', '004'),
    'QJ': ('Q', '001'),
    'Q4': ('Q', '001'),
    'QJ4': ('Q', '003'),
    'QT9': ('T', '008'),
    'QT4': ('4', '011'),
    'Q64': ('4', '007'),
    'QJT2': ('Q', '003'),
    'QJ92': ('Q', '003'),
    'QJ82': ('2', '004'),
    'QT98': ('T', '009'),
    'QT83': ('3', '004'),
    'Q9876': ('7', '004'),
    'Q8652': ('5', '004'),
    'KQ': ('K', '001'),
    'K2': ('K', '001'),
    'KQ5': ('K', '003'),
    'KJT': ('J', '008'),
    'KJ5': ('5', '010'),
    'KT9': ('T', '008'),
    'KT5': ('5', '010'),
    'K75': ('5', '007'),
    'KQJ2': ('K', '003'),
    'KQT2': ('K', '003'),
    'KQ92': ('K', '003'),
    'KJT2': ('J', '009'),
    'KJ92': ('2', '004'),
    'KT98': ('T', '009'),
    'KT84': ('4', '004'),
    'KQJ63': ('K', '003'),
    'KQT63': ('K', '003'),
    'KQ763': ('K', '003'),
    'K9873': ('7', '004'),
    'K8643': ('4', '004'),
    'AK': ('K', '002'),
    'A6': ('A', '001'),
    'AKQ': ('A', '003'),
    'AKJ': ('A', '003'),
    'AK3': ('A', '003'),
    'A93': ('A', '012'),
    'AKQ3': ('A', '013'),
    'AKJ3': ('A', '013'),
    'AK63': ('A', '013'),
    'AQJ3': ('A', '013'),
    'AQ63': ('A', '013'),
    'AJT3': ('A', '013'),
    'AJ63': ('A', '013'),
    'AT98': ('A', '013'),
    'AT52': ('A', '013'),
    'A987': ('A', '013'),
    'A963': ('A', '013'),
    'AKJ42': ('A', '013'),
    'AK742': ('A', '013'),
    'AQJ42': ('A', '013'),
    'AQT92': ('A', '013'),
    'AQT42': ('A', '013'),
    'AQ642': ('A', '013'),
    'AJT53': ('A', '013'),
    'AJ853': ('A', '013'),
    'AT983': ('A', '013'),
    'AT853': ('A', '013'),
    '53': ('5', '001'),
    '953': ('5', '005'),
    '9653': ('6', '014'),
    # Klinger Guide to Better Card Play p24
    '9742': ('7', '014'),
    'J7': ('J', '001'),
    'K83': ('3', '007'),
    'A964': ('A', '013'),
    '9': ('9', '015'),
    'KJ752': ('5', '004'),
    'Q9843': ('4', '004'),
    # 'xxx': ('xxx', 'xxx'),
    # 'xxx': ('xxx', 'xxx'),
    # 'xxx': ('xxx', 'xxx'),
}

HOLDING_NT_CONTRACT ={
    'KQ92': ('2', '004'),
    'KQ763': ('6', '004'),
    'A93': ('3', '007'),
    'AK63': ('3', '004'),
    'AQJ3': ('Q', '009'),
    'AJT3': ('J', '009'),
    'AT98': ('T', '009'),
    'AT52': ('2', '004'),
    'A987': ('7', '004'),
    'A963': ('3', '004'),
    'AK742': ('4', '004'),
    'AQJ42': ('Q', '009'),
    'AQT92': ('T', '009'),
    'AQT42': ('4', '004'),
    'AQ642': ('4', '004'),
    'AJT53': ('J', '009'),
    'AJ853': ('5', '004'),
    'AT983': ('T', '009'),
    'AT853': ('5', '004'),
}

def test_lead_suit_contract():
    """Test the lead card returned in a suit contract."""
    # Arbitrarily use spade suit and 'H' as the contract suit
    contract = Contract('4H')
    for holding, (lead_card, reason) in HOLDING_SUIT_CONTRACT.items():
        cards = [Card(card_name+'S') for card_name in holding]
        selected_card = opening_lead_card(cards, contract)
        assert selected_card == Card(lead_card+'S')
        assert selected_card.selection_reason == reason

def test_lead_nt_contract():
    """Test the lead card returned in a NT contract."""
    contract = Contract('3NT')
    for holding, (lead_card, reason) in HOLDING_NT_CONTRACT.items():
        cards = [Card(card_name+'S') for card_name in holding]
        selected_card = opening_lead_card(cards, contract)
        assert selected_card == Card(lead_card+'S')
        assert selected_card.selection_reason == reason