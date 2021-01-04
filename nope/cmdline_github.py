from githubdashlib import get_connection

from github import Github

conn = get_connection("streamlit/streamlit")



def acquire(conn, labels=[], assignee="", state="open", creator=None):
    issues = conn.get_issues(labels=labels,
                             assignee=assignee,
                             state=state,
                             creator=creator
                            )
    print("Total %s issues+PRs: %i" % (params['state'], issues.totalCount))
    return issues



open_issues = acquire(conn, labels=["media"], state="open")
closed_issues = acquire(conn, labels=["media"], state="closed")


