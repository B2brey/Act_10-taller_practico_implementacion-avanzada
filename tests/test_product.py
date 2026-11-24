from unittest.mock import Mock

import pytest

from source.inventory.exceptions import InsufficientStockError
from source.inventory.models import Product
from source.inventory.service import InventoryService


class TestProduct:
    def test_min_stock_defaults_to_zero(self):
        product = Product(sku="LAP-01", name="Laptop", stock=10)

        assert product.min_stock == 0


class TestMinStockRequirement:
    def test_decrease_rejects_when_result_falls_below_min_stock(self):
        repo = Mock()
        repo.get_by_sku.return_value = Product(
            sku="LAP-01", name="Laptop", stock=10, min_stock=5
        )

        service = InventoryService(repository=repo)

        with pytest.raises(InsufficientStockError):
            service.decrease_stock("LAP-01", 6)

        repo.save_stock.assert_not_called()

    def test_decrease_allows_reaching_exactly_min_stock(self):
        repo = Mock()
        repo.get_by_sku.return_value = Product(
            sku="LAP-01", name="Laptop", stock=10, min_stock=5
        )

        service = InventoryService(repository=repo)

        assert service.decrease_stock("LAP-01", 5) == 5
        repo.save_stock.assert_called_once_with("LAP-01", 5)

    def test_increase_is_not_restricted_by_min_stock(self):
        repo = Mock()
        repo.get_by_sku.return_value = Product(
            sku="LAP-01", name="Laptop", stock=1, min_stock=5
        )

        service = InventoryService(repository=repo)

        assert service.increase_stock("LAP-01", 2) == 3
        repo.save_stock.assert_called_once_with("LAP-01", 3)
