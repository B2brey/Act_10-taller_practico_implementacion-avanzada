from .exceptions import (
    ExternalDependencyError,
    InsufficientStockError,
    InvalidQuantityError,
    ProductNotFoundError,
)
from .models import Product
from .ports import InventoryRepository


class InventoryService:
    """Gestiona las operaciones de inventario sobre un repositorio inyectado."""

    def __init__(self, repository: InventoryRepository) -> None:
        self._repository = repository

    def decrease_stock(self, sku: str, quantity: int) -> int:
        # Obtiene el producto, calcula el nuevo stock y lo guarda en el repositorio
        product = self._repository.get_by_sku(sku)
        new_stock = product.stock - quantity
        self._repository.save_stock(sku, new_stock)
        return new_stock
