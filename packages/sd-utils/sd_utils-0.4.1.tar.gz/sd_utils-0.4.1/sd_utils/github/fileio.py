"""
API for accessing files from github
"""
from github import Github
from github.Repository import Repository
from github.ContentFile import ContentFile


def get_file(owner: str, repo: str, file_path: str, token: str = "") -> str:
    """
    Gets a file from a repo
    
    Args:
        owner (str): the owner of the repo
        repo (str): the name of the repo
        file_path (str): the path of the file relative to 
            the root of the repo
        token (str): the github token used to authenticate. 
            failure to provide one can result in rate limits
            or no access to a private repo
    """

    g = Github() if token == "" else Github(token)
    repo: Repository = g.get_repo(f"{owner}/{repo}")
    response: ContentFile = repo.get_contents(file_path)
    return str(response.decoded_content, "utf-8")
