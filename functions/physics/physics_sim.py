import numpy as np
import pycuda.driver as cuda
import pycuda.autoinit
from pycuda.compiler import SourceModule
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Define constants
a0 = 1.0  # Bohr radius (for hydrogen-like atom)
n = 1  # Principal quantum number
l = 0  # Azimuthal quantum number

# Create a 3D grid
size = 200
x = np.linspace(-10, 10, size)
y = np.linspace(-10, 10, size)
z = np.linspace(-10, 10, size)
x, y, z = np.meshgrid(x, y, z)

# Define the CUDA kernel for electron density calculation
mod = SourceModule(
    """
    __global__ void electron_density(float *x, float *y, float *z, float *density, float a0, int n, int l) {
        int idx = threadIdx.x + blockDim.x * blockIdx.x;
        int idy = threadIdx.y + blockDim.y * blockIdx.y;
        int idz = threadIdx.z + blockDim.z * blockIdx.z;
        int index = idx + idy * gridDim.x * blockDim.x + idz * gridDim.y * blockDim.y * blockDim.z;
        
        float r = sqrt(x[index] * x[index] + y[index] * y[index] + z[index] * z[index]);
        
        density[index] = pow((2 / (n * a0)) * (r / a0), l) * exp(-r / (n * a0)) / pow(n * a0, 2);
    }
"""
)

electron_density_kernel = mod.get_function("electron_density")

# Allocate GPU memory
density_gpu = np.zeros_like(x).astype(np.float32)
x_gpu = cuda.to_device(x.astype(np.float32))
y_gpu = cuda.to_device(y.astype(np.float32))
z_gpu = cuda.to_device(z.astype(np.float32))
density_gpu = cuda.to_device(density_gpu)

# Calculate electron density on GPU
block_size = (8, 8, 8)
grid_size = (size // block_size[0], size // block_size[1], size // block_size[2])

electron_density_kernel(
    x_gpu,
    y_gpu,
    z_gpu,
    density_gpu,
    np.float32(a0),
    np.int32(n),
    np.int32(l),
    block=block_size,
    grid=grid_size,
)

# Copy results back to CPU
cuda.memcpy_dtoh(density_gpu, density_gpu)

# Create a 3D plot of electron density
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection="3d")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")

ax.scatter(x, y, z, c=density_gpu, cmap="viridis", s=1)

plt.title(f"Electron Density (n={n}, l={l})")
plt.show()
