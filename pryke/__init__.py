from enum import Enum, unique
from jinja2 import Environment, PackageLoader
from requests_oauthlib import OAuth2Session

import datetime
import requests
import time


class Pryke:
    """
    A client for interacting with the Wrike API.

    Attributes:
        _response (request):  Last response received by client.  Used for testing.
        endpoint (str):  Base URL for the API
        oauth (requests_oauthlib.OAuth2Session):  OAuth Session
        templates (jinja2.Environment):  Templates Environment
    """
    def __init__(self, client_id, client_secret, access_token=None):
        """
        Initializes the client.

        Args:
            client_id (str):
            client_secret (str):
            access_token (str):
        """
        self.endpoint = "https://www.wrike.com/api/v3/"
        self.oauth = OAuth2Session(client_id=client_id, redirect_uri="http://localhost")
        self._response = None

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

        self.templates = Environment(loader=PackageLoader("pryke", "templates"))

    def get(self, path, params={}, delay=None):
        """
        Dispatch GET request and return response.  Throttles back exponentially if API returns status codes 429 or 503

        Args:
            path (str): relative path to get.
            params (dict):  dictionary of request parameters.
            delay (int):  Seconds to wait before dispatching request; used to throttle

        Returns:
            requests.Response: Response

        See Also:
            Question no. 8 regarding rate limits
            https://developers.wrike.com/faq/
        """
        if delay is not None:
            delay **= 2
            time.sleep(delay)
            delay += 1

        if self.endpoint not in path:
            path = "{}{}".format(self.endpoint, path)

        self._response = self.oauth.get(path, params=params)

        if self._response.status_code in [429, 503]:
            return self.get(path, params=params, delay=delay or 1)

        return self._response

    def account(self, account_id):
        """
        Look up an account by ID

        Args:
            account_id (str): ID for the account

        Returns:
            :class:`Account`:
        """
        r = self.get("accounts/{}".format(account_id))

        if r.status_code == 200:
            return Account(self, data=r.json()['data'][0])
        return None

    def accounts(self):
        """
        All accounts current user has access to.

        Yields:
            :class:`Account`: The next account.
        """
        r = self.get("accounts")

        for account_data in r.json()['data']:
            yield Account(self, data=account_data)

    def attachment(self, attachment_id):
        """
        Looks up an attachment by ID

        Args:
            attachment_id (str): ID of attachment

        Returns:
            :class:`Attachment`: The attachment
        """
        r = self.get("attachments/{}".format(attachment_id))
        if r.status_code == 200:
            return Attachment(self, data=r.json()['data'][0])
        return None

    def comment(self, comment_id):
        """
        Look up a comment by ID

        Args:
            comment_id:

        Returns:
            :class:`Comment`: The comment
        """
        r = self.get("comments/{}".format(comment_id))
        if r.status_code == 200:
            return Comment(self, data=r.json()['data'][0])
        return None

    def comments(self):
        """
        All comments in all accounts

        Yields:
            :class:`Comment`:
        """
        r = self.get("comments")

        for comment_data in r.json()['data']:
            yield Comment(self, data=comment_data)

    def contact(self, contact_id):
        """
        Look up a contact by ID

        Args:
            contact_id (str):  Contact ID to look up.

        Return:
            :class:`Contact`:
        """
        r = self.get("contacts/{}".format(contact_id))

        return Contact(self, data=r.json()['data'][0])

    def contacts(self):
        """
        Contacts of all users and user groups in all accessible accounts.

        Yields:
            :class:`Contact`

        See Also:
            https://developers.wrike.com/documentation/api/methods/query-contacts#get-contacts-empty
        """
        r = self.get("contacts")

        for contact_data in r.json()['data']:
            yield Contact(self, data=contact_data)

    def folder(self, folder_id):
        """
        Search for a single folder by ID

        Args:
            folder_id (str):  ID of the folder

        Returns:
            :class:`Folder`:
        """
        r = self.get("folders/{}".format(folder_id))
        return Folder(self, data=r.json()['data'][0])

    def folders(self):
        """
        Folders for all accounts

        Yields:
            :class:`Folder`:
        """
        r = self.get("folders")
        for folder_data in r.json()['data']:
            yield Folder(self, data=folder_data)

    def group(self, group_id):
        """
        Looks up a group by ID

        Args:
            group_id (str):  Group ID

        Returns:
            :class:`Group`:
        """
        r = self.get("groups/{}".format(group_id))

        return Group(self, data=r.json()['data'][0])

    def task(self, task_id):
        """
        Looks up a task by ID

        Args:
            task_id (str): Task ID

        Returns:
            :class:`Task`:

        See Also:
            https://developers.wrike.com/documentation/api/methods/query-tasks#get-tasks-multi
        """
        # TODO: add parameters
        r = self.get("tasks/{}".format(task_id))
        return Task(self, data=r.json()['data'][0])

    def tasks(self, title=None):
        """
        Queries for tasks in all accounts.

        Keyword Args:
            title (str):  Title filter, exact match

        Yields:
            :class:`Task`:

        See Also:
            https://developers.wrike.com/documentation/api/methods/query-tasks#get-tasks-empty
        """
        params = {'title': title}
        r = self.get("tasks", params)
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

    @property
    def version(self):
        """
        Current API version as reported by server.

        Returns:
            tuple: A tuple of the major and minor version numbers.

        See Also:
            https://developers.wrike.com/documentation/api/methods/api-version
        """
        r = self.get("version")
        data = r.json()["data"][0]
        return data['major'], data['minor']


