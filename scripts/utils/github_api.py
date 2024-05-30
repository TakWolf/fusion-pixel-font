import httpx

_BASE_URL = 'https://api.github.com'


def get_releases_latest_tag_name(repository_name: str) -> str:
    url = f'{_BASE_URL}/repos/{repository_name}/releases/latest'
    response = httpx.get(url, follow_redirects=True)
    assert response.is_success, url
    return response.json()['tag_name']


def get_tag_sha(repository_name: str, tag_name: str) -> str:
    url = f'{_BASE_URL}/repos/{repository_name}/tags'
    response = httpx.get(url, follow_redirects=True)
    assert response.is_success, url
    tag_infos = response.json()
    for tag_info in tag_infos:
        if tag_info['name'] == tag_name:
            return tag_info['commit']['sha']
    raise Exception(f"Tag info not found: '{tag_name}'")


def get_branch_latest_commit_sha(repository_name: str, branch_name: str) -> str:
    url = f'{_BASE_URL}/repos/{repository_name}/branches/{branch_name}'
    response = httpx.get(url, follow_redirects=True)
    assert response.is_success, url
    return response.json()['commit']['sha']
