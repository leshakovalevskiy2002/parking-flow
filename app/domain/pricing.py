from datetime import datetime
from decimal import Decimal
from math import ceil


def calculate_cost(
    start_time: datetime, end_time: datetime, price_per_hour: Decimal, minimum_charge: Decimal
) -> Decimal:
    interval_in_seconds = int((end_time - start_time).total_seconds())
    hours_to_pay = ceil(interval_in_seconds / 3600)
    return max(hours_to_pay * price_per_hour, minimum_charge)
