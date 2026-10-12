def discounted_cents(cents: int, percent: int) -> int:
    return cents * (100 - percent) // 100