class PrykeObject:
    """
    Generic Pryke Object

    Attributes:
        self.instance (:class:`Pryke`): API Client Instance
        self._date_fields (list):  List of fields to treat as dates
    """
    def __init__(self, instance, data={}):
        """
        Inits Object

        Args:
            instance (:class:`Pryke`): API Client Instance
            data (dict): Data received from API client
        """
        self.instance = instance

        self._data = data
        self._date_fields = []

    def _format_dates(self):
        """
        Format date strings to python datetime

        Returns:
            bool: True is successful
        """
        for date_field in self._date_fields:
            current_value = getattr(self, date_field)
            if current_value is not None:
                setattr(self, date_field, datetime.datetime.strptime(current_value, "%Y-%m-%dT%H:%M:%SZ"))

        return True

    def get(self, path, params={}):
        """
        Convenience method for executing a GET request

        Args:
            path (str):
            params (dict):

        Returns:

        """
        return self.instance.get(path, params=params)


class Account(PrykeObject):
    """
    Wrike Account

    Attributes:
        id (str):  Unique identifier for account
        name (str):  Name of account
        date_format (str):  Date format (d/MM/yyyy or MM/dd/yyyy)
        first_day_of_week (str): First day of week Week Day, Enum: Sat, Sun, Mon
        work_days (list):  List of weekdays, not empty. These days are used in task duration computation
        root_folder_id (str):  Identifier for root folder
        recycle_bin_id (str):  Identifier for recycle bin
        created_date (datetime.datetime): Registration date
        subscription: Account subscription; Optional
        metadata (list):  Optional
        custom_fields (list): custom fields accessible for requesting user in the account
        joined_date (datetime.datetime): Date when the user has joined the account

    See Also:
        https://developers.wrike.com/documentation/api/methods/accounts
    """
    def __init__(self, instance, data={}):
        """
        Inits Account

        Args:
            instance (:class:`Pryke`):  An API client instance

        Keyword Args:
            data (dict): Data to populate object attributes
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

        if self.subscription is not None:
            self.subscription_type = self.subscription.get('type')
            self.subscription_paid = self.subscription.get('paid')
            self.subscription_user_limit = self.subscription.get('userLimit')

        self._date_fields = ["created_date", "joined_date"]
        self._format_dates()

    def __repr__(self):
        return "Pryke Account {}".format(self.id)

    def attachments(self, start, end):
        """
        Return all Attachments of account tasks and folders.

        Args:
            start (datetime.datetime): Created date filter start
            end (datetime.datetime): Created date filter end (must be less than 31 days from start)

        Yields:
            :class:`Attachment`

        See Also:
            https://developers.wrike.com/documentation/api/methods/get-attachments#get-accounts-single-attachments
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
            :class:`Contact`
        """
        r = self.get("accounts/{}/contacts".format(self.id))

        for contact_data in r.json()['data']:
            yield Contact(self.instance, data=contact_data)

    def folders(self):
        """
        All folders associated with the account.

        Yields:
            :class:`Folder`
        """
        r = self.get("accounts/{}/folders".format(self.id))

        for folder_data in r.json()['data']:
            yield Folder(self.instance, data=folder_data)

    def groups(self):
        """
        All groups associated with the account.

        Yields:
            :class:`Group`
        """
        r = self.get("accounts/{}/groups".format(self.id))

        for group_data in r.json()['data']:
            yield Group(self.instance, data=group_data)

    @property
    def recycle_bin(self):
        """
        Folder for deleted folders and tasks.

        Returns:
            :class:`Folder`
        """
        r = self.get("folders/{}".format(self.recycle_bin_id))
        return Folder(r.json()['data'])

    @property
    def root_folder(self):
        """
        Root folder of the account.

        Returns:
            :class:`Folder`
        """
        r = self.get("folders/{}".format(self.root_folder_id))
        return Folder(r.json()['data'])

    def tasks(self):
        """
        All tasks associated with the account.

        Yields:
            :class:`Task`
        """
        r = self.get("accounts/{}/tasks".format(self.id))

        for task_data in r.json()['data']:
            yield Task(self.instance, data=task_data)


class Attachment(PrykeObject):
    """
    Wrike Attachment

    Attributes:
        id (str): Unique identifier
        author_id (str): ID of user that uploaded the attachment
        name (str): File Name
        created_date (datetime.datetime): Upload date
        version (int): Version
        type (:class:`AttachmentType`): Type
        content_type (str): Content Type
        size (int): File size; -1 for external attachments
        task_id (str): ID of related task
        folder_id (str): ID of related folder
        comment_id (str): ID of related comment
        current_attachment_id (str): ID of current attachment version
        preview_url (str): Link to download external attachment preview
        url (str): Link to download attachment
        review_ids (list): Review IDs

    See Also:
        https://developers.wrike.com/documentation/api/methods/attachments
    """
    def __init__(self, instance, data={}):
        """
        Inits attachment

        Args:
            instance (:class:`Pryke`): Current Pryke instance.

        Keyword Args:
            data (dict):  Attributes to populate.
        """
        super().__init__(instance, data)

        self.id = data.get('id')
        self.author_id = data.get('authorId')
        self.name = data.get('name')
        self.created_date = data.get('createdDate')
        self.version = data.get('version')
        self.type = AttachmentType(data.get('type'))
        self.content_type = data.get('contentType')
        self.size = data.get('size')
        self.task_id = data.get('taskId')
        self.folder_id = data.get('folderId')
        self.comment_id = data.get('commentId')
        self.current_attachment_id = data.get('currentAttachmentId')
        self.preview_url = data.get('previewUrl')
        self.url = data.get('url')
        self.review_ids = data.get('reviewIds')

        self._author = None
        self._task = None

        self._date_fields = ["created_date"]
        self._format_dates()

    @property
    def author(self):
        """
        User that uploaded the attachment

        Returns:
            :class:`User`: User
        """
        if self._author is None:
            self._author = self.instance.user(self.author_id)
        return self._author

    def download(self, path):
        """
        Downloads the attachment to the specified path

        Args:
            path (str):  Fully-qualified path where attachment should be saved

        Returns:
            bool: True if successful, False on failure
        """
        if self.url is None:
            return False
        with open(path, "wb") as output_file:
            if self.type == AttachmentType.WRIKE:
                r = self.get(self.url)
            else:
                r = requests.get(self.url)
            output_file.write(r.content)
        return True

    @property
    def task(self):
        """
        Related task

        Returns:
            :class:`Task`: The related task
        """
        if self._task is None:
            self._task = self.instance.task(self.task_id)
        return self._task


@unique
class AttachmentType(Enum):

    BOX = "Box"
    DROP_BOX = "DropBox"
    GOOGLE = "Google"
    ONE_DRIVE = "OneDrive"
    WRIKE = "Wrike"  # Attachment file content stored in Wrike.


class Comment(PrykeObject):
    """
    Wrike Comment

    Attributes:
        id (str): Unique identifier
        author_id (str): ID of author user
        text (str): Text of the comment
        updated_date (datetime.datetime): Date and time comment was last updated
        created_date (datetime.datetime):  Date and time comment was created
        task_id (str): ID of related task (only task_id OR folder_id will be populated, not both)
        folder_id (str): ID of related folder (only task_id OR folder_id will be populated, not both)

    See Also:
        https://developers.wrike.com/documentation/api/methods/comments
    """
    def __init__(self, instance, data={}):
        """
        Inits comment

        Args:
            instance (:class:`Pryke`): Current Pryke instance
            data (dict): Data from API
        """
        super().__init__(instance, data)
        self.id = data.get('id')
        self.author_id = data.get('authorId')
        self.text = data.get('text')  # text (body) of the comment
        self.updated_date = data.get('updatedDate')
        self.created_date = data.get('createdDate')
        self.task_id = data.get('taskId')
        self.folder_id = data.get('folderId')

        self._author = None
        self._folder = None
        self._task = None

        self._date_fields = ["created_date", "updated_date"]
        self._format_dates()

    @property
    def author(self):
        """
        Author of comment

        Returns:
            :class:`User`: The author
        """
        if self._author is None:
            self._author = self.instance.user(self.author_id)
        return self._author

    @property
    def folder(self):
        """
        Related folder

        Returns:
            :class:`Folder`: The related folder
        """
        if self._folder is None and self.folder_id is not None:
            self._folder = self.instance.folder(self.folder_id)
        return self._folder

    @property
    def task(self):
        """
        Related task

        Returns:
            :class:`Task`: The related task
        """
        if self._task is None and self.task_id is not None:
            self._task = self.instance.task(self.task_id)
        return self._task


class Contact(PrykeObject):
    """
    Wrike Contact

    See Also:
        https://developers.wrike.com/documentation/api/methods/contacts
    """
    def __init__(self, instance, data={}):
        """
        Inits contact

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
    """
    Wrike Folder

    See Also:
       https://developers.wrike.com/documentation/api/methods/folders-&-projects
    """
    def __init__(self, instance, data={}):
        """
        Inits folder

        Args:
            instance (Pryke):
            data (dict):
        """
        super().__init__(instance, data)
        self.id = data.get('id')
        self.account_id = data.get('accountId')
        self.title = data.get('title')
        self.created_date = data.get('createdDate')
        self.updated_date = data.get('updatedDate')
        self.brief_description = data.get('briefDescription')
        self.description = data.get('description')
        self.color = data.get('color')
        self.shared_ids = data.get('sharedIds', [])
        self.parent_ids = data.get('parentIds', [])
        self.child_ids = data.get('childIds', [])
        self.super_parent_ids = data.get('superParentIds', [])
        self.scope = data.get('scope')
        self.has_attachments = data.get('hasAttachments')
        self.attachment_count = data.get('attachmentCount')
        # TODO: add more fields
        self.project = data.get('project')

        self._date_fields = []
        self._format_dates()

    def __repr__(self):
        return "Pryke Folder {}".format(self.id)

    def attachments(self):
        """
        All attachments of a folder.

        Yields:
            Attachment

        See Also:
            https://developers.wrike.com/documentation/api/methods/get-attachments#get-folders-single-attachments
        """
        # TODO: add versions, createdDate, and withUrls parameters
        r = self.get("folders/{}/attachments".format(self.id))

        for attachment_data in r.json()['data']:
            yield Attachment(self.instance, data=attachment_data)

    def children(self):

        for child_id in self.child_ids:
            f = Folder(self.instance)
            f.id = child_id
            yield f

    def shared_users(self):
        """
        Users who share the folder.

        Yields:
            :class:`User`
        """
        for user_id in self.shared_ids:
            yield self.instance.user(user_id)


