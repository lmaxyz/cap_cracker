import pathlib
import yaml

_APP_DIR = pathlib.Path(__file__).parent
BASE_DIR = _APP_DIR.parent
config_path = _APP_DIR / "config" / "app.yaml"

CAP_FILES_STORAGE = BASE_DIR / "cap_files"

if not CAP_FILES_STORAGE.exists():
    CAP_FILES_STORAGE.mkdir(parents=True)


def get_config(path):
    with open(path) as f:
        cfg = yaml.safe_load(f)
    return cfg


config = get_config(config_path)

STATIC_DIR = BASE_DIR / "static"
