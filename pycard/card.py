import re
from calendar import monthrange
import datetime


class Card(object):
    """
    A credit card that may be valid or invalid.
    """
    # A regexp for matching non-digit values
    non_digit_regexp = re.compile(r'\D')

    # A mapping from common credit card brands to their number regexps
    BRAND_VISA = 'visa'
    BRAND_MASTERCARD = 'mastercard'
    BRAND_AMEX = 'amex'
    BRAND_DISCOVER = 'discover'
    BRAND_UNKNOWN = u'unknown'
    BRANDS = {
        BRAND_VISA: re.compile(r'^4\d{12}(\d{3})?$'),
        BRAND_MASTERCARD: re.compile(r'''
            ^(5[1-5]\d{4}|677189)\d{10}$|  # Traditional 5-series + RU support
            ^(222[1-9]|2[3-6]\d{2}|27[0-1]\d|2720)\d{12}$  # 2016 2-series
        ''', re.VERBOSE),
        BRAND_AMEX: re.compile(r'^3[47]\d{13}$'),
        BRAND_DISCOVER: re.compile(r'^(6011|65\d{2})\d{12}$'),
    }
    FRIENDLY_BRANDS = {
        BRAND_VISA: 'Visa',
        BRAND_MASTERCARD: 'MasterCard',
        BRAND_AMEX: 'American Express',
        BRAND_DISCOVER: 'Discover',
    }

    # Common test credit cards
    TESTS = (
        '4444333322221111',
        '378282246310005',
        '371449635398431',
        '378734493671000',
        '30569309025904',
        '38520000023237',
        '6011111111111117',
        '6011000990139424',
        '555555555554444',
        '5105105105105100',
        '4111111111111111',
        '4012888888881881',
        '4222222222222',
    )

    # Stripe test credit cards
    TESTS += (
        '4242424242424242',
    )

    def __init__(self, number, month, year, cvc, holder=None):
        """
        Attaches the provided card data and holder to the card after removing
        non-digits from the provided number.
        """
        self.number = self.non_digit_regexp.sub('', number)
        self.exp_date = ExpDate(month, year)
        self.cvc = cvc
        self.holder = holder

    def __repr__(self):
        """
        Returns a typical repr with a simple representation of the masked card
        number and the exp date.
        """
        return u'<Card brand={b} number={n}, exp_date={e}>'.format(
            b=self.brand,
            n=self.mask,
            e=self.exp_date.mmyyyy
        )

    @property
    def mask(self):
        """
        Returns the credit card number with each of the number's digits but the
        first six and the last four digits replaced by an X, formatted the way
        they appear on their respective brands' cards.
        """
        # If the card is invalid, return an "invalid" message
        if not self.is_mod10_valid:
            return u'invalid'

        # If the card is an Amex, it will have special formatting
        if self.brand == self.BRAND_AMEX:
            return u'XXXX-XXXXXX-X{e}'.format(e=self.number[11:15])

        # All other cards
        return u'XXXX-XXXX-XXXX-{e}'.format(e=self.number[12:16])

    @property
    def brand(self):
        """
        Returns the brand of the card, if applicable, else an "unknown" brand.
        """
        # Check if the card is of known type
        for brand, regexp in self.BRANDS.items():
            if regexp.match(self.number):
                return brand

        # Default to unknown brand
        return self.BRAND_UNKNOWN

    @property
    def friendly_brand(self):
        """
        Returns the human-friendly brand name of the card.
        """
        return self.FRIENDLY_BRANDS.get(self.brand, 'unknown')

    @property
    def is_test(self):
        """
        Returns whether or not the card's number is a known test number.
        """
        return self.number in self.TESTS

    @property
    def is_expired(self):
        """
        Returns whether or not the card is expired.
        """
        return self.exp_date.is_expired

    @property
    def is_valid(self):
        """
        Returns whether or not the card is a valid card for making payments.
        """
        return not self.is_expired and self.is_mod10_valid

    @property
    def is_mod10_valid(self):
        """
        Returns whether or not the card's number validates against the mod10
        algorithm (Luhn algorithm), automatically returning False on an empty
        value.
        """
        # Check for empty string
        if not self.number:
            return False

        # Run mod10 on the number
        dub, tot = 0, 0
        for i in range(len(self.number) - 1, -1, -1):
            for c in str((dub + 1) * int(self.number[i])):
                tot += int(c)
            dub = (dub + 1) % 2

        return (tot % 10) == 0


class ExpDate(object):
    """
    An expiration date of a credit card.
    """
    def __init__(self, month, year):
        """
        Attaches the last possible datetime for the given month and year, as
        well as the raw month and year values.
        """
        # Attach month and year
        self.month = month
        self.year = year

        # Get the month's day count
        weekday, day_count = monthrange(year, month)

        # Attach the last possible datetime for the provided month and year
        self.expired_after = datetime.datetime(
            year,
            month,
            day_count,
            23,
            59,
            59,
            999999
        )

    def __repr__(self):
        """
        Returns a typical repr with a simple representation of the exp date.
        """
        return u'<ExpDate expired_after={d}>'.format(
            d=self.expired_after.strftime('%m/%Y')
        )

    @property
    def is_expired(self):
        """
        Returns whether or not the expiration date has passed in American Samoa
        (the last timezone).
        """
        # Get the current datetime in UTC
        utcnow = datetime.datetime.utcnow()

        # Get the datetime minus 11 hours (Samoa is UTC-11)
        samoa_now = utcnow - datetime.timedelta(hours=11)

        # Return whether the exipred after time has passed in American Samoa
        return samoa_now > self.expired_after

    @property
    def mmyyyy(self):
        """
        Returns the expiration date in MM/YYYY format.
        """
        return self.expired_after.strftime('%m/%Y')

    @property
    def mmyy(self):
        """
        Returns the expiration date in MM/YY format (the same as is printed on
        cards.
        """
        return self.expired_after.strftime('%m/%y')

    @property
    def MMYY(self):
        """
        Returns the expiration date in MMYY format
        """
        return self.expired_after.strftime('%m%y')

    @property
    def mm(self):
        """
        Returns the expiration date in MM format.
        """
        return self.expired_after.strftime('%m')

    @property
    def yyyy(self):
        """
        Returns the expiration date in YYYY format.
        """
        return self.expired_after.strftime('%Y')
