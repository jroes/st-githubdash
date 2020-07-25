import time

import streamlit as st
import pandas as pd 

from octohub.connection import Connection

from githubdashlib import Label, Issue

TOKEN = "INSERT_TOKEN_HERE"
ISSUES_URI = "/repos/streamlit/streamlit/issues"
LABELS_URI = "/repos/streamlit/streamlit/labels"
ISSUES_PER_REQUEST = 100    # maximum allowed by GitHub API
MAXPAGE = 5



@st.cache
def get_connection():
    return Connection(TOKEN)


@st.cache
def get_labels(conn):
    labels = []
    #Set max return in page to the maximum allowed by GitHub API.
    uri = LABELS_URI + "?per_page=100"
    response = conn.send("GET", uri)
    for item in response.parsed:
        labels.append(Label(**item))
    return labels


def get_issues(conn, label_str, state="open", total=30, page=1):
    issues = []
    uri = ISSUES_URI + "?per_page=%i" % total
    #if page > 1:
    uri += "&page=%i" % page
    response = conn.send("GET", uri, 
                          params={"labels": label_str,
                                  "state": state,
                          },)
    for item in response.parsed:
        issues.append(Issue(**item))
    return issues


# -- SETUP --
conn = get_connection()
ALL_LABELS = {}
for label in get_labels(conn):
    ALL_LABELS[label.name] = label 


# -- SIDEBAR -- 


state = st.sidebar.radio("Issue state", ("open", "closed"))
st.sidebar.header("Filter by Labels")

label_checkboxes = dict(zip(ALL_LABELS.keys(), [False] * len(ALL_LABELS))) 

for name in ALL_LABELS.keys():
    label_checkboxes[name] = st.sidebar.checkbox(label=name)

selected_labels = [name for name in label_checkboxes.keys() if label_checkboxes[name]]


# -- ISSUE LIST --

current_page = st.slider(label="Page", min_value=1, max_value=20)
issues_per_page = st.slider(label="Issues per page", min_value=20,
                                max_value=100)

issues = get_issues(conn, ",".join(selected_labels), state, issues_per_page, current_page)

if selected_labels:
    label_str = " ".join([ALL_LABELS[label].html_name for label in selected_labels])
    st.write("%s (%i issues)" % (label_str, len(issues)), unsafe_allow_html=True)
else:
    st.header("All (%i issues)" % len(issues))

for issue in issues:
    issue_line = "<a href='{i.html_url}'>{i}</a>".format(i=issue)
    st.write(issue_line, unsafe_allow_html=True)
    for label in issue.labels:
        if label.name not in selected_labels:
            issue_line += " " + label.html_name
    if issue.closed_at:
        st.write("Time to close: %r" % issue.time_to_close)


