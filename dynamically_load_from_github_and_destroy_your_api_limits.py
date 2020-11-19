import streamlit as st
import pandas as pd
from github import Github

from datetime import datetime


# FAILED ITERATION BECAUSE I CAN'T EVEN GET CACHE TO LOAD. Not even 1 time.

def initialize(reponame):
    # This GitHub token provides read-only access to public information.
    # We just need it to expand our API query rate.
    gh = Github("[redacted]")
    return gh.get_repo(reponame)


@st.cache(suppress_st_warning=True)
def get_all_issues_and_PRs(reponame="streamlit/streamlit"):
    st.write("Downloading issues from %s" % reponame)
    st.write("(This will take 1-2 minutes, hang tight.)")
    repo = initialize(reponame)
    everything = repo.get_issues(state="all")

    issues = []
    prs = []

    for issue in everything:
        if issue.pull_request:
            prs.append(issue)
        else:
            issues.append(issue)

    return (issues, prs)



ALL_ISSUES, ALL_PRS = get_all_issues_and_PRs()

def get_date(github_datetime):
    if github_datetime is not None:
        return datetime.strptime(github_datetime, "%Y-%m-%dT%H:%M:%SZ")

class SimpleIssue:
    def __init__(self, **kwargs):
        self.__dict__ = kwargs

    def get_labels(self):
        out = ""
        for label in self.labels:
            out += label["name"]
        return out

    def get_creator(self):
        return self.user["login"]

    def to_dict(self):
        return {
            "title": self.title,
            "url": self.url,
            "number": self.number,
            "labels": self.get_labels(),
            "creator": self.get_creator(),
            "state": self.state,
            "assigned": self.assignee,
            "num_comments": self.comments,
            "created_at": get_date(self.created_at),
            "updated_at": get_date(self.updated_at),
            "closed_at": get_date(self.closed_at),
            "closed_by": self.closed_by,
        }



}
pr_dict = {}


st.write("Total issues: %i" % len(ALL_ISSUES))
st.write("Total PRs: %i" % len(ALL_PRS))


