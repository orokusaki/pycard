pycard (pronounced picard)
==========================

pycard is a payment card validation library with a simple interface and no
external dependencies.

Usage
-----

```python
from pycard.card import Card


# Create a card
card = Card(
    number='4444333322221111',
    month=1,
    year=2020,
    cvv2=123
)

# Validate the card (checks that the card isn't expired and is mod10 valid)
assert card.is_valid
```

Extras
------

```python
# ...continued from above example

# Perform validation checks individually
assert not card.is_expired
assert card.is_mod10_valid

# The card is a visa
assert card.brand == 'visa'

# The card is a known test card
assert card.is_test
```
