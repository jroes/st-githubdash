

def get_all_issues_and_PRs(conn):
    print("downloading EVERYTHING from repo, this may take a bit...")
    everything = conn.get_issues(state="all")

    issues = []
    prs = []

    for issue in everything:
        if issue.pull_request:
            prs.append(issue)
        else:
            issues.append(issue)

    return (issues, prs)


#def get_issues(conn, params):


