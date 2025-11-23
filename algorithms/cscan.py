# cscan.py
def cscan(requests, head, disk_size):
    left = sorted([r for r in requests if r < head])
    right = sorted([r for r in requests if r >= head])
    # Move right, jump to start, then serve left
    sequence = [head] + right + [disk_size - 1, 0] + left
    seek = sum(abs(sequence[i] - sequence[i-1]) for i in range(1, len(sequence)))
    return sequence, seek
