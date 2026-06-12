import os

replacements = [
    ("Eidikos Global Events LLC", "Nebula Cybernetics Academy"),
    ("Eidikos Global Events", "Nebula Cybernetics Academy"),
    ("Eidikos", "Nebula"),
    ("eidikos", "nebula")
]

directories_to_check = [
    "d:\\Projects\\Edupro\\eidikos-flask-app\\app",
    "d:\\Projects\\Edupro\\eidikos-flask-app"
]

files_to_ignore = [
    "seed.py",
    "app.db",
    "replace_script.py"
]

def replace_in_file(filepath):
    if any(filepath.endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.gif', '.pyc', '.db', '.sqlite3']):
        return
        
    for ignore in files_to_ignore:
        if filepath.endswith(ignore):
            return

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        return

    original_content = content
    for old, new in replacements:
        content = content.replace(old, new)

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {filepath}")

for d in directories_to_check:
    for root, dirs, files in os.walk(d):
        if 'venv' in root or '.git' in root or '__pycache__' in root or 'migrations' in root:
            continue
        for file in files:
            replace_in_file(os.path.join(root, file))

print("Replacement complete.")
