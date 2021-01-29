import streamlit as st
import secrets_beta
import pandas as pd
from github import Github

import altair as alt
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
 
@st.cache
def get_issues(repo_name, since):
    gh = Github(st.secrets["GITHUB_API_KEY"])
    repo = gh.get_repo(repo_name)
    return [format_issue(issue) for issue in repo.get_issues(state="all",
        since=datetime.combine(since, datetime.min.time()))[:350]]

def format_issue(issue):
    formatted_issue = {
        'number': issue.number,
        'url': issue.html_url,
        'body': issue.body,
        'state': issue.state,
        'created_at': issue.created_at,
        'closed_at': issue.closed_at,
        'comments_count': issue.comments,
        'is_pull_request': issue.pull_request is not None,
        'labels': [label.name for label in issue.labels]
    }

    if issue.comments > 0:
        comments = issue.get_comments()
        first_comment = comments[0]
        formatted_issue['first_comment_at'] = first_comment.created_at

    return formatted_issue

def add_issue_stats(df):
    df['hrs_until_issue_closed'] = (df['closed_at'] - df['created_at']).dt.total_seconds()/3600
    df['hrs_until_first_comment'] = (df['first_comment_at'] - df['created_at']).dt.total_seconds()/3600
    return df

st.header("GitHub analytics dashboard")

repo_name = st.text_input("Repository name", "streamlit/streamlit")
since = st.date_input("Issues since", value=date.today() + relativedelta(months=-3))
#issue_count = st.number_input("Number of issues to analyze", value=200)

issues = get_issues(repo_name, since)

df = pd.DataFrame.from_dict(issues)
df = add_issue_stats(df)

st.subheader("How quickly do we usually answer a GitHub issue?")
c = alt.Chart(df).mark_circle().encode(
    x='created_at', y='hrs_until_first_comment', size='comments_count', color='state',
    tooltip=['number', 'created_at', 'hrs_until_first_comment', 'comments_count'],
    href='url')
st.altair_chart(c, use_container_width=True)

# Issue age should be easy and fun
#  Find closed_at and plot by created_at... maybe?
#  Issue number is a good substitute for temporal order...

st.subheader("How quickly do we merge PRs?")
c = alt.Chart(df[df.is_pull_request.eq(True)]).mark_circle().encode(
    x='created_at', y='hrs_until_issue_closed', size='hrs_until_issue_closed',
    tooltip=['number', 'created_at', 'hrs_until_issue_closed'],
    href='url')
st.altair_chart(c, use_container_width=True)

# Month by month average
c = alt.Chart(df[df.is_pull_request.eq(True)]).mark_bar().encode(
    x='yearmonth(created_at):O', y='average(hrs_until_issue_closed)')
st.altair_chart(c, use_container_width=True)


# Could I pull in issue labels?
st.subheader("How quickly do we close issues?")

c = alt.Chart(df).mark_circle().encode(
    x='created_at', y='hrs_until_issue_closed',
    tooltip=['number', 'created_at', 'hrs_until_issue_closed', 'comments_count'],
    href='url')
st.altair_chart(c, use_container_width=True)

with st.beta_expander("Raw data"):
    df

# TODO:
# . PR turnaround time
# . PR comment turnaround time
# . average PRs per week
# . LOC changed per PR