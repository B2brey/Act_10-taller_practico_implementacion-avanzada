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
    def test_decreases_stock_and_saves_new_value(self):

        # Stub: simula que la base de datos devuelve un producto con 10 unidades
        repo = Mock()
        repo.get_by_sku.return_value = Product(sku="LAP-01", name="Laptop", stock=10)

        service = InventoryService(repository=repo)
        remaining = service.decrease_stock("LAP-01", 3)

        assert remaining == 7

        # Mock: verifica las llamadas exactas a la dependencia externa
        repo.get_by_sku.assert_called_once_with("LAP-01")
        repo.save_stock.assert_called_once_with("LAP-01", 7)

    @pytest.mark.parametrize("invalid_quantity", [0, -1, -5])
    def test_rejects_non_positive_quantity_without_touching_repository(
        self, invalid_quantity
    ):
        repo = Mock()
        service = InventoryService(repository=repo)

        with pytest.raises(InvalidQuantityError):
            service.decrease_stock("LAP-01", invalid_quantity)

        repo.get_by_sku.assert_not_called()
        repo.save_stock.assert_not_called()

    @pytest.mark.parametrize("invalid_quantity", [True, False, 2.5, "3", None])
    def test_rejects_non_integer_quantity_without_touching_repository(
        self, invalid_quantity
    ):
        repo = Mock()
        service = InventoryService(repository=repo)

        with pytest.raises(InvalidQuantityError):
            service.decrease_stock("LAP-01", invalid_quantity)

        repo.get_by_sku.assert_not_called()
        repo.save_stock.assert_not_called()

    def test_raises_error_when_product_does_not_exist(self):
        repo = Mock()
        repo.get_by_sku.return_value = None

        service = InventoryService(repository=repo)

        with pytest.raises(ProductNotFoundError):
            service.decrease_stock("UNKNOWN-SKU", 1)

        repo.save_stock.assert_not_called()

    def test_raises_error_when_stock_is_insufficient(self):
        repo = Mock()
        repo.get_by_sku.return_value = Product(sku="MOU-02", name="Mouse", stock=2)

        service = InventoryService(repository=repo)

        with pytest.raises(InsufficientStockError):
            service.decrease_stock("MOU-02", 5)

        repo.save_stock.assert_not_called()

    def test_wraps_repository_failure_in_domain_error(self):
        repo = Mock()
        repo.get_by_sku.side_effect = ConnectionError("Fallo de conexión a la BD")

        service = InventoryService(repository=repo)

        with pytest.raises(ExternalDependencyError):
            service.decrease_stock("LAP-01", 1)
