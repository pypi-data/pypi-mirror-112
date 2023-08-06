class Product:
    product_id: str
    weight: float
    brand: str

    def __init__(self, attrs=None):
        self.__dict__ = attrs or dict()
