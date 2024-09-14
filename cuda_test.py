from numba import cuda, float64
import numpy as np
from timeit import default_timer as timer

# Normal function to run on CPU
def func(a):
    for i in range(a.size):
        a[i] += 1

from numba import cuda

print("CUDA Version:", cuda.runtime.get_version())

# Function optimized to run on GPU
@cuda.jit
def func2(a):
    # Get the thread's absolute position within the grid
    i = cuda.grid(1)
    # Check if the thread is within the bounds of the array
    if i < a.size:
        a[i] += 1

if __name__ == "__main__":
    n = 10000000
    a = np.ones(n, dtype=np.float64)
    a_device = cuda.to_device(a)

    # Measure time for CPU execution
    start = timer()
    func(a)
    print("without GPU:", timer() - start)

    # Measure time for GPU execution
    start = timer()
    # Define the number of threads per block and number of blocks per grid
    threads_per_block = 256
    blocks_per_grid = (a.size + (threads_per_block - 1)) // threads_per_block
    func2[blocks_per_grid, threads_per_block](a_device)
    a_device.copy_to_host(a)  # Copy the result back to host
    print("with GPU:", timer() - start)
