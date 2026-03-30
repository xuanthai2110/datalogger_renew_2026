import os

def master_fix():
    print("Starting master import fix...")
    root_dir = "backend"
    
    # Map of old prefixes to new unified prefixes
    # We want EVERYTHING to be absolute from the project root.
    replacements = {
        "from database ": "from backend.database ",
        "from database import": "from backend.database import",
        "from db_manager ": "from backend.database ",
        "from workers ": "from backend.workers ",
        "from services ": "from backend.services ",
        "from models ": "from backend.models ",
        "from schemas ": "from backend.models ", # Safety for old names
        "from core ": "from backend.core ",
        "from communication ": "from backend.communication ",
        "from drivers ": "from backend.drivers ",
        "from api ": "from backend.api ",
    }
    
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                # Skip __init__.py which use relative imports within package
                if file == "__init__.py":
                    continue
                    
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                new_content = content
                for old, new in replacements.items():
                    # Only replace if it doesn't already have the backend. prefix
                    # To avoid backend.backend.xxx
                    if old in new_content and f"backend.{old.split(' ')[1]}" not in new_content:
                        new_content = new_content.replace(old, new)
                
                if new_content != content:
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    print(f"Fixed: {path}")

if __name__ == "__main__":
    master_fix()
