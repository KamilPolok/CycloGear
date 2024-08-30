import os
import shutil
import subprocess
import sys

from cyclogear.config import APP_NAME, APP_ICON, DATA_PATH, RESOURCES_PATH, RESOURCES_DIR_NAME, DATA_DIR_NAME

def run_pyinstaller(app_name, icon_path, dist_path, spec_path, source_path):
    try:
        subprocess.run([
            'pyinstaller',
            '--name', app_name,
            '--icon', icon_path,
            '--noconsole',
            '--distpath', dist_path,
            '--specpath', spec_path,
            source_path
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error during PyInstaller execution: {e}")
        sys.exit(1)

def copy_directory(src, dest):
    try:
        if os.path.exists(dest):
            shutil.rmtree(dest)
        shutil.copytree(src, dest)
    except OSError as e:
        print(f"Error copying directory from {src} to {dest}: {e}")
        sys.exit(1)

def main():
    # Define paths
    app_name = APP_NAME
    icon_path = APP_ICON
    dist_path = os.path.abspath("./build/dist")
    spec_path = os.path.abspath("./build/spec")
    source_path = os.path.abspath("./cyclogear/main.py")
    
    # Run PyInstaller
    run_pyinstaller(app_name, icon_path, dist_path, spec_path, source_path)

    # Copy necessary folders to the distribution directory
    copy_directory(DATA_PATH, os.path.join(dist_path, app_name, DATA_DIR_NAME))
    copy_directory(RESOURCES_PATH, os.path.join(dist_path, app_name, RESOURCES_DIR_NAME))

if __name__ == "__main__":
    main()
