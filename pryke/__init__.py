from requests_oauthlib import OAuth2Session

import datetime


class Pryke:

    def __init__(self, client_id, client_secret, access_token=None):

        self.oauth = OAuth2Session(client_id=client_id, redirect_uri="http://localhost")

        if access_token is not None:
            self.oauth.token = access_token
            self.oauth.access_token = access_token

        else:
            self.authorization_url, state = self.oauth.authorization_url("https://www.wrike.com/oauth2/authorize")
            print(self.authorization_url)

            response = input('Enter the full callback URL')

            token = self.oauth.fetch_token("https://www.wrike.com/oauth2/token",
                                           authorization_response=response,
                                           client_secret=client_secret)

    def folders(self, folder_ids=None):
        """
        Yields folders for all accounts, or filtered by folder ids.

        :param folder_ids: a list of folder IDs to return
        :yields: Folder
        """
        if folder_ids is None:
            r = self.oauth.get("https://www.wrike.com/api/v3/folders")
        else:
            folder_ids = ",".join(folder_ids)
            r = self.oauth.get("https://www.wrike.com/api/v3/folders/{}".format(folder_ids))
            print(r.json())
        for folder_data in r.json()['data']:
            yield Folder(data=folder_data)

    def tasks(self):
        r = self.oauth.get("https://www.wrike.com/api/v3/tasks")
        for task_data in r.json()['data']:
            yield Task(data=task_data)


class PrykeObject:

    def __init__(self, data={}):
        self._data = data
        self._date_fields = []

    def _format_dates(self):
        """
        Format date strings to python datetimes
        :return:
        """
        for date_field in self._date_fields:
            current_value = getattr(self, date_field)
            if current_value is not None:
                setattr(self, date_field, datetime.datetime.strptime(current_value, "%Y-%m-%dT%H:%M:%SZ"))

        return True


class Folder(PrykeObject):

    def __init__(self, data={}):
        super().__init__()
        self.id = data.get('id')
        self.accountId = data.get('accountId')
        self.title = data.get('title')
        self.created_date = data.get('createdDate')
        self.updated_date = data.get('updatedDate')
        self.brief_description = data.get('briefDescription')
        self.description = data.get('description')
        self.color = data.get('color')
        self.shared_ids = data.get('sharedIds')
        self.parent_ids = data.get('parentIds')
        self.child_ids = data.get('childIds')
        self.super_parent_ids = data.get('superParentIds')
        self.scope = data.get('scope')
        self.has_attachments = data.get('hasAttachments')
        self.attachment_count = data.get('attachmentCount')
        # more
        self.project = data.get('project')

        self._date_fields = []
        self._format_dates()

    def __repr__(self):
        return "Folder(id='{}', title='{}')".format(self.id, self.title)

    def children(self):

        for child_id in self.child_ids:
            f = Folder()
            f.id = child_id
            yield f


class Task(PrykeObject):

    def __init__(self, data={}):
        super().__init__()
        self.id = data.get('id')
        self.account_id = data.get('accountId')
        self.title = data.get('title')
        self.description = data.get('description')
        self.brief_description = data.get('briefDescription')
        self.parent_ids = data.get('parentIds')
        self.super_parent_ids = data.get('superParentIds')
        self.shared_ids = data.get('sharedIds')
        self.responsible_ids = data.get('responsibleIds')
        self.status = data.get('status')
        self.importance = data.get('importance')
        self.created_date = data.get('createdDate')
        self.updated_date = data.get('updatedDate')
        self.completed_date = data.get('completedDate')
        self.dates = data.get('dates')
        self.scope = data.get('scope')
        # more

        self._date_fields = ["created_date", "updated_date", "completed_date"]
        self._format_dates()

    def __repr__(self):
        return "Task(id='{}', title='{}')".format(self.id, self.title)
