from pathlib import Path

import httpx


def download_file(url: str, file_path: Path):
    with httpx.stream('GET', url, follow_redirects=True) as response:
        assert response.is_success, url
        tmp_file_path = file_path.with_suffix(f'{file_path.suffix}.download')
        with tmp_file_path.open('wb') as file:
            for chunk in response.iter_raw(1024):
                file.write(chunk)
        tmp_file_path.rename(file_path)
