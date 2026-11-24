from unittest.mock import Mock

import pytest

from source.inventory.exceptions import (
    ExternalDependencyError,
    InsufficientStockError,
    InvalidQuantityError,
    InventoryError,
    ProductNotFoundError,
)
from source.inventory.models import Product
from source.inventory.service import InventoryService


class TestDecreaseStock:
    def test_increases_stock_and_saves_new_value(self):
        # Stub: simula que la base de datos devuelve un producto con 10 unidades
        repo = Mock()
        repo.get_by_sku.return_value = Product(sku="LAP-01", name="Laptop", stock=10)

        service = InventoryService(repository=repo)
        result = service.increase_stock("LAP-01", 5)

        assert result == 15
        # Mock: verifica las llamadas exactas a la dependencia externa
        repo.get_by_sku.assert_called_once_with("LAP-01")
        repo.save_stock.assert_called_once_with("LAP-01", 15)

    @pytest.mark.parametrize(
        "invalid_quantity", [0, -1, -5, True, False, 2.5, "3", None]
    )
    def test_rejects_invalid_quantity_without_touching_repository(
        self, invalid_quantity
    ):
        repo = Mock()
        service = InventoryService(repository=repo)

        with pytest.raises(InvalidQuantityError):
            service.increase_stock("LAP-01", invalid_quantity)

        repo.get_by_sku.assert_not_called()
        repo.save_stock.assert_not_called()

    def test_raises_error_when_product_does_not_exist(self):
        repo = Mock()
        repo.get_by_sku.return_value = None

        service = InventoryService(repository=repo)

        with pytest.raises(ProductNotFoundError):
            service.increase_stock("UNKNOWN-SKU", 1)

        repo.save_stock.assert_not_called()

    def test_wraps_save_failure_in_domain_error(self):
        repo = Mock()
        repo.get_by_sku.return_value = Product(sku="LAP-01", name="Laptop", stock=10)
        repo.save_stock.side_effect = ConnectionError("Fallo al escribir en la BD")

        service = InventoryService(repository=repo)

        with pytest.raises(ExternalDependencyError):
            service.increase_stock("LAP-01", 5)
