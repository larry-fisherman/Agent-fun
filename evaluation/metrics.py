def total_return(values: list[float]) -> float:
    return (values[-1] - values[0]) / values[0] * 100

def max_drawdown(values: list[float]) -> float:
    peak = values[0]
    worst = 0.0
    for v in values:
        if v > peak:
            peak = v
        drop = (v - peak) / peak * 100
        if drop < worst:
            worst = drop
    return worst


if __name__ == "__main__":
    test = [100, 120, 90, 130, 104]
    print(total_return(test))   # should be 4.0
    print(max_drawdown(test))   # should be -25.0
