

from Food import Food
from BioLabel import BioLabel


class BioFood(Food,BioLabel):

    def __init__(self, id, name, price, stock, expired_by, label):
        Food.__init__(id, name, price, stock, expired_by)
        BioLabel.__init__(label=label)