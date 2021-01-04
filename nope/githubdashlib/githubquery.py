## THIS CODE RELIES ON THE octohub GitHub interaction library

from .githubapi import get_issues, DEFAULT_PER_PAGE


class IssueQuery:
    """ Keyword args for init:

        labels: list
        state: str (should be "open" or "closed")
        page: int
        since: datetime
        direction: str ("asc" or "desc")
        sort: str ( TODO )
    """

    def __init__(self, conn, **kwargs):
        self.conn = conn

        self.labels = kwargs.get("labels", [])
        self.state = kwargs.get("state", None)
        self.page = kwargs.get("page", 1)
        self.since = kwargs.get("since", None) 
        self.direction = kwargs.get("direction", None)
        self.sort = kwargs.get("sort", None)
        self.per_page = kwargs.get("per_page", DEFAULT_PER_PAGE)

        self.last_query = None

    def load(self):
        "Use loaded parameters to send query to API; load self.issues."

        params = {"state": self.state,
                  "labels": ",".join(self.labels)}

        self.last_query = params
        self.issues = get_issues(self.conn, params, self.direction,
                          self.since, self.sort, self.per_page, self.page)

        #return get_issues(self.conn, params, self.direction,
        #                  self.since, self.sort, self.per_page, self.page)


    def next_page(self):
        "Increment page, query API, and load next list of Issues."
        self.page += 1
        self.load()

