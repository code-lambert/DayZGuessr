import os
from PIL import Image

# --- Config ---
input_path = "namalsk_full.png" 
output_base = "maps/namalsk"
target_zoom = 5
tile_size = 256

# 1. Load and prepare the background
img = Image.open(input_path).convert("RGBA")
# For Zoom 5, the total canvas must be 2^5 * 256 = 8192px
canvas_size = (2**target_zoom) * tile_size
canvas = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0)) # Transparent background

# 2. Paste Namalsk onto the canvas
canvas.paste(img, (0, 0))

# 3. Generate all zoom levels (0 to 5)
for z in range(target_zoom + 1):
    z_dir = os.path.join(output_base, str(z))
    os.makedirs(z_dir, exist_ok=True)
    
    # Calculate grid size for this zoom (e.g., Zoom 2 = 4x4 tiles)
    grid_count = 2**z
    current_canvas_size = grid_count * tile_size
    
    # Resize the master canvas for this specific zoom level
    resized_canvas = canvas.resize((current_canvas_size, current_canvas_size), Image.LANCZOS)
    
    for x in range(grid_count):
        x_dir = os.path.join(z_dir, str(x))
        os.makedirs(x_dir, exist_ok=True)
        
        for y in range(grid_count):
            left = x * tile_size
            top = y * tile_size
            right = left + tile_size
            bottom = top + tile_size
            
            tile = resized_canvas.crop((left, top, right, bottom))
            tile.save(os.path.join(x_dir, f"{y}.webp"), "WEBP", quality=80)
            
    print(f"Zoom {z} complete ({grid_count}x{grid_count} tiles)")

print("All zoom levels generated successfully!")
