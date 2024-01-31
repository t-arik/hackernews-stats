import sys
import tarfile
import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('input_dir', type=Path, help='Contains all the \
                    directories with the scraped HTML pages')
parser.add_argument('output_dir', type=Path, help='The backup archives will \
                    be written to that direcotry')
parser.add_argument('-d', '--delete', action='store_true', help='Delete the \
                    scraped HTML pages after they have been archived')
args = parser.parse_args()
input_dir: Path = args.input_dir
output_dir: Path = args.output_dir

def stderr(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

if not input_dir.exists():
    stderr("direcory", input_dir, "does not exist")
    exit(1)
elif not input_dir.is_dir():
    stderr(input_dir, "is not a directory")
    exit(1)

if not output_dir.exists():
    output_dir.mkdir(parents=True)
elif not output_dir.is_dir():
    stderr(output_dir, "is not a directory")
    exit(1)

for scrape_dir in sorted(input_dir.iterdir()):
    files = [p for p in scrape_dir.iterdir() if p.is_file()]
    if not any([p for p in files if p.name == 'index.html']):
        stderr("warning:", scrape_dir, "does not contain an index.html file")
        continue
    elif len(files) != 31:
        stderr("warning:", scrape_dir, "does not contain expected 31 files")
        continue

    output_file = output_dir / (scrape_dir.name + '.tar.xz')
    if output_file.exists():
        stderr(output_file, "already exists")
        continue

    with tarfile.open(output_file, 'w:xz') as tar:
        tar.add(scrape_dir, arcname=scrape_dir.name)

    if args.delete:
        for file in files:
            file.unlink()
        scrape_dir.rmdir()

    print(output_file)
