import yaml
import os
import shutil

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))

# Reads yaml from file by given path
def load_yaml(path : str) -> dict:
    """Loads yaml conig from given file"""
    try:
        with open(path, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: Configuration file '{path}' not found.")
        return None
    except yaml.YAMLError as e:
        print(f"Error: Invalid YAML in configuration file: {e}")
        return None

def copy_file(source_file : str, target_dir : str):
    """Copies suorce_file to target_dir"""
    if not os.path.exists(target_dir):
        os.makedirs(target_dir, exist_ok=True)
    dest: str = os.path.join(target_dir, os.path.basename(source_file))
    shutil.copy(source_file, dest)
