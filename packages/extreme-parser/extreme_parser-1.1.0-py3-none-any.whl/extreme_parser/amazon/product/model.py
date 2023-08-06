class Product:
    weight: float
    brand: str
    price_min: float
    price_max: float
    in_stock: bool

    def __init__(self, attrs=None):
        self.__dict__ = attrs or dict()
