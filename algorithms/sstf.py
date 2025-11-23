# sstf.py
def sstf(requests, head):
    reqs = requests.copy()
    sequence = [head]
    cur = head
    while reqs:
        nearest = min(reqs, key=lambda x: abs(x - cur))
        sequence.append(nearest)
        reqs.remove(nearest)
        cur = nearest
    seek = sum(abs(sequence[i] - sequence[i-1]) for i in range(1, len(sequence)))
    return sequence, seek
