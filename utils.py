from datetime import datetime


def get_date(github_datetime):
    if github_datetime is not None:
        return datetime.strptime(github_datetime, "%Y-%m-%dT%H:%M:%SZ")

class SimpleIssue:
    def __init__(self, **kwargs):
        self.__dict__ = kwargs

    def get_labels(self):
        out = ""
        for label in self.labels:
            out += label["name"]
        return out

    def get_creator(self):
        return self.user["login"]

    def to_dict(self):
        return {
            "title": self.title,
            "url": self.url,
            "number": self.number,
            "labels": self.get_labels(),
            "creator": self.get_creator(),
            "state": self.state,
            "assigned": self.assignee,
            "num_comments": self.comments,
            "created_at": get_date(self.created_at),
            "updated_at": get_date(self.updated_at),
            "closed_at": get_date(self.closed_at),
            "closed_by": self.closed_by,
        }

    def to_json(self):
        return json.dumps({
            "title": self.title,
            "url": self.url,
            "number": self.number,
            "labels": self.get_labels(),
            "creator": self.get_creator(),
            "state": self.state,
            "assigned": self.assignee,
            "num_comments": self.comments,
            "created_at": self.created_at,
            "updated_at": self.updated_at),
            "closed_at": self.closed_at,
            "closed_by": self.closed_by,
        })



