# bankers.py
import numpy as np

def is_safe_state(allocation, maximum, available):
    """Check if the system is in a safe state using Banker's Algorithm 
    """
    allocation = np.array(allocation, dtype=int)
    maximum = np.array(maximum, dtype=int)
    available = np.array(available, dtype=int)
    P, R = allocation.shape
    need = maximum - allocation
    finish = [False] * P
    work = available.copy()
    safe_seq = []

    while len(safe_seq) < P:
        progressed = False
        for i in range(P):
            if not finish[i]:
                if np.all(need[i] <= work):
                    # this process can finish
                    work += allocation[i]
                    finish[i] = True
                    safe_seq.append(i)
                    progressed = True
        if not progressed:
            # no process could proceed -> unsafe
            return False, []
    return True, safe_seq
