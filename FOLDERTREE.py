import os

def print_directory_tree(startpath):
    excluded_dirs = {'.git', '.idea', '__pycache__', 'venv'}
    for root, dirs, files in os.walk(startpath, topdown=True):
        # Modify dirs in-place to skip specific directories
        dirs[:] = [d for d in dirs if d not in excluded_dirs]
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        # Print the root directory with appropriate tree branching
        if level == 0:
            print(f"{os.path.basename(root)}/")
        else:
            print(f"{indent}├── {os.path.basename(root)}")
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print(f"{subindent}└── {f}")

# Use the current working directory as the starting path
print_directory_tree(os.getcwd())
