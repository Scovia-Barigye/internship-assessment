from typing import List


def collatz(n: int) -> List[int]:
    
    result = [n]
    while n != 1:
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
        result.append(n)
    return result


def distinct_numbers(numbers: List[int]) -> int:
    
    return len(set(numbers))
