import time
import os

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from octohub.connection import Connection

from githubdashlib import Label, Issue
from githubdashlib import get_labels as _get_labels
from githubdashlib import get_issues as _get_issues
from githubdashlib import get_all_the_issues as _get_all_the_issues 


TOKEN = os.environ.get("GITHUB_API_TOKEN", None)
ISSUES_URI = "/repos/streamlit/streamlit/issues"
LABELS_URI = "/repos/streamlit/streamlit/labels"

@st.cache
def get_connection():
    return Connection(TOKEN)

CONN = get_connection()

@st.cache
def get_labels():
    return _get_labels(CONN, per_page=100)

@st.cache
def get_all_open_issues():
    return _get_all_the_issues(CONN, "open")

@st.cache
def get_all_closed_issues():
    return _get_all_the_issues(CONN, "closed")



def make_ttc_dataframe(issues):
    # "closed_at" should exist in all issues for this to work
    issdict = {"number": [],
               "title": [],
               "state": [],
               "labels": [],
               "ttc": [],
              }
    for iss in issues:
        labels = list(iss.labels.keys())

        if "bug" not in labels:
            continue

        issdict["number"].append(iss.number)
        issdict["title"].append(iss.title)
        issdict["state"].append(iss.state)
        issdict["labels"].append(list(iss.labels.keys()))
        issdict["ttc"].append(iss.time_to_close)

    return pd.DataFrame(issdict)


def make_issue_dataframe(issues):
    issdict = {"number": [],
               "title": [],
               "state": [],
               "is_enhancement": [],
               "is_bug": [],
               "is_both": [],
               "is_docs": [],
               "is_neither": [],
               "needs_triage": [],
               "labels": [],
               "created_at": [],
               "closed_at": [],
            }
    for iss in issues:
        labels = list(iss.labels.keys())

        issdict["number"].append(iss.number)
        issdict["title"].append(iss.title)
        issdict["state"].append(iss.state)
        issdict["needs_triage"].append(1 if "needs_triage" in labels else 0)
        issdict["labels"].append(labels)
        issdict["created_at"].append(None if not iss.created_at else iss.created_at.timestamp())
        issdict["closed_at"].append(None if not iss.closed_at else iss.closed_at.timestamp())

        issdict["is_docs"].append(1 if "docs" in labels else 0)

        if "enhancement" in labels and "bug" in labels:
            issdict["is_both"] = 1
            issdict["is_enhancement"] = 0
            issdict["is_bug"] = 0
            issdict["is_neither"] = 0
        elif "enhancement" in labels:
            issdict["is_both"] = 0
            issdict["is_enhancement"] = 1
            issdict["is_bug"] = 0
            issdict["is_neither"] = 0
        elif "bug" in labels:
            issdict["is_both"] = 0
            issdict["is_enhancement"] = 0
            issdict["is_bug"] = 1
            issdict["is_neither"] = 0
        else:
            issdict["is_both"] = 0
            issdict["is_enhancement"] = 0
            issdict["is_bug"] = 0
            issdict["is_neither"] = 1
    
    return pd.DataFrame(issdict)
    

# -- SETUP --
labels = get_labels()
open_issues = get_all_open_issues()
closed_issues = get_all_closed_issues()
issues = open_issues + closed_issues 

issdf = make_issue_dataframe(issues)


# -- SIDEBAR --
st.sidebar.header("Streamlit GitHub Issue charts!")

option = st.sidebar.selectbox(
        "CHARTS!",
        ('Issue breakdown by major label', 
         'Issue breakdown by project category',
         'Issues closed by month',
         'Time-to-close bugs',
         'Time-to-first-answer',
         'Issue open/close rates',
        ))

st.sidebar.header("Basic stats")
st.sidebar.markdown("* Total issues: %i" % len(issues))
st.sidebar.markdown("* Open issues: %i" % len(open_issues))
st.sidebar.markdown("* Closed issues: %i" % len(closed_issues))


# -- MAIN --
if option == "Issue breakdown by major label":
    st.write(issdf)

    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    labels = "enhancement", "bug", "docs", "bughancement", "PR or ??"

    #sizes = [15, 30, 45, 10]
    sizes = (issdf["is_enhancement"].sum(), 
            issdf["is_bug"].sum(),
            issdf["is_docs"].sum(),
            issdf["is_both"].sum(),
            issdf["is_neither"].sum(),
            )
    #explode = (0, .1, 0, 0)  # only "explode" the 4th slice
    explode = (0, 0, 0, 0.1, 0)

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    st.pyplot()


# ---
if option == "Issue breakdown by project category":
    fig, ax = plt.subplots()

    size = 0.3
    vals = np.array([[60., 32.], [37., 40.], [29., 10.]])

    cmap = plt.get_cmap("tab20c")
    outer_colors = cmap(np.arange(3)*4)
    inner_colors = cmap([1, 2, 5, 6, 9, 10])

    ax.pie(vals.sum(axis=1), radius=1, colors=outer_colors,
           wedgeprops=dict(width=size, edgecolor='w'))

    ax.pie(vals.flatten(), radius=1-size, colors=inner_colors,
           wedgeprops=dict(width=size, edgecolor='w'))

    ax.set(aspect="equal", title='Pie plot with `ax.pie`')
    st.pyplot()


# ---
if option == "Time-to-close bugs":
    st.write("For all closed BUGS, how long did it take us to close them?")

    issdf = make_ttc_dataframe(closed_issues)

    st.dataframe(issdf)

    # Data for plotting


# ---
if option == "Issue open/close rates":
    st.write("Since launch, how many issues have been opened per day? How many closed?")

    # ----- Fake stand-in graph ----- 
    # X axis = days since launch
    t = np.arange(0, 210, 1)
    
    # Y axis = avg length to time it took us to put a first response on an issue.
    s = 1 + np.sin(2 * np.pi * t)

    fig, ax = plt.subplots()
    ax.plot(t, s)

    ax.set(xlabel='time (days)', ylabel='avg time to close a bug',
           title='Not the real graph')
    ax.grid()

    fig.savefig("test.png")
    st.pyplot()