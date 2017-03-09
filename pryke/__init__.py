from enum import Enum, unique
from requests_oauthlib import OAuth2Session

import datetime


class Pryke:

    def __init__(self, client_id, client_secret, access_token=None):
        """
        A client for interacting with the Wrike API.

        Args:
            client_id (str):
            client_secret (str):
            access_token (str):
        """
        self.endpoint = "https://www.wrike.com/api/v3/"
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

    def get(self, path, params={}):
        """
        Dispatch GET request and return response.

        Args:
            path (str): relative path to get.
            params (dict):  dictionary of request parameters.

        Returns:
            A requests response object.

        """
        return self.oauth.get("{}{}".format(self.endpoint, path), params=params)

    def account(self, account_id):
        """
        Look up an account by ID

        Args:
            account_id (str): ID for the account

        Returns:
            Account
        """
        r = self.get("accounts/{}".format(account_id))

        if r.status_code == 200:
            return Account(self, data=r.json()['data'][0])
        else:
            return None

    def accounts(self):
        """
        All accounts current user has access to.

        Yields:
            Account
        """
        r = self.get("accounts")

        for account_data in r.json()['data']:
            yield Account(self, data=account_data)

    def comments(self):
        """Yields all comments in all accounts"""
        r = self.get("comments")

        for comment_data in r.json()['data']:
            yield Comment(self, data=comment_data)

    def contact(self, contact_id):
        """Returns a contact by ID"""
        r = self.get("contacts/{}".format(contact_id))

        return Contact(self, data=r.json()['data'][0])

    def contacts(self):
        """Yields accounts user has access to"""
        r = self.get("contacts")

        for contact_data in r.json()['data']:
            yield Contact(self, data=contact_data)

    def folder(self, folder_id):
        """
        Search for a single folder by ID
        Args:
            folder_id (str):  ID of the folder

        Returns:
            Folder
        """
        r = self.get("folders/{}".format(folder_id))
        return Folder(self, data=r.json()['data'][0])

    def folders(self, folder_ids=None):
        """
        Yields folders for all accounts, or filtered by folder ids.

        :param folder_ids: a list of folder IDs to return
        :yields: Folder
        """
        if folder_ids is None:
            r = self.get("folders")
        else:
            folder_ids = ",".join(folder_ids)
            r = self.get("folders/{}".format(folder_ids))
        for folder_data in r.json()['data']:
            yield Folder(self, data=folder_data)

    def group(self, group_id):
        """
        Looks up a group by ID

        Args:
            group_id (str):  Group ID

        Returns:
            Group
        """
        r = self.get("groups/{}".format(group_id))

        return Group(self, data=r.json()['data'][0])

    def task(self, task_id):
        """
        Looks up a task by ID
        https://developers.wrike.com/documentation/api/methods/query-tasks#get-tasks-multi

        Args:
            task_id (str): Task ID

        Returns:
            Task
        """
        # TODO: add parameters
        r = self.get("tasks/{}".format(task_id))
        return Task(self, data=r.json()['data'][0])

    def tasks(self):
        r = self.get("tasks")
        for task_data in r.json()['data']:
            yield Task(self, data=task_data)

    def user(self, user_id):
        """
        Looks up a user by ID

        Args:
            user_id (str):  ID for user.

        Returns:
            User
        """
        r = self.get("users/{}".format(user_id))

        return User(self, data=r.json()['data'][0])


class PrykeObject:

    def __init__(self, instance, data={}):
        self.instance = instance

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

    def get(self, path, params={}):
        return self.instance.get(path, params=params)


