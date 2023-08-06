import pytest
from unittest.mock import Mock, MagicMock, call
from pyArango.connection import Connection
from pyArango.collection import Collection, Collection_metaclass
from pyArango.document import Document
from pyArango.theExceptions import DocumentNotFoundError, CreationError
import pyArango
from pyArango.database import Database
import lowball_arangodb_authdb.authdb
from lowball_arangodb_authdb.authdb import LowballArangoDBAuthDB, AuthenticationCollection
from lowball.models.authentication_models.token import Token
from datetime import datetime
import pathlib
import re

@pytest.fixture(params=[
    "right_length_bad",
    "wronglength",
    "wrongerlengthtoolong",
    ["not", "a", "string"],
    "",
    None,
    {},
    1,
    3,
    ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16"],
    "AGoodTryButNope!"
])
def invalid_token_ids(request):

    return request.param

@pytest.fixture(params=[
    "abcdEFGH13578642",
    "zx73hg5490ljHGHF",
    "asimpletokenidya",
    "4Simpl3T0ken1dyA"
])
def valid_token_ids(request):

    return request.param

@pytest.fixture
def wrapped_re_fullmatch(monkeypatch):

    monkeypatch.setattr(re, "fullmatch", Mock(wraps=re.fullmatch))

@pytest.fixture(params=[
    "short_client_id",
    "different cleint id",
    "CLINET_DI"
])
def nonemptystrings(request):
    return request.param


@pytest.fixture(params=[
    [],
    ["r1", "r2", "r3"],
    ["r1"]
])
def valid_roles(request):
    return request.param


@pytest.fixture(params=[
    "2020-05-10 10:20:30",
    "1991-05-02 16:30:00",
    "2030-12-31 00:00:00"
])
def valid_datetimes(request):

    return request.param



@pytest.fixture(params=[
    "not even close",
    "2020:10:4T00:00:00",
    "2020-13-4 00:00:00",
    "2020-11-4 25:00:00"
])
def invalid_datetimes(request):

    return request.param

@pytest.fixture(
    params=[
        ["not", "string"],
        1234,
        "string.but.missing.specifier",
        "",
        None

    ]
)
def invalid_urls(request):
    return request.param

@pytest.fixture(params=[
    "http://127.0.0.1",
    "https://127.0.0.1",
    "https://any.string"
])
def valid_urls(request):

    return request.param

@pytest.fixture(params=[
    "not integer",
    "40",
    0,
    70000,
    65536,
    7.2,
    None
])
def invalid_ports(request):

    return request.param

@pytest.fixture(params=[
    80,
    443,
    8529,
    8443,
    8080,
    1,
    65535
])
def valid_ports(request):
    return request.param

@pytest.fixture(params=[
    "",
    ["not", "a", "string"],
    None
])
def not_strings_or_empty(request):
    return request.param


@pytest.fixture(params=[
    ["not", "string"],
    1234
])
def just_not_string(request):
    return request.param

@pytest.fixture(params=[
    "",
    "12345",
    None
])
def string_or_none(request):
    return request.param

@pytest.fixture(params=[
    50,
    "not string path",
    ["not", "bool"]
])
def not_bool_or_string_path(request):
    return request.param

@pytest.fixture(params=[
    "/path/to/file.ca",
    "/another/path",
    True,
    False
])
def valid_verify(request, path_does_exist, path_is_file):
    return request.param

@pytest.fixture
def path_does_not_exist(monkeypatch):

    monkeypatch.setattr(pathlib.Path, "exists", Mock(return_value=False))

@pytest.fixture
def path_does_exist(monkeypatch):
    monkeypatch.setattr(pathlib.Path, "exists", Mock(return_value=True))

@pytest.fixture
def path_is_file(monkeypatch):
    monkeypatch.setattr(pathlib.Path, "is_file", Mock(return_value=True))

@pytest.fixture
def path_is_not_file(monkeypatch):
    monkeypatch.setattr(pathlib.Path, "is_file", Mock(return_value=False))

@pytest.fixture(params=[
    "_system",
    "",
    None,
    ["not", "string"],
    1
])
def invalid_database_name(request):
    return request.param

@pytest.fixture(params=[
    "Collection",
    "SystemCollection",
    "Edges",
    "",
    None,
    ["not", "string"],
    1
])
def invalid_collection_name(request):
    return request.param

