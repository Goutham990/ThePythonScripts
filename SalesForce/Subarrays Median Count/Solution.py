from collections import defaultdict

def count_median_subarrays(n, efficiency, k):
    target = efficiency[k - 1]
    transformed = []

    for num in efficiency:
        if num > target:
            transformed.append(1)
        elif num < target:
            transformed.append(-1)
        else:
            transformed.append(0)

    prefix_balance = 0
    balance_counter = defaultdict(int)
    balance_counter[0] = 1

    result = 0
    found_target = False

    for i in range(n):
        if transformed[i] == 0:
            found_target = True

        if not found_target:
            prefix_balance += transformed[i]
            balance_counter[prefix_balance] += 1
        else:
            prefix_balance += transformed[i]
            result += balance_counter[prefix_balance]
            result += balance_counter[prefix_balance - 1]

    return result

# Example usage
efficiency = [5, 3, 1, 4, 7]
k = 4
print(count_median_subarrays(len(efficiency), efficiency, k))
