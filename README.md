pycard (incorrectly pronounced Picard)
======================================

pycard Card is a credit card validation library with a simple interface and no
external dependencies.

Usage
-----

    >>> from pycard.card import Card
    >>>
    >>> card = Card(
    ...     number='4444333322221111',
    ...     month=1,
    ...     year=2013,
    ...     cvv2=123
    ... )
    ...
    >>> card
    <pycard.Card brand=visa, number=XXXX-XXXX-XXXX-1111, exp_date=01/2013>
    >>> # Check whether or not the card is valid
    >>> card.is_valid
    False
    >>> # Check whether or not the card's number is valid
    >>> card.is_mod10_valid
    True
    >>> # Check whether or not the card is expired
    >>> card.is_expired
    True
    >>> # Check whether or not the card is a test card
    >>> card.is_test
    True
