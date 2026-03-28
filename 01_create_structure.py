from pathlib import Path

def create_directory_structure():
    """Create the complete IPDMA package directory structure."""
    
    directories = [
        "src/ipdma",
        "src/ipdma/engines",
        "src/ipdma/diagnostics",
        "src/ipdma/utils",
        "src/ipdma/cli",
        "tests",
        "docs",
        "examples",
        ".github/workflows",
        ".devcontainer"
    ]
    
    for dir_path in directories:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"✓ Created {dir_path}")
    
    # Create empty __init__.py files where needed
    init_files = [
        "src/ipdma/engines/__init__.py",
        "src/ipdma/diagnostics/__init__.py",
        "src/ipdma/utils/__init__.py",
        "src/ipdma/cli/__init__.py",
        "tests/__init__.py"
    ]
    
    for init_file in init_files:
        Path(init_file).touch()
        print(f"✓ Created {init_file}")
    
    print("\n✅ Directory structure created successfully!")

if __name__ == "__main__":
    create_directory_structure()