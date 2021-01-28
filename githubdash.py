import streamlit as st
import pandas as pd


from githubdashlib import get_all_issues_and_PRs, get_connection

@st.cache
def get_everything():
    conn = get_connection("streamlit/streamlit")
    return get_all_issues_and_PRs(conn)


#ALL_ISSUES, ALL_PRS = get_everything()


ALL_ISSUES = []
ALL_PRS = []




st.write("Total issues: %i" % len(ALL_ISSUES))
st.write("Total PRs: %i" % len(ALL_PRS))


