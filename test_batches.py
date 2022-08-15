from typing import Tuple
from datetime import date

from model import Batch, OrderLine

def test_allocating_to_a_batch_reduces_the_available_quantity():
    batch = Batch("batch-001", "SMALL-TABLE", qty=20, eta=date.today())
    line = OrderLine("order-ref", "SMALL-TABLE", 2)

    batch.allocate(line)

    assert batch.available_quantity == 18


def make_batch_and_line(sku: str, batch_qty: int, line_qty) -> Tuple[Batch, OrderLine]:
    return ( Batch("batch-001", sku=sku, qty=batch_qty, eta=date.today()),
             OrderLine(orderid="order-123", sku=sku, qty=line_qty))