class Group(PrykeObject):
    """
    A collection of Wrike Users

    Attributes:
        id (str):  Unique identifier for the group
        account_id (str):  ID for associated account
        title (str):  Title for the group
        member_ids (list):  List of group member user IDs
        child_ids (list):  List of child group IDs
        parent_ids (list):  List of parent group IDs
        avatar_url (str):  URL for group avatar
        my_team (bool):  True for default ("My Team") group
        metadata (list):  List of group metadata entries (key, value string pairs)

    See Also:
        https://developers.wrike.com/documentation/api/methods/groups
    """
    def __init__(self, instance, data={}):
        """
        Inits group

        Args:
            instance (Pryke):  An API client instance.
            data (dict):  Data to populate object attributes.
        """
        super().__init__(instance, data)

        self.id = data.get('id')
        self.account_id = data.get('accountId')
        self.title = data.get('title')
        self.member_ids = data.get('memberIds', [])
        self.child_ids = data.get('childIds', [])
        self.parent_ids = data.get('parentIds', [])
        self.avatar_url = data.get('avatarUrl')
        self.my_team = data.get('myTeam', False)
        self.metadata = data.get('metadata', [])

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
    """
    Wrike Task

    Attributes:
        id (str):  Unique identifier for the task.
        account_id (str):  ID for the associated account.
        title (str):  Title of the task. Cannot be empty.
        description (str):  Optional
        brief_description (str):  Optional
        parent_ids (list):  List of parent folder IDs
        super_parent_ids (list):  List of super parent folder IDs

    See Also:
        https://developers.wrike.com/documentation/api/methods/tasks
    """
    def __init__(self, instance, data={}):
        """
        Inits Task

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
        self.author_ids = data.get('authorIds')
        self.custom_status_id = data.get('customStatusId')
        self.has_attachments = data.get('hasAttachments')
        self.attachment_count = data.get('attachmentCount')  # (int)
        self.permalink = data.get('permalink')  # (str)
        self.priority = data.get('priority')  # (str)
        self.followed_by_me = data.get('followedByMe')  # (bool)
        self.follower_ids = data.get('followerIds')  # (list)
        self.recurrent = data.get('recurrent')  # (bool)
        # TODO: add more properties

        self._author = None

        self._date_fields = ["created_date", "updated_date", "completed_date"]
        self._format_dates()

    def __repr__(self):
        return "Pryke Task {}".format(self.id)

    @property
    def account(self):
        """
        Account this task is associated with.

        Returns:
            Account or None
        """
        return self.instance.account(self.account_id)

    @property
    def author(self):
        """
        Author of the task.

        Returns:
            User
        """
        if self._author is None:
            self._author = self.instance.user(self.author_ids[0])
        return self._author

    def attachments(self):
        """
        All Attachments of the task.

        Yields:
            :class:`Attachment`

        See Also:
            https://developers.wrike.com/documentation/api/methods/get-attachments#get-tasks-single-attachments
        """
        # TODO: add versions, createdDate, and withUrls parameters
        r = self.get("tasks/{}/attachments".format(self.id))

        for attachment_data in r.json()['data']:
            yield Attachment(self.instance, data=attachment_data)

    def comments(self):
        """
        All comments of the task.

        Yields:
            Comment

        See Also:
            https://developers.wrike.com/documentation/api/methods/get-comments#get-tasks-single-comments
        """
        r = self.get("tasks/{}/comments".format(self.id))

        for comment_data in r.json()['data']:
            yield Comment(self.instance, data=comment_data)

    def export(self, path):
        """
        Exports task to HTML format.

        Args:
            path (str): Fully-qualified path to the export file.

        Returns:
            bool: True if file was saved
        """
        template = self.instance.templates.get_template("task.html")
        with open(path, "w") as export_file:
            export_file.write(template.render(task=self))
        return True


class User(PrykeObject):
    """
    Wrike User

    Attributes:
        id (str):  Unique Identifier
        first_name (str):  First Name
        last_name (str):  Last Name
        type (UserType):  Type
        profiles (list):  List of user profiles in accounts accessible for requesting user
        avatar_url (str):  URL for avatar
        timezone (str):  Timezone ID ('America/New_York')
        locale (str):  Locale
        deleted (bool):  True if user is deleted, false otherwise
        me (bool):  Field is present and set to true for requesting user.
        member_ids (list):  List of group members contact IDs
        metadata (list):  Key/value pairs
        my_team (bool):  present and set to true for My Team (default) group
        title (str):  Title
        company_name (str):  Company Name
        phone (str):  Phone number
        location (str):  Location

    See Also:
        https://developers.wrike.com/documentation/api/methods/users
    """
    def __init__(self, instance, data={}):
        """
        Inits User

        Args:
            instance (Pryke):  An API client instance.
            data (dict):  Data to populate object attributes.
        """
        super().__init__(instance, data)

        self.id = data.get('id')
        self.first_name = data.get('firstName')
        self.last_name = data.get('lastName')
        self.type = UserType(data.get('type'))
        self.profiles = data.get('profiles')
        self.avatar_url = data.get('avatarUrl')
        self.timezone = data.get('timezone')
        self.locale = data.get('locale')
        self.deleted = data.get('deleted')
        self.me = data.get('me')
        self.member_ids = data.get('memberIds')
        self.metadata = data.get('metadata')
        self.my_team = data.get('myTeam')
        self.title = data.get('title')
        self.company_name = data.get('companyName')
        self.phone = data.get('phone')
        self.location = data.get('location')

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)


@unique
class UserType(Enum):
    person = "Person"
    group = "Group"