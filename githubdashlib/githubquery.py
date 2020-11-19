from .githubobjects import Issue

ISSUES_URI = "/repos/streamlit/streamlit/issues"

DEFAULT_PER_PAGE = 30


def get_issues(conn, params=None, direction=None, since=None,
                     sort=None, per_page=DEFAULT_PER_PAGE, page=1):
    issues = []
    uri = ISSUES_URI + "?per_page=%i" % per_page
    if since:
        uri += "&since=%s" % since
    if sort:
        uri += "&sort=%s" % sort
    if direction:
        uri += "&direction=%s" % direction

    uri += "&page=%i" % page
    response = conn.send("GET", uri,
                          params=params,
                        )
    for item in response.parsed:
        issues.append(Issue(**item))
    return issues



class IssueQuery:

    def __init__(self, conn, **kwargs):
        self.conn = conn

        self.labels = kwargs.get("labels", [])
        self.state = kwargs.get("state", None)
        self.page = kwargs.get("page", 1)
        self.since = kwargs.get("since", None) 
        self.direction = kwargs.get("direction", None)
        self.sort = kwargs.get("sort", None)

        self.last_query = None

    def load(self):
        "Use loaded parameters to send query to API; load self.issues."

        params = {"state": self.state,
                  "labels": ",".join(self.labels)}

        self.last_params = params
        self.issues = get_issues(self.conn, params, self.direction,
                          self.since, self.sort, self.per_page, self.page)

        #return get_issues(self.conn, params, self.direction,
        #                  self.since, self.sort, self.per_page, self.page)


    def next_page(self):
        "Increment page, query API, and load next list of Issues."
        self.page += 1
        self.load()



