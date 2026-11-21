from typing import Optional, Protocol

from .models import Product


class InventoryRepository(Protocol):
    """Contrato que simula la base de datos de inventario."""

    def get_by_sku(self, sku: str) -> Optional[Product]:
        """Obtiene un producto por su SKU o None si no existe."""
        pass

    def save_stock(self, sku: str, new_stock: int) -> None:
        """Guarda el stock actualizado para el SKU indicado."""
        pass
