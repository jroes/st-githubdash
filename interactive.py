import time
import os

import streamlit as st
import pandas as pd

from octohub.connection import Connection

from githubdashlib import Label, Issue
from githubdashlib import get_labels as _get_labels
from githubdashlib import get_issues as _get_issues
from githubdashlib import get_all_the_issues as _get_all_the_issues 


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

@st.cache
def get_all_open_issues(conn):
    return _get_all_the_issues(conn, "open")

@st.cache
def get_all_closed_issues(conn):
    return _get_all_the_issues(conn, "closed")
    

# -- SETUP --
conn = get_connection()
ALL_LABELS = {}
for label in get_labels(conn):
    ALL_LABELS[label.name] = label


st.sidebar.header("Pie charts!")
st.sidebar.markdown("* How are we doing on time-to-first-answer on GitHub issues?")
st.sidebar.markdown("* How quickly are we closing bugs? What kinds of bugs are we slow at?")
st.sidebar.markdown("* Issues by interactivity...") 


open_issues = get_all_open_issues(conn)
closed_issues = get_all_closed_issues(conn)

st.write("Number of issues: %i" % len(issues))

