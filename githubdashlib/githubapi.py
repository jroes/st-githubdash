from .githubobjects import Label, Issue

ISSUES_URI = "/repos/streamlit/streamlit/issues"
LABELS_URI = "/repos/streamlit/streamlit/labels"


def get_labels(conn, per_page=30):
    labels = []
    # Set max return in page to the maximum allowed by GitHub API.
    uri = LABELS_URI + "?per_page=%i" % per_page
    response = conn.send("GET", uri)
    for item in response.parsed:
        labels.append(Label(**item))
    return labels


def get_issues(conn, params=None, direction=None, since=None, 
                     sort=None, per_page=30, page=1):
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


def get_all_the_issues(conn, state="open"):
    issues = []
    uri = ISSUES_URI + "?per_page=100&state=%s" % state

    page = 1
    more_issues = True
    while more_issues:
        uri += "&page=%i" % page
        response = conn.send("GET", uri, params={},)
        for item in response.parsed:
            issues.append(Issue(**item))
        if not len(issues) % 100:
            page += 1
        else:
            more_issues = False
    return issues


