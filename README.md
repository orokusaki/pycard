pycard (pronounced picard)
==========================

pycard is a credit card validation library with a simple interface and no
external dependencies.

Usage
-----

```python
from pycard.card import Card


card = Card(
    number='4444333322221111',
    month=1,
    year=2020,
    cvv2=123
)

# The card is not expired
assert not card.is_expired
# The card is mod10 valid
assert card.is_mod10_valid
# The card is valid
assert card.is_valid
# The card is a known test card
assert card.is_test
```
