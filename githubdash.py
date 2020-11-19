import streamlit as st
import pandas as pd
from github import Github

from datetime import datetime


def initialize(reponame):
    # This GitHub token provides read-only access to public information.
    # We just need it to expand our API query rate.
    gh = Github("d15cbe887b2fde45ea9a057d6c0e2c37c5d8449a")
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

def get_date(github_datetime):
    return datetime.strptime(github_datetime, "%Y-%m-%dT%H:%M:%SZ")


ALL_ISSUES, ALL_PRS = get_all_issues_and_PRs()

class SimpleIssue:
    def __init__(**kwargs):
        self.__dict__ = kwargs

    def get_labels(self):
        

    def to_dict(self):
        return {
            "title": self.title,
            "url": self.url,
            "number": self.number,
            "labels": self.get_labels(),
            "username": self.get_username(),
            "state": self.state,
            "assigned": self.assignee,
            "num_comments": self.comments,
            "created_at": self.get_date(self.created_at),
            "updated_at": self.get_date(self.updated_at),
            "closed_at": self.get_date(self.closed_at),
            "closed_by": self.closed_by,
        }



}
pr_dict = {}


st.write("Total issues: %i" % len(ALL_ISSUES))
st.write("Total PRs: %i" % len(ALL_PRS))


