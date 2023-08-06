import pathlib

from lowball.models.authentication_models import Token, valid_token_id
from lowball.models.provider_models import AuthDatabase
from pyArango.connection import Connection
from pyArango.collection import Collection, Field, Collection_metaclass
from .token_validators import *
from pyArango.database import Database
from pyArango.document import Document
from pyArango.theExceptions import DocumentNotFoundError


class AuthenticationCollection(Collection):

    _validation = {
        "on_save": True,
        "on_set": True,
        "on_load": False,
        "allow_foreign_fields": True
    }

    _fields = {
        "tid": Field(validators=[TokenIDValidator()]),
        "cid": Field(validators=[ClientIDValidator()]),
        "cts": Field(validators=[TimestampValidator()]),
        "ets":  Field(validators=[TimestampValidator()]),
        "rcid": Field(validators=[ClientIDValidator()]),
        "r": Field(validators=[RolesValidator()])
    }


class LowballArangoDBAuthDB(AuthDatabase):

    _RESERVED_DATABASE_NAMES = [
        "_system"
    ]

    _RESERVED_COLLECTION_NAMES = [
        "Collection",
        "SystemCollection",
        "Edges"
    ]

    def __init__(self,
                 url="http://127.0.0.1",
                 port=8529,
                 user="root",
                 password=None,
                 verify=True,
                 database_name="lowball_authdb",
                 collection_name="authentication_tokens",
                 ):

        self.url = url
        self.port = port
        self.user = user
        self.password = password
        self.verify = verify
        self.database_name = database_name
        self.collection_name = collection_name

        AuthDatabase.__init__(self)

        self.connection = Connection(
            arangoURL=f"{self.url}:{self.port}",
            username=self.user,
            password=self.password,
            verify=self.verify
        )
        Collection_metaclass.collectionClasses[self.collection_name] = AuthenticationCollection

        self._init_database()
        self._init_collection()

    def _init_database(self):
        try:
            self.database = self.connection[self.database_name]
        except KeyError:
            self.database = self.connection.createDatabase(name=self.database_name)

    def _init_collection(self):
        try:
            self.collection = self.database[self.collection_name]
        except KeyError:
            self.collection = self.database.createCollection(self.collection_name, waitForSync=True)

    def get_now(self):
        return datetime.utcnow()

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Url must be a nonempty string beginning with (http:// or https://")
        if not (value.startswith("http://") or value.startswith("https://")):
            raise ValueError("Url must be a nonempty string beginning with (http:// or https://")

        self._url = value

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, value):
        if not isinstance(value, int) or value not in range(1, 65536):
            raise ValueError("Port must be an integer with values from 1-65535")
        self._port = value

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("User must be a nonempty string")
        self._user = value

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        if not (value is None or isinstance(value, str)):
            raise ValueError("Password must be a string or None")

        self._password = value

    @property
    def verify(self):
        return self._verify

    @verify.setter
    def verify(self, value):
        if isinstance(value, bool):
            self._verify = value
        elif isinstance(value, str):
            path = pathlib.Path(value)
            if not path.exists() or not path.is_file():
                raise ValueError("Verify must be a boolean true/false or a valid path to a file on the system")
            self._verify = value
        else:
            raise ValueError("Verify must be a boolean true/false or a valid path to a file on the system")

    @property
    def database_name(self):
        return self._database_name

    @database_name.setter
    def database_name(self, value):
        if not value or not isinstance(value, str) or value in self._RESERVED_DATABASE_NAMES:
            raise ValueError(
                f"Database Name must be a non empty string, but cannot be one of {self._RESERVED_DATABASE_NAMES}")

        self._database_name = value

    @property
    def collection_name(self):
        return self._collection_name

    @collection_name.setter
    def collection_name(self, value):
        if not value or not isinstance(value, str) or value in self._RESERVED_COLLECTION_NAMES:
            raise ValueError(
                f"Collection Name must be a non empty string, but cannot be one of {self._RESERVED_COLLECTION_NAMES}")

        self._collection_name = value

    def add_token(self, token_object):

        if not isinstance(token_object, Token):
            raise TypeError("LowballArangoDBAuthDB received a non Token Object to add to the database")

        existing_token = self.lookup_token(token_object.token_id)

        if existing_token is not None:
            raise ValueError("Error during token creation. Attempt to create token with existing token id. Try Again.")

        new_document = self.collection.createDocument(token_object.to_dict())
        new_document._key = token_object.token_id
        new_document.save()

    def lookup_token(self, token_id):

        try:
            token_doc = self.collection.fetchDocument(token_id)
        except DocumentNotFoundError:
            return None

        try:
            token = Token(**token_doc.getStore())
            return token
        except:
            token_doc.delete()
        return None

    def revoke_token(self, token_id):

        try:
            token_doc = self.collection.fetchDocument(token_id)
        except DocumentNotFoundError:
            return None

        token_doc.delete()
        return None

    def revoke_all(self):

        self.collection.truncate()

    def list_tokens(self):

        tokens = self.collection.fetchAll()
        token_list = []
        for token_doc in tokens:
            try:
                token = Token(**token_doc.getStore())
                token_list.append(token)
            except:
                token_doc.delete()

        return token_list

    def list_tokens_by_client_id(self, client_id):

        QUERY = f"""
FOR token in {self.collection_name}
FILTER token.cid == @client_id
RETURN token
"""
        bind_vars = {
            "client_id": client_id
        }
        tokens = self.collection.database.AQLQuery(QUERY, bindVars=bind_vars)

        results = []
        for token in tokens:
            try:
                t = Token(**token.getStore())
                results.append(t)
            except:
                token.delete()
        return results

    def list_tokens_by_role(self, role):

        QUERY = f"""
FOR token in {self.collection_name}
FILTER @role in token.r
return token
"""
        bind_vars = {
            "role": role
        }
        tokens = self.collection.database.AQLQuery(QUERY, bindVars=bind_vars)

        results = []
        for token in tokens:
            try:
                t = Token(**token.getStore())
                results.append(t)
            except:
                token.delete()
        return results

    def cleanup_tokens(self):
        QUERY = f"""
FOR token in {self.collection_name}
FILTER token.ets < "{str(self.get_now()).split(".")[0]}"
REMOVE token in {self.collection_name}
"""
        self.collection.database.AQLQuery(QUERY)