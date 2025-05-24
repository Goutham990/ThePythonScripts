def logTransferReceiver(logReceiver, k):
    n = len(logReceiver)
    visited = {}  # Map from developer ID to the time (step) it was visited
    path = []     # The full path of developers visited in order
    current = 1   # Start with developer 1

    for step in range(k + 1):
        if current in visited:
            # Cycle detected
            cycle_start = visited[current]
            prefix = path[:cycle_start]
            cycle = path[cycle_start:]

            print("Cycle detected starting at index {}".format(cycle_start))
            print("Prefix path: {}".format(prefix))
            print("Cycle path: {}".format(cycle))

            if k < len(prefix):
                print("k={} is in prefix. Developer: {}".format(k, prefix[k]))
                return prefix[k]
            else:
                k -= len(prefix)
                result = cycle[k % len(cycle)]
                print("k={} in cycle. Developer: {}".format(k, result))
                return result

        visited[current] = len(path)
        path.append(current)

        # Debug
        print("Step {}: Developer {} transfers to {}".format(step, current, logReceiver[current - 1]))
        current = logReceiver[current - 1]

    # If k is small and no cycle was found (very rare), just return current
    print("No cycle detected. Developer after {} steps: {}".format(k, current))
    return current