@pytest.fixture(params=[
    ("http://127.0.0.1", 443, "lowball", "test", False, "db", "toke"),
    ("https://local.arang", 8529, "below", "blaw", True, "daby", "auth")
])
def init_calls_expected_connection(request):

    url, port, user, pw, verify, db_name, col_name = request.param

    return request.param, call(
        arangoURL=f"{url}:{port}",
        username=user,
        password=pw,
        verify=verify
    )

@pytest.fixture
def basic_db_name():
    return 'test'

class TestMockConnection(Connection):

    def __init__(self, *args, **kwargs):
        pass

class TestMockDatabase(Database):

    def __init__(self, *args, **kwargs):
        pass


class TestMockCollection(Collection):

    def __init__(self, *args, **kwargs):
        self.database = TestMockDatabase()

class TestMockDocument(Document):

    def __init__(self, *args, **kwargs):
        self.test_key = None
        self.token_json = None

@pytest.fixture
def mock_init_database(monkeypatch):
    monkeypatch.setattr(LowballArangoDBAuthDB, "_init_database", Mock())

@pytest.fixture
def mock_init_collection(monkeypatch):

    monkeypatch.setattr(LowballArangoDBAuthDB, "_init_collection", Mock())


@pytest.fixture
def basic_mock_pyarango(monkeypatch, basic_mock_connection, basic_mock_database, mock_init_database, mock_init_collection):
    pass


@pytest.fixture
def mock_pyarango(monkeypatch):

    monkeypatch.setattr(lowball_arangodb_authdb.authdb, "Connection", TestMockConnection)
    monkeypatch.setattr(lowball_arangodb_authdb.authdb, "Database", TestMockDatabase)
    monkeypatch.setattr(lowball_arangodb_authdb.authdb, "Collection", TestMockCollection)
    monkeypatch.setattr(lowball_arangodb_authdb.authdb, "Document", TestMockDocument)

@pytest.fixture
def basic_mock_connection(monkeypatch):

    monkeypatch.setattr(TestMockConnection, "__init__", Mock(return_value=None))
    monkeypatch.setattr(TestMockConnection, "createDatabase", Mock(return_value=Mock()))
    monkeypatch.setattr(TestMockConnection, "__getitem__", Mock(return_value=None))

@pytest.fixture
def basic_mock_database(monkeypatch):

    monkeypatch.setattr(TestMockDatabase, "__init__", Mock(return_value=None))

@pytest.fixture
def basic_mock_connection_get_item_db_not_present(monkeypatch, basic_db_name):

    mock = Mock()
    mock.side_effect = KeyError()
    TestMockDatabase.name = basic_db_name
    monkeypatch.setattr(TestMockDatabase, "__init__", Mock(return_value=None))
    monkeypatch.setattr(TestMockConnection, "__init__", Mock(return_value=None))
    monkeypatch.setattr(TestMockConnection, "__getitem__", mock)
    monkeypatch.setattr(TestMockConnection, "createDatabase", Mock(return_value=TestMockDatabase(connection=Mock(), name=basic_db_name)))

@pytest.fixture
def mock_connection_get_item_db_present(monkeypatch, basic_db_name):
    TestMockDatabase.name = basic_db_name
    monkeypatch.setattr(TestMockDatabase, "__init__", Mock(return_value=None))
    monkeypatch.setattr(TestMockConnection, "__init__", Mock(return_value=None))
    monkeypatch.setattr(TestMockConnection, "__getitem__", Mock(return_value=TestMockDatabase(connection=Mock(), name=basic_db_name)))


@pytest.fixture
def mock_database_getitem_collection_not_present(mock_connection_get_item_db_present, monkeypatch):

    def mock_create_collection(className = 'Collection', **colProperties):

        return Collection_metaclass.getCollectionClass(className)(Mock(), colProperties)

    monkeypatch.setattr(TestMockDatabase, "__getitem__", Mock(side_effect=KeyError))
    monkeypatch.setattr(TestMockCollection, "__init__", Mock(return_value=None))
    monkeypatch.setattr(TestMockDatabase, "createCollection", Mock(wraps=mock_create_collection))

