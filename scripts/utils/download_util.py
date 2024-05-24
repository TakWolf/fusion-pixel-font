from pathlib import Path

import requests


def download_file(url: str, file_path: Path):
    response = requests.get(url, stream=True)
    assert response.ok, url
    tmp_file_path = file_path.with_suffix(f'{file_path.suffix}.download')
    with tmp_file_path.open('wb') as file:
        for chunk in response.iter_content(chunk_size=512):
            if chunk is not None:
                file.write(chunk)
    tmp_file_path.rename(file_path)
