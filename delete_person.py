import pickle
import numpy as np

# Load data
with open('data/names.pkl', 'rb') as f:
    names = pickle.load(f)

with open('data/faces_data.pkl', 'rb') as f:
    faces = pickle.load(f)

# Convert to numpy (if not already)
names = np.array(names)
faces = np.array(faces)

# Person to delete
person_to_delete = "shubham"

# Find indexes where name is NOT 'modi'
mask = names != person_to_delete

# Filter data
new_names = names[mask]
new_faces = faces[mask]

# Save back
with open('data/names.pkl', 'wb') as f:
    pickle.dump(list(new_names), f)

with open('data/faces_data.pkl', 'wb') as f:
    pickle.dump(new_faces, f)

print(f"[DONE] Removed '{person_to_delete}' successfully!")
print("Remaining people:", set(new_names))