@pytest.fixture
def mock_database_getitem_collection_present(mock_connection_get_item_db_present, monkeypatch):

    def mock_get_item(value):

        return Collection_metaclass.getCollectionClass(value)(Mock(), {})

    monkeypatch.setattr(TestMockCollection, "__init__", Mock(return_value=None))
    monkeypatch.setattr(TestMockDatabase, "__getitem__", Mock(wraps=mock_get_item))


@pytest.fixture
def mock_auth_db(monkeypatch):

    monkeypatch.setattr(LowballArangoDBAuthDB, "__init__", Mock(return_value=None))
    LowballArangoDBAuthDB.url = "http://127.0.0.1"
    LowballArangoDBAuthDB.port = 8529
    LowballArangoDBAuthDB.user = "root"
    LowballArangoDBAuthDB.password = None
    LowballArangoDBAuthDB.verify = True
    LowballArangoDBAuthDB.database_name = "lowball_authdb"
    LowballArangoDBAuthDB.collection_name = "authentication_tokens"
    LowballArangoDBAuthDB.collection = TestMockCollection()


@pytest.fixture
def mocked_document(monkeypatch):

    # mock the following
    # TestMockDocument.getStore
    # TestMockDocument.save
    # TestMockDocument.delete
    def mock_doc_get_store(self):

        return self.token_json

    monkeypatch.setattr(TestMockDocument, "delete", Mock())
    monkeypatch.setattr(TestMockDocument, "save", Mock())
    monkeypatch.setattr(TestMockDocument, "getStore", mock_doc_get_store)


@pytest.fixture(params=[
    0,
    1,
    2,
    3,
    4,
    5,
    6,
    7
])
def token_ids(test_token_id1, test_token_id2, test_token_id3, test_token_id4, test_token_id5, test_token_id6, test_token_id7, test_token_id8, request):

    return [
        test_token_id1,
        test_token_id2,
        test_token_id3,
        test_token_id4,
        test_token_id5,
        test_token_id6,
        test_token_id7,
        test_token_id8
    ][request.param]


@pytest.fixture(params=[
    0,
    1,
    2,
    3,
    4,
    5
])
def present_token_ids(test_token_id1, test_token_id2, test_token_id3, test_token_id4, test_token_id5, test_token_id7, request):

    return [
        test_token_id1,
        test_token_id2,
        test_token_id3,
        test_token_id4,
        test_token_id5,
        test_token_id7,

    ][request.param]


@pytest.fixture
def token_dict_map(
        basic_user1_test_token1,
        basic_user1_test_token2,
        basic_user2_test_token1,
        basic_user2_test_token2,
        admin_user1_test_token1,
        admin_user2_test_token1
        ):
    token_dict_map = {
        basic_user1_test_token1.token_id: basic_user1_test_token1.to_dict(),
        basic_user1_test_token2.token_id: basic_user1_test_token2.to_dict(),
        basic_user2_test_token1.token_id: basic_user2_test_token1.to_dict(),
        basic_user2_test_token2.token_id: basic_user2_test_token2.to_dict(),
        admin_user1_test_token1.token_id: admin_user1_test_token1.to_dict(),
        admin_user2_test_token1.token_id: admin_user2_test_token1.to_dict(),

    }
    return token_dict_map


@pytest.fixture
def mock_filled_token_collection(
        monkeypatch,
        token_dict_map,
        mocked_document
        ):

    # mock the following
    # TestMockCollection.__getitem__
    # TestMockCollection.fetchDocument
    # TestMockCollection.fetchAll

    def mock_collection_getitem(key):

        token_dict = token_dict_map.get(key)

        if token_dict:
            document = TestMockDocument()
            document.token_json = token_dict
            document.test_key = key
            return document
        else:
            raise DocumentNotFoundError("not found")

    def mock_collection_fetch_document(key, *args, **kwargs):
        token_dict = token_dict_map.get(key)

        if token_dict:
            document = TestMockDocument()
            document.token_json = token_dict
            document.test_key = key
            return document
        else:
            raise DocumentNotFoundError("not found")

    def mock_collection_fetch_all():

        results = []
        for key, token_dict in token_dict_map.items():
            doc = TestMockDocument()
            doc.test_key = key
            doc.token_json = token_dict
            results.append(doc)
        return results

    monkeypatch.setattr(TestMockCollection, "fetchDocument", Mock(wraps=mock_collection_fetch_document))
    monkeypatch.setattr(TestMockCollection, "__getitem__", Mock(wraps=mock_collection_getitem))
    monkeypatch.setattr(TestMockCollection, "fetchAll", Mock(wraps=mock_collection_fetch_all))
    monkeypatch.setattr(TestMockCollection, "truncate", Mock())

