import os

# Base is current directory (already inside movie-recommender)
base = "."

folders = [
    "data",
    "notebooks",
    "src",
]

files = [
    "notebooks/exploration.ipynb",
    "src/__init__.py",
    "src/preprocess.py",
    "src/vectorizer.py",
    "src/recommender.py",
    "main.py",
    "requirements.txt",
    "README.md",
]

# Create folders
for folder in folders:
    os.makedirs(folder, exist_ok=True)
    print(f"📁 Created folder: {folder}")

# Create empty files
for file in files:
    with open(file, "w") as f:
        pass
    print(f"📄 Created file: {file}")

print("\n✅ Project structure ready inside movie-recommender!")