from github import NamedUser
from github import ContentFile
from github import Repository
from github import RateLimitExceededException
from github import UnknownObjectException
from github import BadCredentialsException
from github import MainClass as GithubMainClass

from functools import wraps

def _get_attr_func(attr):
    """Returns a function which gets this attribute from an object."""

    def get_attr_func(obj):
        return getattr(obj, attr)
    return get_attr_func

def hash_repo(repo):
    st.warning(f"`hash_repo` -> `{repo._streamlit_hash}`")
    return repo._streamlit_hash

# This dictionary of hash functions allows you to safely intermix PyGithub
# with Streamit caching.
GITHUB_HASH_FUNCS = {
    GithubMainClass.Github: lambda _: None,
    NamedUser.NamedUser: _get_attr_func('login'),
    ContentFile.ContentFile: _get_attr_func('download_url'),
    Repository.Repository: hash_repo,
}

def rate_limit(limit_type: str):
    """Function decorator to try to handle Github search rate limits.
    See: https://developer.github.com/v3/search/#rate-limit

    limit_type: 'core' for regular API calls | 'search' for search calls
    """

    # Willing to wait up to an hour to lift the limits.
    MAX_WAIT_SECONDS = 60.0 * 60.0

    def rate_limit_decorator(func):
        @wraps(func)
        def wrapped_func(github, *args, **kwargs):
            try:
                return func(github, *args, **kwargs)
            except RateLimitExceededException:
                # We were rate limited by Github, Figure out how long to wait.
                # Round up, and wait that long.
                search_limit = getattr(github.get_rate_limit(), limit_type)
                remaining = search_limit.reset - datetime.utcnow()
                wait_seconds = math.ceil(remaining.total_seconds() + 1.0)
                wait_seconds = min(wait_seconds, MAX_WAIT_SECONDS)
                # with st.spinner(f'Waiting {wait_seconds}s to avoid {limit_type} rate limit.'):
                #    time.sleep(wait_seconds)
                print(f"Waiting {wait_seconds}s to avoid GitHub {limit_type} API limit.")
                return func(github, *args, **kwargs)
        return wrapped_func
    return rate_limit_decorator


