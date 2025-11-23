# fcfs.py
def fcfs(requests, head):
    sequence = [head] + requests[:]  # head then in-order requests
    seek = sum(abs(sequence[i] - sequence[i-1]) for i in range(1, len(sequence)))
    return sequence, seek
