import time
import os

import streamlit as st
import pandas as pd

from octohub.connection import Connection

from githubdashlib import Label, Issue
from githubdashlib import get_labels as _get_labels
from githubdashlib import IssueQuery


TOKEN = os.environ.get("GITHUB_API_TOKEN", None)
ISSUES_URI = "/repos/streamlit/streamlit/issues"
LABELS_URI = "/repos/streamlit/streamlit/labels"
ISSUES_PER_REQUEST = 100    # maximum allowed by GitHub API
MAXPAGE = 5


@st.cache
def get_connection():
    return Connection(TOKEN)


@st.cache
def get_labels(conn):
    return _get_labels(conn, per_page=100)



# -- SETUP --
conn = get_connection()
ALL_LABELS = {}
for label in get_labels(conn):
    ALL_LABELS[label.name] = label


# -- SIDEBAR -- 
option = st.sidebar.selectbox(
        "Things you can do",
        ('Issues by label', 
         'Charts and graphs',
         'Dubious Awards!',
        ))



# Menu selector
if option == "Charts and graphs":
    st.sidebar.header("Pie charts!")
    st.header("Coming soon...")
    st.markdown("""
            * How are we doing on time-to-first-answer on GitHub issues?
            * How quickly are we closing bugs? What kinds of bugs are we slow at?
            * FIRST POST!!!11one:: who's gotten 'first comment' most often?
            * PRs per month
            * PR size (lines of code) over time
            * Times issue has been reopened
            * Issues closed (and how long it took) per issue type, per month
        """)

elif option == "Issues by interactivity":
    st.sidebar.header("Issues by interactivity")
    st.header("Coming soon!")


elif option == "Issues by label":

    query = IssueQuery(conn)
    query.per_page = st.sidebar.slider(label="Issues per page", min_value=20,
                                          max_value=100)
    query.page = 1

    st.sidebar.header("Filter by Labels")

    #selected_labels = st.sidebar.multiselect(label="Labels",
    #                        options=list(ALL_LABELS.keys()),
    #                        )

    label_checkboxes = dict(zip(ALL_LABELS.keys(), [False] * len(ALL_LABELS))) 

    for name in ALL_LABELS.keys():
        label_checkboxes[name] = st.sidebar.checkbox(label=name)

    query.labels = [name for name in label_checkboxes.keys() if label_checkboxes[name]]


    # -- ISSUE LIST --

    query.state = st.radio("Issue state", ("open", "closed"))
    query.load()

    if query.labels:
        label_str = " ".join([ALL_LABELS[label].html_name for label in query.labels])
        st.write("%s (%i issues)" % (label_str, len(query.issues)), unsafe_allow_html=True)
    else:
        st.header("All (%i issues)" % len(query.issues))

    for issue in query.issues:
        issue_line = "<a href='{i.html_url}'>{i}</a>".format(i=issue)
        st.write(issue_line, unsafe_allow_html=True)
        for label in issue.labels:
            try:
                if label.name not in query.labels:
                    issue_line += " " + label.html_name
            except AttributeError:
                issue_line += label
        if issue.closed_at:
            st.write("Time to close: %r" % issue.time_to_close)


