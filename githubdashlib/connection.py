from github import Github

import os


GITHUB_API_KEY = os.environ["GITHUB_API_KEY"]

def get_connection(reponame):
    """
    Return connection object using full name of repo, e.g. 'streamlit/streamlit'.

    GITHUB_API_KEY must be set as environment variable.
    """
    # This GitHub token provides read-only access to public information.
    # We just need it to expand our API query rate.
    gh = Github(GITHUB_API_KEY)
    return gh.get_repo(reponame)



