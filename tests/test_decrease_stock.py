from unittest.mock import Mock

import pytest

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
