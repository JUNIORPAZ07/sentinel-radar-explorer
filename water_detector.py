import numpy as np
import rasterio
import matplotlib.pyplot as plt

# 1. Load and Normalize the data again so this file has "context"
file_path = "bay_area_radar_matrix.tiff"
print(f"Opening {file_path} for water detection...")

with rasterio.open(file_path) as dataset:
    radar_matrix = dataset.read(1).astype(np.float32)

# Apply Log and Normalization
db_matrix = 10 * np.log10(radar_matrix + 1e-5)
matrix_min, matrix_max = np.min(db_matrix), np.max(db_matrix)
normalized_matrix = (db_matrix - matrix_min) / (matrix_max - matrix_min)

# Downsample so it doesn't crash
small_matrix = normalized_matrix[::5, ::5]

# 2. THE LOGIC: Water is dark (low backscatter)
# Thresholding: 1 if it's water (dark), 0 if it's land (bright)
water_mask = np.where(small_matrix < 0.15, 1, 0)

# 3. Visualize the comparison
print("Generating water mask visualization...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

ax1.imshow(small_matrix, cmap='magma')
ax1.set_title("Original Radar Matrix")
ax1.axis('off')

ax2.imshow(water_mask, cmap='Blues')
ax2.set_title("Detected Water (Binary Mask)")
ax2.axis('off')

plt.tight_layout()
plt.savefig("water_detection_final.png")
print("✅ Done! Open water_detection_final.png to see your AI's work.")