class Account(PrykeObject):

    def __init__(self, instance, data={}):
        """
        Wrike Account.

        Args:
            instance (Pryke):  An API client instance.
            data (dict): Data to populate object attributes.
        """
        super().__init__(instance, data)

        self.id = data.get('id')
        self.name = data.get('name')
        self.date_format = data.get('title')
        self.first_day_of_week = data.get("firstDayOfWeek")
        self.work_days = data.get("workDays")
        self.root_folder_id = data.get("rootFolderId")
        self.recycle_bin_id = data.get("recycleBinId")
        self.created_date = data.get("createdDate")
        self.subscription = data.get("subscription")
        self.metadata = data.get("metadata")
        self.custom_fields = data.get("customFields")
        self.joined_date = data.get("joinedDate")

        self._date_fields = ["created_date", "joined_date"]
        self._format_dates()

    def __repr__(self):
        return "Account(id='{}', name='{}')".format(self.id, self.name)

    def attachments(self, start, end):
        """
        Return all Attachments of account tasks and folders.
        https://developers.wrike.com/documentation/api/methods/get-attachments#get-accounts-single-attachments

        Args:
            start (datetime.datetime): Created date filter start
            end (datetime.datetime): Created date filter end (must be less than 31 days from start)

        Yields:
            Attachment
        """
        # TODO: add versions and withUrls params
        params = {'createdDate': { 'start': start.strftime("%Y-%m-%dT%H:%M:%SZ"),
                                   'end': end.strftime("%Y-%m-%dT%H:%M:%SZ") }}
        r = self.get("accounts/{}/attachments".format(self.id), params=params)

        for attachment_data in r.json()['data']:
            yield Attachment(self.instance, data=attachment_data)

    def contacts(self):
        """
        Gets the contacts associated with the account.

        Yields:
            Contacts

        """
        r = self.get("accounts/{}/contacts".format(self.id))

        for contact_data in r.json()['data']:
            yield Contact(self.instance, data=contact_data)

    def folders(self):
        """
        All folders associated with the account.

        Yields:
            Folder
        """
        r = self.get("accounts/{}/folders".format(self.id))

        for folder_data in r.json()['data']:
            yield Folder(self.instance, data=folder_data)

    def groups(self):
        """
        All groups associated with the account.

        Yields:
            Group

        """
        r = self.get("accounts/{}/groups".format(self.id))

        for group_data in r.json()['data']:
            yield Group(self.instance, data=group_data)

    def tasks(self):
        """
        All tasks associated with the account.

        Yields:
            Tasks

        """
        r = self.get("accounts/{}/tasks".format(self.id))

        for task_data in r.json()['data']:
            yield Task(self.instance, data=task_data)


class Attachment(PrykeObject):

    def __init__(self, instance, data={}):
        """
        Wrike Attachment
        https://developers.wrike.com/documentation/api/methods/attachments

        Args:
            instance (Pryke): Current Pryke instance.
            data (dict):  Attributes to populate.
        """
        super().__init__(instance, data)
        self.id = data.get('id')
        self.author_id = data.get('authorId')  # ID of user who uploaded attachment
        self.name = data.get('name')  # Attachment filename
        self.created_date = data.get('createdDate')  # Upload date
        self.version = data.get('version')  # Attachment version (number)
        self.type = AttachmentType(data.get('type'))  # AttachmentType
        self.content_type = data.get('contentType')  # string
        self.size = data.get('size')  # For external attachments, size is equal to -1
        self.task_id = data.get('taskId')  # ID of related task.
        self.folder_id = data.get('folderId')  # ID of related folder.
        # TODO: more fields

        self._date_fields = ["created_date"]
        self._format_dates()


@unique
class AttachmentType(Enum):

    box = "Box"
    drop_box = "DropBox"
    google = "Google"
    one_drive = "OneDrive"
    wrike = "Wrike"  # Attachment file content stored in Wrike.


class Comment(PrykeObject):

    def __init__(self, instance, data={}):
        """
        Wrike Comment
        https://developers.wrike.com/documentation/api/methods/comments

        Args:
            instance (Pryke):
            data (dict):
        """
        super().__init__(instance, data)
        self.id = data.get('id')
        self.author_id = data.get('authorId')
        self.text = data.get('text')  # text (body) of the comment
        self.updated_date = data.get('updatedDate')
        self.created_date = data.get('createdDate')
        self.task_id = data.get('taskId')
        self.folder_id = data.get('folderId')

        self._date_fields = ["created_date", "updated_date"]
        self._format_dates()


