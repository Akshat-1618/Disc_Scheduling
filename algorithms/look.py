# look.py
def look(requests, head):
    left = sorted([r for r in requests if r < head], reverse=True)
    right = sorted([r for r in requests if r >= head])
    # Move right, then reverse to serve left (no go-to-end)
    sequence = [head] + right + left
    seek = sum(abs(sequence[i] - sequence[i-1]) for i in range(1, len(sequence)))
    return sequence, seek