@pytest.fixture
def mock_filled_token_collection_bad_values(token_dict_map, monkeypatch, mocked_document):

    token_dict_map["badvalue1"] = {
        "invalid_value": "yep"
    }
    token_dict_map["badvalue2"] = {
        "invalid_value_again": "yep"
    }

    def mock_collection_getitem(key):

        token_dict = token_dict_map.get(key)

        if token_dict:
            document = TestMockDocument()
            document.token_json = token_dict
            document.test_key = key
            return document
        else:
            raise DocumentNotFoundError("not found")

    def mock_collection_fetch_document(key, *args, **kwargs):
        token_dict = token_dict_map.get(key)

        if token_dict:
            document = TestMockDocument()
            document.token_json = token_dict
            document.test_key = key
            return document
        else:
            raise DocumentNotFoundError("not found")

    def mock_collection_fetch_all():

        results = []
        for key, token_dict in token_dict_map.items():
            doc = TestMockDocument()
            doc.test_key = key
            doc.token_json = token_dict
            results.append(doc)
        return results

    monkeypatch.setattr(TestMockCollection, "fetchDocument", Mock(wraps=mock_collection_fetch_document))
    monkeypatch.setattr(TestMockCollection, "__getitem__", Mock(wraps=mock_collection_getitem))
    monkeypatch.setattr(TestMockCollection, "fetchAll", Mock(wraps=mock_collection_fetch_all))


@pytest.fixture
def mock_document_save_no_issues(monkeypatch):

    monkeypatch.setattr(TestMockDocument, "save", Mock())


@pytest.fixture
def mock_document_save_creation_error(monkeypatch):
    monkeypatch.setattr(TestMockDocument, "save", Mock(raises=CreationError))

@pytest.fixture
def mock_document_delete(monkeypatch):
    monkeypatch.setattr(TestMockDocument, "delete", Mock())

@pytest.fixture
def mock_collection_create_document_all_good(monkeypatch):
    monkeypatch.setattr(TestMockCollection, "createDocument", Mock(return_value=TestMockDocument()))


@pytest.fixture
def fetch_document_returns_bad_token_data(mock_filled_token_collection, monkeypatch):

    doc = TestMockDocument()
    doc.token_json = {
        "invalid": "structure"
    }
    monkeypatch.setattr(TestMockCollection, "fetchDocument", Mock(return_value=doc))

###############
# TOKEN STUFF #
###############
@pytest.fixture
def basic_user_id1():

    return "user1"


@pytest.fixture
def basic_user_id2():
    return "user2"


@pytest.fixture
def admin_user_id1():
    return "admin1"


@pytest.fixture
def admin_user_id2():
    return "admin2"


@pytest.fixture
def test_token_id1():

    return "a" * 16


@pytest.fixture
def test_token_id2():
    return "b" * 16


@pytest.fixture
def test_token_id3():
    return "c" * 16


@pytest.fixture
def test_token_id4():
    return "d" * 16


@pytest.fixture
def test_token_id5():
    return "e" * 16


@pytest.fixture
def test_token_id6():
    return "f" * 16


@pytest.fixture
def test_token_id7():
    return "g" * 16


@pytest.fixture
def test_token_id8():
    return "h" * 16


@pytest.fixture
def admin_role():
    return "admin"


@pytest.fixture
def test_role1():
    return "r1"


@pytest.fixture
def test_role2():
    return "r2"


@pytest.fixture
def basic_user1_test_token1(test_token_id1, admin_user_id1, basic_user_id1):

    return Token(
        cid=basic_user_id1,
        r=[],
        cts=datetime(2021, 1, 1),
        ets=datetime(2021, 2, 1),
        rcid=admin_user_id1,
        tid=test_token_id1
    )

@pytest.fixture
def basic_user1_test_token2(test_token_id2, admin_user_id1, basic_user_id1, test_role1):

    return Token(
        cid=basic_user_id1,
        r=[test_role1],
        cts=datetime(2021, 1, 1),
        ets=datetime(2021, 2, 1),
        rcid=admin_user_id1,
        tid=test_token_id2
    )

