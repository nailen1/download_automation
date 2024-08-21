import os

def print_directory_structure(root_dir, prefix='', ignore_dirs=None):
    if ignore_dirs is None:
        ignore_dirs = ['.git', '__pycache__', '.ipynb_checkpoints']
    
    # Print the root directory name only
    print(os.path.basename(root_dir) + '/')
    
    def print_directory(path, prefix=''):
        contents = sorted(os.listdir(path))
        contents = [c for c in contents if c not in ignore_dirs]
        
        for index, item in enumerate(contents, start=1):
            is_last = index == len(contents)
            is_hidden = item.startswith('.')
            full_path = os.path.join(path, item)
            is_dir = os.path.isdir(full_path)
            
            if is_last:
                if is_hidden:
                    marker = '└··'
                else:
                    marker = '└──'
                next_prefix = prefix + '    '
            else:
                if is_hidden:
                    marker = '├··'
                else:
                    marker = '├──'
                next_prefix = prefix + '│   '
            
            # Add '/' to directory names
            if is_dir:
                item += '/'
            
            print(f"{prefix}{marker} {item}")
            
            if is_dir and item not in ignore_dirs:
                try:
                    print_directory(full_path, next_prefix)
                except PermissionError:
                    print(f"{next_prefix}[Permission Denied]")
                except Exception as e:
                    print(f"{next_prefix}[Error: {str(e)}]")
    
    print_directory(root_dir)

# Usage
print_directory_structure('./')