import streamlit as st
import secrets_beta
import pandas as pd
from github import Github

import altair as alt
 
@st.cache
def get_issues(repo_name, issue_count):
    gh = Github(st.secrets["GITHUB_API_KEY"])
    repo = gh.get_repo(repo_name)
    return [format_issue(issue) for issue in repo.get_issues(state="all")[:issue_count]]

def format_issue(issue):
    formatted_issue = {
        'number': issue.number,
        'url': issue.url,
        'body': issue.body,
        'state': issue.state,
        'created_at': issue.created_at,
        'closed_at': issue.closed_at,
        'comments_count': issue.comments,
        'is_pull_request': issue.pull_request is not None
    }

    if issue.comments > 0:
        comments = issue.get_comments()
        first_comment = comments[0]
        formatted_issue['first_comment_at'] = first_comment.created_at

    return formatted_issue

repo_name = st.text_input("Repository name", "streamlit/streamlit")
issue_count = st.number_input("Number of issues to analyze", value=200)

issues = get_issues(repo_name, issue_count)

df = pd.DataFrame.from_dict(issues)

df['hrs_until_first_comment'] = (df['first_comment_at'] - df['created_at']).dt.total_seconds()/3600

# This ended up not filling the container width the way I expected
#st.vega_lite_chart(df, {
#    'mark': {'type': 'circle', 'tooltip': True},
#    'encoding': {
#        'x': {'field': 'created_at', 'type': 'temporal'},
#        'y': {'field': 'hrs_until_first_comment', 'type': 'quantitative'}
#        'size': {'field': 'c', 'type': 'quantitative'},
#        'color': {'field': 'c', 'type': 'quantitative'},
#    },
#}, use_container_width=True)

st.subheader("How quickly do we usually answer a GitHub issue?")
c = alt.Chart(df).mark_circle().encode(
    x='created_at', y='hrs_until_first_comment', size='comments_count', color='state',
    tooltip=['number', 'created_at', 'hrs_until_first_comment', 'comments_count'])
st.altair_chart(c, use_container_width=True)


# Issue age should be easy and fun
#  Find closed_at and plot by created_at... maybe?
#  Issue number is a good substitute for temporal order...

st.subheader("How quickly do we close issues?")
df['hrs_until_issue_closed'] = (df['closed_at'] - df['created_at']).dt.total_seconds()/3600

c = alt.Chart(df).mark_circle().encode(
    x='created_at', y='hrs_until_issue_closed',
    tooltip=['number', 'created_at', 'hrs_until_issue_closed', 'comments_count'])
st.altair_chart(c, use_container_width=True)

with st.beta_expander("Raw data"):
    df
