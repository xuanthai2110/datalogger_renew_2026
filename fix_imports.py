import os

def fix_files():
    root_dir = "backend"
    replacements = {
        "database.sqlite_manager": "database",
        "from database": "from database",
        "import database": "import database",
        "from schemas": "from models",
        "import schemas": "import models",
        "import config as app_config": "from core import config as app_config"
    }
    
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                new_content = content
                for old, new in replacements.items():
                    new_content = new_content.replace(old, new)
                
                if new_content != content:
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    print(f"Updated {path}")

if __name__ == "__main__":
    fix_files()
