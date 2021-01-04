from ghapi.core import GhApi
import os


api = GhApi(owner="streamlit", repo="streamlit", token=os.environ["GITHUB_API_KEY"])

issues = api.issues.list(state="open")
print(api.limit_rem)






# for posterity -- the following took me about 25 minutes to figure out...

"""
from ghapi import GhApi
import ghapi
ghapi?
from ghapi.core import GhApi
api = GhApi()
api.issues?
api.issues.list(labels=["media"])
GhApi?
GhApi(owner="streamlit", repo="streamlit")
import os
os.environ["GITHUB_API_KEY"]
GhApi(owner="streamlit", repo="streamlit", token=os.environ["GITHUB_API_KEY"])
api = GhApi(owner="streamlit", repo="streamlit", token=os.environ["GITHUB_API_KEY"])
api.issues.list?
issues = api.issues.list(state="open", labels=["media"])
issues
issues = api.issues.list(state="open")
issues
api.activity
api.activity?
api.limit_rem
history
iss1 = issues[0]
iss1
iss1.comments
iss1.labels
iss1.labels?
iss1.state
iss1.labels?
api.limit_rem
iss1.labels
api.limit_rem
iss2.labels
issues[1].labels
api.limit_rem
issues[3].labels
api.limit_rem
issues[2].comments
iss1.assignee
iss1.assignees
api.limit_rem
iss1.number
iss1.user
api.limit_rem
history
"""

