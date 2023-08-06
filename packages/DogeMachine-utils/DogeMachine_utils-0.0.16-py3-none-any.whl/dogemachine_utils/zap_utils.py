import platform
import os
import glob
import shutil


def clean_zap_dir(directory: str):
    """Remove extra ZAP files from the directory"""
    if platform.system() == "Darwin":
        results = glob.glob(os.path.join(directory, "*/"))
        print(results)
        for result in results:
            if os.path.isdir(result):
                # Any directories under this one are due to the shared volume, let's remove it
                shutil.rmtree(result)
        for file_pattern in ["*.xml", "*.properties", "*.html", "*.log", "*-template.yaml"]:
            results = glob.glob(os.path.join(directory, file_pattern))
            print(results)
            for result in results:
                if os.path.isfile(result):
                    os.remove(result)