@pytest.fixture
def basic_user2_test_token1(test_token_id3, admin_user_id2, basic_user_id2, test_role1):

    return Token(
        cid=basic_user_id2,
        r=[test_role1],
        cts=datetime(2021, 1, 1),
        ets=datetime(2021, 2, 1),
        rcid=admin_user_id2,
        tid=test_token_id3
    )


@pytest.fixture
def basic_user2_test_token2(test_token_id4, admin_user_id1, basic_user_id2, test_role1, test_role2):

    return Token(
        cid=basic_user_id2,
        r=[test_role1, test_role2],
        cts=datetime(2021, 1, 1),
        ets=datetime(2021, 2, 1),
        rcid=admin_user_id1,
        tid=test_token_id4
    )


@pytest.fixture
def admin_user1_test_token1(test_token_id5, admin_user_id1, admin_role):

    return Token(
        cid=admin_user_id1,
        r=[admin_role],
        cts=datetime(2021, 1, 1),
        ets=datetime(2021, 2, 1),
        rcid=admin_user_id1,
        tid=test_token_id5
    )


@pytest.fixture
def admin_user1_test_token2(test_token_id6, admin_user_id1, admin_role, test_role1):

    return Token(
        cid=admin_user_id1,
        r=[admin_role, test_role1],
        cts=datetime(2021, 1, 1),
        ets=datetime(2021, 2, 1),
        rcid=admin_user_id1,
        tid=test_token_id6
    )


@pytest.fixture
def admin_user2_test_token1(test_token_id7, admin_user_id2, admin_role):

    return Token(
        cid=admin_user_id2,
        r=[admin_role],
        cts=datetime(2021, 1, 1),
        ets=datetime(2021, 2, 1),
        rcid=admin_user_id2,
        tid=test_token_id7
    )


@pytest.fixture
def admin_user2_test_token2(test_token_id8, admin_user_id2, admin_role, test_role1):

    return Token(
        cid=admin_user_id2,
        r=[admin_role, test_role1],
        cts=datetime(2021, 1, 1),
        ets=datetime(2021, 2, 1),
        rcid=admin_user_id2,
        tid=test_token_id8
    )

@pytest.fixture
def list_tokens_by_client_id_request_response(
        basic_user1_test_token1,
        basic_user1_test_token2,
        basic_user_id1,
        monkeypatch
):

    response = [basic_user1_test_token1, basic_user1_test_token2]
    response_documents = []
    for token in response:
        doc = TestMockDocument()
        doc.token_json = token.to_dict()
        doc.test_key = token.token_id
        response_documents.append(doc)
    bad_doc = TestMockDocument()
    bad_doc.token_json = {
        "bad_value": "not token"
    }
    bad_doc.test_key = "bigbaddoc"
    response_documents.append(bad_doc)
    monkeypatch.setattr(TestMockDatabase, "AQLQuery", Mock(return_value=response_documents))
    return basic_user_id1, response

@pytest.fixture
def list_tokens_by_role_request_response(
        basic_user1_test_token1,
        basic_user1_test_token2,
        basic_user2_test_token1,
        basic_user2_test_token2,
        admin_user1_test_token1,
        admin_user2_test_token1,
        admin_role,
        test_role1,
        test_role2,
        monkeypatch
):

    response = [admin_user1_test_token1, admin_user2_test_token1]
    response_documents = []
    for token in response:
        doc = TestMockDocument()
        doc.token_json = token.to_dict()
        doc.test_key = token.token_id
        response_documents.append(doc)

    bad_doc = TestMockDocument()
    bad_doc.token_json = {
        "bad_value": "not token"
    }
    bad_doc.test_key = "bigbaddoc"
    response_documents.append(bad_doc)
    monkeypatch.setattr(TestMockDatabase, "AQLQuery", Mock(return_value=response_documents))
    return admin_role, response


@pytest.fixture
def fake_utcnow(monkeypatch):
    from datetime import datetime
    now = datetime.utcnow()
    monkeypatch.setattr(LowballArangoDBAuthDB, "get_now", Mock(return_value=now))
    return now

@pytest.fixture
def simple_mock_aql_query(monkeypatch):
    monkeypatch.setattr(TestMockDatabase, "AQLQuery", Mock(return_value=[]))
