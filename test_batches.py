from typing import Tuple
from datetime import date

from model import Batch, OrderLine

def test_allocating_to_a_batch_reduces_the_available_quantity():
    batch = Batch("batch-001", "SMALL-TABLE", qty=20, eta=date.today())
    line = OrderLine("order-ref", "SMALL-TABLE", 2)

    batch.allocate(line)

    assert batch.available_quantity == 18


def make_batch_and_line(sku: str, batch_qty: int, line_qty: int) -> Tuple[Batch, OrderLine]:
    return ( Batch("batch-001", sku=sku, qty=batch_qty, eta=date.today()),
             OrderLine(orderid="order-123", sku=sku, qty=line_qty))

def test_can_allocate_if_available_quantity_greater_than_requred():
    large_batch, small_line = make_batch_and_line(sku="ELEGANT-LAMP", batch_qty=20, line_qty=2)
    assert large_batch.can_allocate(small_line)

def test_cannot_allocate_if_available_quantity_is_smaller_than_required():
    small_batch, large_line = make_batch_and_line(sku="ELEGANT-LAMP", batch_qty=2, line_qty=20)
    assert small_batch.can_allocate(large_line) is False

def test_can_allocate_if_quantity_available_is_equal_to_required():
    batch, line = make_batch_and_line(sku="ELEGANT-LAMP", batch_qty=2, line_qty=2)
    assert batch.can_allocate(line)


def test_cannot_allocate_if_skus_do_not_match():
    batch = Batch(ref="batch-001", sku="UNCOMFORTABLE-CHAIR", qty=100, eta=None)
    different_sku_line = OrderLine(orderid="order-123", sku="EXPENSIVE-TOASTER", qty=10)
    assert batch.can_allocate(different_sku_line) is False

def test_can_only_deallocate_allocated_lines():
    batch, unallocated_line = make_batch_and_line(sku="DECORATIVE-TRINKET",
            batch_qty=20, line_qty=2)
    batch.deallocate(unallocated_line)
    assert batch.available_quantity == 20

def test_allocation_is_idempotent():
    batch, line = make_batch_and_line(sku="ANGULAR-DESK", batch_qty=20,
            line_qty=2)
    batch.allocate(line)
    batch.allocate(line)
    assert batch.available_quantity == 18