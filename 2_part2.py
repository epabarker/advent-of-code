import time

# Load data
with open('2-input.txt', 'r') as f: 
    ranges = f.read().strip().split(',')

# Part 1
print("=" * 50)
print("PART 1")
print("=" * 50)
start_time = time.time()

total = 0
for r in ranges:
    seq_len = 0
    lower, upper = r.split('-')
    if len(lower) % 2 == 0: 
        seq_len = (len(lower) // 2)
    elif len(upper) % 2 == 0: 
        seq_len = (len(upper) // 2)
    if seq_len == 0: 
        continue
    
    min_n_digit = 10**(2*seq_len - 1)
    max_n_digit = (10**(2*seq_len)) - 1
    
    start = max(int(lower), min_n_digit)
    end = min(int(upper), max_n_digit)
    
    first_seq = str(start)[0:seq_len]
    last_seq = str(end)[0:seq_len]
    
    for seq in range(int(first_seq), int(last_seq) + 1):
        id = int(str(seq)*2)
        if id in range(start, end + 1):
            total += id

end_time = time.time()
print(f"Total Sum: {total}")
print(f"Execution time: {(end_time - start_time):.4f} seconds")

# Part 2
print("\n" + "=" * 50)
print("PART 2")
print("=" * 50)
start_time = time.time()

range_tuples = [tuple(r.split('-')) for r in ranges]
standard_ranges = []
for lower, upper in range_tuples:
    if len(upper) != len(lower):
        mid = 10**(len(upper)-1)
        standard_ranges.append((lower, str(mid-1)))
        standard_ranges.append((str(mid), upper))
    else:
        standard_ranges.append((lower, upper))
        
invalid_ids = set()
for lower, upper in standard_ranges:
    divisors = [i for i in range(1, (len(lower)//2 + 1)) if len(lower) % i == 0]
    for d in divisors:
        start = lower[:d]
        repeat = int(start)
        id = str(repeat)*int(len(upper)/int(d))
        while int(id) <= int(upper):
            if int(id) >= int(lower):
                invalid_ids.add(id)
            repeat += 1
            id = str(repeat)*int(len(lower)/int(d))
            
invalid_ids_list = [int(id) for id in invalid_ids]
total = sum(invalid_ids_list)

end_time = time.time()
print(f"Total: {total}")
print(f"Execution time: {(end_time - start_time):.4f} seconds")

# Part 2 - Optimized
print("\n" + "=" * 50)
print("PART 2 - OPTIMIZED (3D Chess brain)")
print("=" * 50)
start_time = time.time()


from math import ceil, floor

def rep_multiplier(d, r):
    return (10 ** (d * r) - 1) // (10 ** d - 1)

def min_max_base_for_range(R_start, R_end, r, d):
    M = rep_multiplier(d, r)
    a_min = max(ceil(R_start / M), 10 ** (d - 1))
    a_max = min(floor(R_end / M), 10 ** d - 1)
    return a_min, a_max

def sum_repeated_range(a_start, a_end, r, d):
    M = rep_multiplier(d, r)
    total_a = (a_end * (a_end + 1) - (a_start - 1) * a_start) // 2
    return M * total_a

with open('2-input.txt', 'r') as f:
    ranges = f.read().strip().split(',')

range_tuples = [tuple(r.split('-')) for r in ranges]
standard_ranges = []
for lower, upper in range_tuples:
    if len(upper) != len(lower):
        mid = 10 ** (len(upper) - 1)
        standard_ranges.append((lower, str(mid - 1)))
        standard_ranges.append((str(mid), upper))
    else:
        standard_ranges.append((lower, upper))

total_sum = 0

for lower, upper in standard_ranges:
    L = len(lower)
    R_start, R_end = int(lower), int(upper)
    divisors = [d for d in range(1, (L // 2) + 1) if L % d == 0]
    all_sum = {}
    for d in divisors:
        r = L // d
        a_min, a_max = min_max_base_for_range(R_start, R_end, r, d)
        all_sum[d] = sum_repeated_range(a_min, a_max, r, d)
    primitive_sum = {}
    for d in sorted(divisors):
        s = all_sum[d]
        for q in primitive_sum:
            if d % q == 0:
                s -= primitive_sum[q]
        primitive_sum[d] = s
    total_sum += sum(primitive_sum.values())


end_time = time.time()
print(f"Total: {total_sum}")
print(f"Execution time: {(end_time - start_time):.4f} seconds")
