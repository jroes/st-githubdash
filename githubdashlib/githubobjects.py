from datetime import datetime


class Event:
    def __init__(self, **kwargs):
        self.actor = kwargs.get("actor", None)
        self.created_at = kwargs.get("created_at", None)
        self.org = kwargs.get("org", None)
        self.payload = kwargs.get("payload", None)
        self.public = kwargs.get("public", False)
        self.repo = kwargs.get("repo", None)
        self.type = kwargs.get("type", None)

        self._process_datetimes()

    @property
    def action(self):
        return self.payload.get("action", None)

    @property
    def username(self):
        return self.actor.get("login", None)

    def _process_datetimes(self):
        # '2020-07-23T05:47:47Z'
        if self.created_at:
            self.created_at = datetime.strptime(self.created_at, "%Y-%m-%dT%H:%M:%SZ")

    def __str__(self):
        return "[{e.actor.login}]: {e.payload}".format(e = self)




class Label:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
        self.node_id = kwargs.get('node_id', None)
        self.url = kwargs.get('url', None)
        self.name = kwargs.get('name', None)
        self.color = kwargs.get('color', None)
        self.default = kwargs.get('default', False)
        self.description = kwargs.get('description', None)

    @property
    def href(self):
        return '<a href="{l.url}">{l.name}</a>'

    @property
    def html_name(self):
        return '<font style="font-weight:bold;" color="#{l.color}">[{l.name}]</font>'.format(l=self)

    def __str__(self):
        return "[{l.name}]: {l.description}".format(l = self)

    def __repr__(self):
        return "<Label {l.name}: {l.color}>".format(l = self)



class Issue:
    def __init__(self, **kwargs):
        self.state = kwargs.get("state", None)
        self.number = kwargs.get("number", None)
        self.title = kwargs.get("title", None)
        self.user = kwargs.get("user", None)
        self.locked = kwargs.get("locked", None)
        self.assignee = kwargs.get("assignee", None)
        self.assignees = kwargs.get("assignees", [])
        self.milestone = kwargs.get("milestone", None)
        self.comments = kwargs.get("comments", 0)
        self.author_association = kwargs.get("author_association", None)
        self.active_lock_reason = kwargs.get("active_lock_reason", None)
        self.body = kwargs.get("body", "")

        self.created_at = kwargs.get("created_at", None)
        self.updated_at = kwargs.get("updated_at", None)
        self.closed_at = kwargs.get("closed_at", None)
        self._process_datetimes()

        self.labels = {}
        labels = kwargs.get("labels", [])
        for item in labels:
            label = Label(**item)
            self.labels[label.name] = label

        self.repository_url = kwargs.get("repository_url", None)
        self.labels_url = kwargs.get("labels_url", None)
        self.comments_url = kwargs.get("comments_url", None)
        self.events_url = kwargs.get("events_url", None)
        self.html_url = kwargs.get("html_url", None)

    def _process_datetimes(self):
        # '2020-07-23T05:47:47Z'
        if self.created_at:
            self.created_at = datetime.strptime(self.created_at, "%Y-%m-%dT%H:%M:%SZ")
            #self.created_at = self.created_at.replace(tzinfo=None)
        if self.updated_at:  
            self.updated_at = datetime.strptime(self.updated_at, "%Y-%m-%dT%H:%M:%SZ")
            #self.updated_at = self.updated_at.replace(tzinfo=None)
        if self.closed_at:
            self.closed_at = datetime.strptime(self.closed_at, "%Y-%m-%dT%H:%M:%SZ")
            #self.closed_at = self.closed_at.replace(tzinfo=None)

    @property
    def time_to_close(self):
        if self.closed_at:
            return self.closed_at - self.created_at
        return None

    def __str__(self):
        return "#{i.number}: {i.title}".format(i = self)

    def __repr__(self):
        return "<Issue #{i.number}: {i.title}>".format(i = self)


