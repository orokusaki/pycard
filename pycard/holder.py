class Holder(object):
    """
    A credit card holder.
    """
    def __init__(self, first, last, street, post_code):
        """
        Attaches holder data for later use.
        """
        self.first = first
        self.last = last
        self.street = street
        self.post_code = post_code

    def __repr__(self):
        """
        Returns a typical repr with a simple representation of the holder.
        """
        return u'<Holder name={n}>'.format(n=self.name)

    @property
    def name(self):
        """
        Returns the full name of the holder.
        """
        return u'{f} {l}'.format(f=self.first, l=self.last)
