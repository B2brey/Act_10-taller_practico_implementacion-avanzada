from dataclasses import dataclass


@dataclass
class Product:
    sku: str
    name: str
    stock: int
    min_stock: int = 0
