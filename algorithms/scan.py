# scan.py
def scan(requests, head, disk_size):
    left = sorted([r for r in requests if r < head], reverse=True)
    right = sorted([r for r in requests if r >= head])
    # Move right first (towards end), then to end, then come back left
    sequence = [head] + right + [disk_size - 1] + left
    seek = sum(abs(sequence[i] - sequence[i-1]) for i in range(1, len(sequence)))
    return sequence, seek
