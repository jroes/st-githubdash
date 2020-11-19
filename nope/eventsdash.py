import time
import os

import streamlit as st
import pandas as pd 

from octohub.connection import Connection

from githubdashlib import get_all_events as _get_events


TOKEN = os.environ.get("GITHUB_API_TOKEN", None)


@st.cache
def get_connection():
    return Connection(TOKEN)

CONN = get_connection()

def get_events():
    return _get_events(CONN)


# -- EVENTS LIST --

eventdict = {
    "username": [],
    "action": [],
    "created_at": [],
    "title": [],
    "url": [],
    }

for event in get_events():
    if event.action == "created":
        eventdict["username"].append(event.username)
        eventdict["action"].append(event.action)
        eventdict["created_at"].append(event.created_at)
        try:
            eventdict["title"].append(event.payload["issue"]["title"])
            eventdict["url"].append(event.payload["issue"]["url"])
        except KeyError:
            eventdict["title"].append("na")
            eventdict["url"].append(None)


st.table(eventdict)

