import time
import os

import streamlit as st
import pandas as pd 

from octohub.connection import Connection

from githubdashlib import Label, Issue 
from githubdashlib import get_labels as _get_labels
from githubdashlib import get_issues as _get_issues
from githubdashlib import get_all_events as _get_events


TOKEN = os.environ.get("GITHUB_API_TOKEN", None)
ISSUES_PER_REQUEST = 100    # maximum allowed by GitHub API
MAXPAGE = 5


@st.cache
def get_connection():
    return Connection(TOKEN)

CONN = get_connection()

@st.cache(allow_output_mutation=True)
def get_labels():
    return _get_labels(CONN, per_page=100)


def get_issues(params, per_page=30, page=1):
    return _get_issues(CONN, params, per_page=per_page, page=page)


# -- SETUP --

_all_labels = get_labels()

ALL_LABELS = {}
for label in _all_labels:
    ALL_LABELS[label.name] = label 


# -- SIDEBAR -- 
state = st.sidebar.radio("Issue state", ("open", "closed"))
st.sidebar.header("Filter by Labels")

label_checkboxes = dict(zip(ALL_LABELS.keys(), [False] * len(ALL_LABELS))) 

for name in ALL_LABELS.keys():
    try:
        label_checkboxes[name] = st.sidebar.checkbox(label=name)
    except TypeError:
        pass

selected_labels = [name for name in label_checkboxes.keys() if label_checkboxes[name]]


# -- ISSUE LIST --
issues_per_page = st.slider(label="Issues per page", min_value=20,
                                max_value=100)
current_page = st.number_input(label="Page", min_value=1)

params = {"state": state,
          "labels": ",".join(selected_labels)}
issues = get_issues(params, per_page=issues_per_page, page=current_page)

if selected_labels:
    label_str = " ".join([ALL_LABELS[label].html_name for label in selected_labels])
    st.write("%s (%i issues)" % (label_str, len(issues)), unsafe_allow_html=True)
else:
    st.header("All (%i issues)" % len(issues))

for issue in issues:
    issue_line = "<a href='{i.html_url}'>{i}</a>".format(i=issue)
    for label in issue.labels.values():
        if label.name not in selected_labels:
            issue_line += " " + label.html_name
    st.write(issue_line, unsafe_allow_html=True)
    if issue.closed_at:
        st.write("Time to close: %r" % issue.time_to_close)


