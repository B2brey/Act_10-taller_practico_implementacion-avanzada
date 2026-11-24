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
        self._validate_positive_quantity(quantity)
        product = self._get_product_or_raise(sku)
        self._ensure_sufficient_stock(product, quantity)

        new_stock = product.stock - quantity
        self._persist_stock(sku, new_stock)
        return new_stock

    def increase_stock(self, sku: str, quantity: int) -> int:
        self._validate_positive_quantity(quantity)
        product = self._repository.get_by_sku(sku)
        new_stock = product.stock + quantity
        self._repository.save_stock(sku, new_stock)
        return new_stock

    def _ensure_sufficient_stock(self, product: Product, quantity: int) -> None:
        if product.stock < quantity:
            raise InsufficientStockError("Stock insuficiente para descontar.")

    def _get_product_or_raise(self, sku: str) -> Product:
        try:
            product = self._repository.get_by_sku(sku)
        except Exception as exc:
            raise ExternalDependencyError("Error al consultar el repositorio.") from exc

        if product is None:
            raise ProductNotFoundError(f"Producto '{sku}' no encontrado.")
        return product

    def _validate_positive_quantity(self, quantity: int) -> None:
        # En Python bool es subclase de int, por eso se descarta explícitamente
        if not isinstance(quantity, int) or isinstance(quantity, bool) or quantity <= 0:
            raise InvalidQuantityError("La cantidad debe ser un entero positivo.")

    def _persist_stock(self, sku: str, new_stock: int) -> None:
        try:
            self._repository.save_stock(sku, new_stock)
        except Exception as exc:
            raise ExternalDependencyError("Error al guardar el stock.") from exc
