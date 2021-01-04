from datetime import datetime


def _get_date(github_datetime):
    if github_datetime is not None:
        return datetime.strptime(github_datetime, "%Y-%m-%dT%H:%M:%SZ")


def _get_reactions(ghapi_reactions):
    """
    In [70]: iss2463.reactions
    Out[70]: 
    - url: https://api.github.com/repos/streamlit/streamlit/issues/2463/reactions
    - total_count: 0
    - +1: 0
    - -1: 0
    - laugh: 0
    - hooray: 0
    - confused: 0
    - heart: 0
    - rocket: 0
    - eyes: 0
    """


def _get_labels(ghapi_labels):
    out = []
    for item in ghapi_labels:
        out.append(item.name)
    return out


def _get_username(ghapi_user):
    return ghapi_user.login



class SimpleIssue:
    def __init__(ghapi_issue):
        self.url = ghapi_issue.url
        self.title = ghapi_issue.title
        self.number = ghapi_issue.number
        self.num_comments = ghapi_issue.comments
        self.labels = _get_labels(ghapi_issue.labels)
        self.state = ghapi_issue.state
        self.username = _get_username(ghapi_issue.user)
        self.body = ghapi_issue.body

        self.created_at = _get_date(ghapi_issue.created_at)
        self.closed_at = _get_date(ghapi_issue.closed_at)
        self.updated_at = _get_date(ghapi_issue.updated_at)

        #TODO
        #self.reactions = _get_reactions(ghapi_issue.reactions)
        #self.assignee = ghapi_issue.assignee
        #self.closed_by = ghapi_issue.closed_by


    def get_labels(self):
        out = []
        for item in self.labels:
            out.append(item)
        return out

    def to_dict(self):
        return {
            "title": self.title,
            "url": self.url,
            "number": self.number,
            "labels": self.labels,
            "username": self.username,
            "state": self.state,
            "num_comments": self.num_comments,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "closed_at": self.closed_at,
            #"closed_by": self.closed_by,
            #"assignee": self.assignee,
            #"reactions": self.reactions,
        }



