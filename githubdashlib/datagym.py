import pandas as pd


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