class Contact(PrykeObject):

    def __init__(self, instance, data={}):
        """
        Wrike Contact
        https://developers.wrike.com/documentation/api/methods/contacts

        Args:
            instance (Pryke):
            data (dict):
        """
        super().__init__(instance, data)
        self.id = data.get('id')
        self.first_name = data.get('firstName')
        self.last_name = data.get('lastName')
        self.type = data.get('type')  # UserType Enum
        # TODO: add more properties


class Folder(PrykeObject):

    def __init__(self, instance, data={}):
        """
        Wrike Folder
        https://developers.wrike.com/documentation/api/methods/folders-&-projects

        Args:
            instance (Pryke):
            data (dict):
        """
        super().__init__(instance, data)
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
        # TODO: add more fields
        self.project = data.get('project')

        self._date_fields = []
        self._format_dates()

    def __repr__(self):
        return "Folder(id='{}', title='{}')".format(self.id, self.title)

    def attachments(self):
        """
        All Attachments of a folder.
        https://developers.wrike.com/documentation/api/methods/get-attachments#get-folders-single-attachments

        Yields:
            Attachment
        """
        # TODO: add versions, createdDate, and withUrls parameters
        r = self.get("folders/{}/attachments".format(self.id))

        for attachment_data in r.json()['data']:
            yield Attachment(self.instance, data=attachment_data)

    def children(self):

        for child_id in self.child_ids:
            f = Folder()
            f.id = child_id
            yield f

    def shared_users(self):
        """
        Users who share the folder.

        Yields:
            User
        """
        for user_id in self.shared_ids:
            yield self.instance.user(user_id)


class Group(PrykeObject):

    def __init__(self, instance, data={}):
        """
        A collection of Users
        https://developers.wrike.com/documentation/api/methods/groups

        Args:
            instance (Pryke):  An API client instance.
            data (dict):  Data to populate object attributes.
        """
        super().__init__(instance, data)

        self.id = data.get('id')
        self.account_id = data.get('accountId')
        self.title = data.get('title')
        self.member_ids = data.get('memberIds')  # List of group members user IDs
        self.child_ids = data.get('childIds')
        self.parent_ids = data.get('parentIds')
        self.avatar_url = data.get('avatarUrl')
        self.my_team = data.get('myTeam')  # Field is present and set to true for My Team (default) group
        self.metadata = data.get('metadata')

    def account(self):
        """
        Account associated with this group.

        Returns:
            Account

        """
        return self.instance.account(self.account_id)

    def users(self):
        """
        All users belonging to this group.

        Yields:
            User

        """
        for user_id in self.member_ids:
            yield self.instance.user(user_id)


class Task(PrykeObject):

    def __init__(self, instance, data={}):
        """
        Wrike Task
        https://developers.wrike.com/documentation/api/methods/tasks

        Args:
            instance (Pryke): An API client instance.
            data (dict): Data to populate object attributes.
        """
        super().__init__(instance, data)
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
        # TODO: add more properties

        self._date_fields = ["created_date", "updated_date", "completed_date"]
        self._format_dates()

    def __repr__(self):
        return "Task(id='{}', title='{}')".format(self.id, self.title)

    def attachments(self):
        """
        All Attachments of the task.
        https://developers.wrike.com/documentation/api/methods/get-attachments#get-tasks-single-attachments

        Yields:
            Attachment
        """
        # TODO: add versions, createdDate, and withUrls parameters
        r = self.get("tasks/{}/attachments".format(self.id))

        for attachment_data in r.json()['data']:
            yield Attachment(self.instance, data=attachment_data)


class User(PrykeObject):

    def __init__(self, instance, data={}):
        """
        Wrike User
        https://developers.wrike.com/documentation/api/methods/users

        Args:
            instance (Pryke):  An API client instance.
            data (dict):  Data to populate object attributes.
        """
        super().__init__(instance, data)

        self.id = data.get('id')
        self.first_name = data.get('firstName')
        self.last_name = data.get('lastName')
        self.type = data.get('type')  # UserType Enum
        self.profiles = data.get('profiles')
        # TODO: add more properties
