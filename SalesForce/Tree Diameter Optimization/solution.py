from collections import deque, defaultdict

def optimizeHierarchy(n, k, edges):
    if n == 1:
        return 0

    # Step 1: Build tree
    tree = defaultdict(list)
    degree = [0] * (n + 1)
    for u, v in edges:
        tree[u].append(v)
        tree[v].append(u)
        degree[u] += 1
        degree[v] += 1

    # Step 2: BFS Layer-wise Leaf Trimming
    removed = [False] * (n + 1)
    leaves = deque()
    for node in range(1, n + 1):
        if degree[node] == 1:
            leaves.append(node)
    
    remaining_nodes = n
    while k > 0 and leaves:
        leaf_count = len(leaves)
        if k < leaf_count:
            break  # Not enough operations to remove this full layer
        k -= leaf_count
        for _ in range(leaf_count):
            leaf = leaves.popleft()
            removed[leaf] = True
            remaining_nodes -= 1
            for neighbor in tree[leaf]:
                degree[neighbor] -= 1
                if degree[neighbor] == 1:
                    leaves.append(neighbor)

    # Step 3: Find diameter in remaining tree
    def bfs(start):
        visited = [-1] * (n + 1)
        q = deque()
        q.append(start)
        visited[start] = 0
        farthest_node = start
        while q:
            node = q.popleft()
            for neighbor in tree[node]:
                if visited[neighbor] == -1 and not removed[neighbor]:
                    visited[neighbor] = visited[node] + 1
                    q.append(neighbor)
                    if visited[neighbor] > visited[farthest_node]:
                        farthest_node = neighbor
        return farthest_node, visited[farthest_node]

    # Find a starting node that's not removed
    for i in range(1, n + 1):
        if not removed[i]:
            start = i
            break
    else:
        return 0  # All nodes removed

    far_node, _ = bfs(start)
    _, diameter = bfs(far_node)
    return diameter

