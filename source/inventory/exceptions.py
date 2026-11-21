class InventoryError(Exception):
    """Error base del dominio de inventario."""


class ProductNotFoundError(InventoryError):
    """Se lanza cuando no existe un producto con el SKU indicado."""


class InvalidQuantityError(InventoryError):
    """Se lanza cuando la cantidad no es un entero positivo válido."""


class InsufficientStockError(InventoryError):
    """Se lanza cuando no hay suficiente stock disponible."""


class ExternalDependencyError(InventoryError):
    """Se lanza cuando falla el repositorio o servicio externo."""
