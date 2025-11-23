# clook.py
def clook(requests, head):
    left = sorted([r for r in requests if r < head])
    right = sorted([r for r in requests if r >= head])
    # Move right, then jump to lowest left and continue
    sequence = [head] + right + left
    seek = sum(abs(sequence[i] - sequence[i-1]) for i in range(1, len(sequence)))
    return sequence, seek
