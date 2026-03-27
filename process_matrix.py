import numpy as np
import rasterio
import matplotlib.pyplot as plt

# 1. Open the raw scientific file
file_path = "bay_area_radar_matrix.tiff"
print(f"Opening {file_path}...")

with rasterio.open(file_path) as dataset:
    radar_matrix = dataset.read(1).astype(np.float32)

# 2. Apply Log Transformation (The Decibel Scale)
print("Applying Logarithmic Transformation...")
db_matrix = 10 * np.log10(radar_matrix + 1e-5)

# 3. AI PREP: Min-Max Normalization (Scaling to 0-1)
# This is the Calculus-based prep for a Neural Network
print("Normalizing matrix for AI readiness...")
matrix_min = np.min(db_matrix)
matrix_max = np.max(db_matrix)
normalized_matrix = (db_matrix - matrix_min) / (matrix_max - matrix_min)

# 4. Downsampling for performance (Slicing)
small_matrix = normalized_matrix[::5, ::5]

# 5. Save the final result
print("Rendering final Bay Area visualization...")
plt.figure(figsize=(12, 10))
# Using 'magma' or 'viridis' often looks cooler for radar than plain gray!
plt.imshow(small_matrix, cmap='magma') 
plt.title("Sentinel-1 SAR: Normalized Bay Area Matrix")
plt.colorbar(label="Normalized Intensity (0 to 1)")

output_file = "bay_area_final.png"
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"✅ Success! View your final data product at: {output_file}")