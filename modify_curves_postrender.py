import os
import hou

#Get the rendered frame number and create file path
frame = int(hou.frame())
file_path = f"/tmp/hda_output_layer_{frame}.usda"

if os.path.exists(file_path):
	try:
		os.remove(file_path)
		print(f"Deleted: {file_path}")
	except Exception as e:
		print(f"Failed to delete {file_path}: {e}")
