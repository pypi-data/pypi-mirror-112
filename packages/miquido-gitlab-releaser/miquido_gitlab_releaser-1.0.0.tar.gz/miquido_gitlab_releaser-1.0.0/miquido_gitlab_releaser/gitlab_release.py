import requests
import os
import sys


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def __post_body(tag_name: str, desc: str):
    return {
        "name": tag_name,
        "tag_name": tag_name,
        "description": desc
    }


def create_release(reader):
    desc = reader.read()

    gitlab_token = os.getenv('GITLAB_TOKEN')
    if gitlab_token is None:
        eprint('Missing GITLAB_TOKEN environment variable')
        exit(127)

    tag = os.getenv('CI_COMMIT_TAG')
    if tag is None:
        eprint('Missing CI_COMMIT_TAG environment variable. Must be run for tag')
        exit(127)

    headers = {'PRIVATE-TOKEN': gitlab_token}
    project_no = os.getenv('CI_PROJECT_ID')

    res = requests.post(f"https://gitlab.com/api/v4/projects/{project_no}/releases", headers=headers,
                        json=__post_body(tag, desc))
    if res.status_code >= 400:
        exit(1)


if __name__ == '__main__':
    create_release()
