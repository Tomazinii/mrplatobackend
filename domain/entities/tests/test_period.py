
import datetime
import pytest
from domain.entities.objectValue import Period
from datetime import date

pytestmark = pytest.mark.unit

def test_period_valid():
    value_date = date(2000,5,30)
    start = value_date
    end = value_date

    obj: Period = Period.create_period(start=start, end=end)

    assert obj.get_period()["start"] == start
    assert obj.get_period()["end"] == end
    