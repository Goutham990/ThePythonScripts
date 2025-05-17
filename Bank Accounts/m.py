def max_stocks(n, prices, k):
    day_stock_info = [(prices[i], i + 1) for i in range(n)]
    day_stock_info.sort()

    total_stocks = 0

    for price, max_allowed in day_stock_info:
        can_buy = min(k // price, max_allowed)
        total_stocks += can_buy
        k -= can_buy * price
        if k <= 0:
            break

    return total_stocks

# Read all input at once
import sys
data = sys.stdin.read().split()

n = int(data[0])
prices = list(map(int, data[1:n+1]))
k = int(data[n+1])

print(max_stocks(n, prices, k))
