pycard (pronounced picard)
==========================

pycard is a payment card validation library with a simple interface and no
external dependencies.

Installation
------------

```bash
pip install captain-pycard  # pycard was taken in PyPi
```

That's it, and there are no dependencies!

Usage
-----

```python
import pycard

# Create a card
card = pycard.Card(
    number='4444333322221111',
    month=1,
    year=2020,
    cvc=123
)

# Validate the card (checks that the card isn't expired and is mod10 valid)
assert card.is_valid

# Perform validation checks individually
assert not card.is_expired
assert card.is_mod10_valid

# The card is a visa
assert card.brand == 'visa'
assert card.friendly_brand == 'Visa'
assert card.mask == 'XXXX-XXXX-XXXX-1111'

# The card is a known test card
assert card.is_test
```
