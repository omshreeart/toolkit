"""Build the exact, verified HERO static release for GitHub Pages."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path, PurePosixPath
from urllib.parse import quote
from urllib.request import Request, urlopen
import hashlib
import json

manifest = json.loads(Path('site-manifest.json').read_text())
source = manifest['source'].rstrip('/') + '/'
if not source.startswith('https://'):
    raise ValueError('The release source must use HTTPS.')
output = Path('_site')
output.mkdir(exist_ok=True)


def fetch_file(item):
    relative = PurePosixPath(item['path'])
    if relative.is_absolute() or '..' in relative.parts:
        raise ValueError('Unsafe release path.')
    target = output.joinpath(*relative.parts)
    target.parent.mkdir(parents=True, exist_ok=True)
    request = Request(source + quote(relative.as_posix(), safe='/'),
                      headers={'User-Agent': 'HERO-Static-Publisher/1.0'})
    digest = hashlib.sha256()
    size = 0
    temporary = target.with_name(target.name + '.download')
    with urlopen(request, timeout=60) as response, temporary.open('wb') as stream:
        while chunk := response.read(1024 * 1024):
            size += len(chunk)
            digest.update(chunk)
            stream.write(chunk)
    if size != item['size'] or digest.hexdigest() != item['sha256']:
        temporary.unlink(missing_ok=True)
        raise ValueError(f'Release verification failed: {relative}')
    temporary.replace(target)
    return relative.as_posix()


with ThreadPoolExecutor(max_workers=8) as workers:
    futures = [workers.submit(fetch_file, item) for item in manifest['files']]
    for completed, future in enumerate(as_completed(futures), 1):
        future.result()
        if completed % 25 == 0:
            print(f'Verified {completed}/{len(futures)} release files', flush=True)

(output / '.nojekyll').write_text('')
if not (output / 'index.html').is_file():
    raise ValueError('The release is missing index.html.')
print(f'HERO is ready: {len(manifest["files"])} verified static files.', flush=True)
