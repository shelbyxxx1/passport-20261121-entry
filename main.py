"""Ship the committed deterministic artwork byte-for-byte without rendering."""

import os
import shutil
from pathlib import Path


def clear_output_directory(output):
    for entry in output.iterdir():
        if entry.is_symlink() or not entry.is_dir():
            entry.unlink()
        else:
            shutil.rmtree(entry)


def main():
    source = Path(__file__).resolve().parent / 'entry.png'
    output = Path(os.environ.get('MAKEFUN_OUTPUT_DIR', '/output'))
    output.mkdir(parents=True, exist_ok=True)
    clear_output_directory(output)
    shutil.copyfile(source, output / 'entry.png')


if __name__ == '__main__':
    main()
