import lowball_arangodb_authdb.authdb
import pytest

from lowball_arangodb_authdb.authdb import LowballArangoDBAuthDB, AuthenticationCollection
from unittest.mock import call
import pyArango
from pyArango.connection import Connection
from pyArango.collection import Collection, Collection_metaclass
from pyArango.database import Database
from pyArango.document import Document
from lowball.models.authentication_models import Token

class TestAuthDBInit:
    """Tests:

    initialization with connection object,
    initial database setup if it doesnt exist
    defaults for everything

    Parameters:
        arango_url="http://127.0.0.1"
        arango_port=8529
        user="root"
        password=None
        verify=True
        database_name="lowball"
        collection_name="authentication_tokens"

    arango_url should include http:// or https://, i think we rely on the connection class to validate any further here

    arango_port should be valid integer

    user: string (non empty)
    password: string/none

    verify: boolean OR string -> path to ca

    database_name: string

    collection_name: string


    _key = token id

    I think we can keep this implementation low level meaning, not creating high level of abstraction. Tokens should
    be immutable once created

    Should setup Validators for the token documents in the collection

    Alright, validators are interesting. So we set them in a Collection class
    definition. It seems that when we db.createCollection

    Document objects??? I don't think so, should be able to translate back
    and forth between a doc and a Token object with ease

    looks like we should be able to leverage their metaclass setup by using this

    Collection_metaclass.collectionClasses["desired_collection_name"] = OurClass
    Looks like to preserve structure we need to restrict their names from Collection, SystemCollection, and Edges,
    but anything else is fair game
    """

    def test_init_sets_expected_defaults(self, basic_mock_pyarango, mock_pyarango):

        authdb = LowballArangoDBAuthDB()

        assert authdb.url == "http://127.0.0.1"
        assert authdb.port == 8529
        assert authdb.user == "root"
        assert authdb.password == None
        assert authdb.verify == True
        assert authdb.database_name == "lowball_authdb"
        assert authdb.collection_name == "authentication_tokens"

    def test_init_accepts_expected_kwargs(self, basic_mock_pyarango, mock_pyarango):

        authdb = LowballArangoDBAuthDB(
            url="https://local.arango",
            port=8080,
            user="lowball",
            password="supersafe",
            verify=False,
            database_name="authdb",
            collection_name="token_store",
        )

        assert authdb.url == "https://local.arango"
        assert authdb.port == 8080
        assert authdb.user == "lowball"
        assert authdb.password == "supersafe"
        assert authdb.verify == False
        assert authdb.database_name == "authdb"
        assert authdb.collection_name == "token_store"

    # test validation of arango url parameter beyond making sure it's a string with http/https in front
    def test_arango_url_error_if_not_string_or_missing_http_specifier(self,
                                                                      invalid_urls,
                                                                      mock_pyarango,
                                                                      basic_mock_pyarango):

        with pytest.raises(ValueError):
            LowballArangoDBAuthDB(url=invalid_urls)

    def test_arango_url_no_error_if_set_correctly(self,
                                                  valid_urls,
                                                  mock_pyarango,
                                                  basic_mock_pyarango):
        authdb = LowballArangoDBAuthDB(url=valid_urls)
        assert authdb.url == valid_urls

    def test_validation_of_arango_port_parameter_as_integer_as_valid_port_number(self,
                                                                                 invalid_ports,
                                                                                 mock_pyarango,
                                                                                 basic_mock_pyarango):
        with pytest.raises(ValueError):
            LowballArangoDBAuthDB(port=invalid_ports)

    def test_arango_port_no_error_when_correct_ports(self,
                                                     valid_ports,
                                                     mock_pyarango,
                                                     basic_mock_pyarango):
        authdb = LowballArangoDBAuthDB(port=valid_ports)
        assert authdb.port == valid_ports

    def test_validation_of_arango_user_parameter_nonempty_string(self,
                                                                 not_strings_or_empty,
                                                                 mock_pyarango,
                                                                 basic_mock_pyarango):
        with pytest.raises(ValueError):
            LowballArangoDBAuthDB(user=not_strings_or_empty)

    def test_arango_user_no_error_when_nonempty_string(self,
                                                       nonemptystrings,
                                                       mock_pyarango,
                                                       basic_mock_pyarango):
        authdb = LowballArangoDBAuthDB(user=nonemptystrings)
        assert authdb.user == nonemptystrings

    def test_validation_of_arango_password_parameter_is_string_or_none(self,
                                                                       just_not_string,
                                                                       mock_pyarango,
                                                                       basic_mock_pyarango):
        with pytest.raises(ValueError):
            LowballArangoDBAuthDB(password=just_not_string)

    def test_arango_password_no_error_when_string_or_none(self,
                                                          string_or_none,
                                                          mock_pyarango,
                                                          basic_mock_pyarango):
        authdb = LowballArangoDBAuthDB(password=string_or_none)
        assert authdb.password == string_or_none

    def test_validation_of_verify_parameter_when_not_bool_or_string_path_file(self,
                                                                              not_bool_or_string_path,
                                                                              mock_pyarango,
                                                                              basic_mock_pyarango):
        with pytest.raises(ValueError):
            LowballArangoDBAuthDB(verify=not_bool_or_string_path)

    def test_validation_of_verify_parameter_when_path_does_not_exist(self,
                                                                     path_does_not_exist,
                                                                     mock_pyarango,
                                                                     basic_mock_pyarango):

        with pytest.raises(ValueError):
            LowballArangoDBAuthDB(verify="/non_existent/path")

    def test_validation_of_verify_parameter_when_path_does_exist_but_is_not_a_file(self,
                                                                                   path_does_exist,
                                                                                   path_is_not_file,
                                                                                   mock_pyarango,
                                                                                   basic_mock_pyarango):
        with pytest.raises(ValueError):
            LowballArangoDBAuthDB(verify="/non_existent/file_path")

    def test_verify_no_error_when_bool_or_string_path_that_exists(self,
                                                                  valid_verify,
                                                                  mock_pyarango,
                                                                  basic_mock_pyarango):

        authdb = LowballArangoDBAuthDB(verify=valid_verify)
        assert authdb.verify == valid_verify

    def test_validation_of_database_name_parameter_if_not_string_or_system_db(self,
                                                                              invalid_database_name,
                                                                              mock_pyarango,
                                                                              basic_mock_pyarango):
        with pytest.raises(ValueError):
            LowballArangoDBAuthDB(database_name=invalid_database_name)

    def test_database_name_when_string_but_not_system(self,
                                                      nonemptystrings,
                                                      mock_pyarango,
                                                      basic_mock_pyarango):
        authdb = LowballArangoDBAuthDB(database_name=nonemptystrings)
        assert authdb.database_name == nonemptystrings

    def test_validation_of_collection_name_parameter_if_not_string_or_reserved_name(self,
                                                                                    invalid_collection_name,
                                                                                    mock_pyarango,
                                                                                    basic_mock_pyarango):
        with pytest.raises(ValueError):
            LowballArangoDBAuthDB(collection_name=invalid_collection_name)

    def test_collection_name_when_string_but_not_reserved(self,
                                                          mock_pyarango,
                                                          nonemptystrings,
                                                          basic_mock_pyarango):
        authdb = LowballArangoDBAuthDB(collection_name=nonemptystrings)
        assert authdb.collection_name == nonemptystrings

    def test_arango_connection_created_correctly(self, mock_pyarango, init_calls_expected_connection,
                                                 basic_mock_pyarango,
                                                 basic_mock_connection):

        params, expected_call = init_calls_expected_connection

        auth_db = LowballArangoDBAuthDB(*params)

        auth_db.connection.__init__.assert_has_calls([expected_call])

    def test_authentication_database_created_if_not_present(self,
                                                            mock_pyarango,
                                                            basic_mock_connection_get_item_db_not_present,
                                                            mock_init_collection,
                                                            basic_db_name):

        authdb = LowballArangoDBAuthDB(database_name=basic_db_name)
        authdb.connection.__getitem__.assert_called_once_with(basic_db_name)
        authdb.connection.createDatabase.assert_called_once_with(name=basic_db_name)

        assert isinstance(authdb.database, Database)
        assert authdb.database.name == basic_db_name

    def test_authentication_database_accessed_if_present(self,
                                                         mock_pyarango,
                                                         basic_db_name,
                                                         mock_init_collection,
                                                         mock_connection_get_item_db_present):
        authdb = LowballArangoDBAuthDB(database_name=basic_db_name)
        authdb.connection.__getitem__.assert_called_once_with(basic_db_name)

        assert isinstance(authdb.database, Database)
        assert authdb.database.name == basic_db_name


    def test_named_authentication_collection_is_correctly_set(self,
                                                              mock_pyarango,
                                                              basic_db_name,
                                                              mock_connection_get_item_db_present,
                                                              mock_init_database,
                                                              mock_init_collection,
                                                              nonemptystrings
                                                              ):
        authdb = LowballArangoDBAuthDB(collection_name=nonemptystrings)

        assert Collection_metaclass.collectionClasses.get(nonemptystrings) == AuthenticationCollection


    def test_authentication_collection_created_if_not_present(self,
                                                              mock_pyarango,
                                                              mock_database_getitem_collection_not_present,
                                                              nonemptystrings
                                                              ):
        authdb = LowballArangoDBAuthDB(collection_name=nonemptystrings)

        authdb.database.__getitem__.assert_called_once_with(nonemptystrings)
        authdb.database.createCollection.assert_called_once_with(authdb.collection_name, waitForSync=True)
        assert isinstance(authdb.collection, AuthenticationCollection)

    def test_authentication_collection_accessed_if_present(self,
                                                           mock_pyarango,
                                                           mock_database_getitem_collection_present,
                                                           nonemptystrings):

        authdb = LowballArangoDBAuthDB(collection_name=nonemptystrings)

        authdb.database.__getitem__.assert_called_once_with(nonemptystrings)
        assert isinstance(authdb.collection, AuthenticationCollection)


class TestAddToken:

    def test_error_when_not_given_token_object(self, mock_auth_db):

        authdb = LowballArangoDBAuthDB()

        with pytest.raises(TypeError):
            authdb.add_token("string")

        with pytest.raises(TypeError):
            authdb.add_token(None)

        with pytest.raises(TypeError):
            authdb.add_token([])

    def test_failure_when_token_with_token_id_already_exists(self, mock_auth_db, basic_user1_test_token1, mocked_document,
                                                             mock_filled_token_collection):

        authdb = LowballArangoDBAuthDB()

        with pytest.raises(ValueError):
            authdb.add_token(basic_user1_test_token1)

    def test_add_token_calls_create_document_with_token_dictionary_sets_key_and_saves(self,
                                                                                      mock_auth_db,
                                                                                      mock_pyarango,
                                                                                      admin_user1_test_token2,
                                                                                      mock_filled_token_collection,
                                                                                      mock_collection_create_document_all_good,
                                                                                      mock_document_save_no_issues
                                                                                      ):
        authdb = LowballArangoDBAuthDB()

        authdb.add_token(admin_user1_test_token2)

        authdb.collection.createDocument.assert_called_once_with(admin_user1_test_token2.to_dict())

        # have to go this deep because of the way we mock
        lowball_arangodb_authdb.authdb.Document.save.assert_called_once()


class TestLookupToken:

    def test_returns_none_when_token_not_found(self,
                                               test_token_id6,
                                               mock_pyarango,
                                               mock_filled_token_collection,
                                               mock_auth_db
                                               ):

        authdb = LowballArangoDBAuthDB()

        token = authdb.lookup_token(test_token_id6)
        authdb.collection.fetchDocument.assert_called_once_with(test_token_id6)
        assert token is None

    def test_deletes_token_if_token_information_cannot_be_loaded_into_token_when_found(self, mock_pyarango,
                                                                                       mock_auth_db,
                                                                                       fetch_document_returns_bad_token_data,
                                                                                       mock_document_delete
                                                                                       ):
        authdb = LowballArangoDBAuthDB()

        token = authdb.lookup_token("doesntmatter")
        assert token is None
        authdb.collection.fetchDocument.assert_called_once_with("doesntmatter")
        lowball_arangodb_authdb.authdb.Document.delete.assert_called_once()

    def test_returns_token_object_when_token_document_found(self,
                                                            mock_pyarango,
                                                            mock_filled_token_collection,
                                                            mock_auth_db,
                                                            test_token_id5,
                                                            admin_user1_test_token1
                                                            ):
        authdb = LowballArangoDBAuthDB()

        token = authdb.lookup_token(test_token_id5)
        assert isinstance(token, Token)
        assert token.to_dict() == admin_user1_test_token1.to_dict()

        authdb.collection.fetchDocument.assert_called_once_with(test_token_id5)


class TestRevokeToken:

    def test_returns_none(self,
                          mock_pyarango,
                          mock_auth_db,
                          mock_filled_token_collection,
                          token_ids
                          ):
        authdb = LowballArangoDBAuthDB()

        assert authdb.revoke_token(token_ids) is None
        authdb.collection.fetchDocument.assert_called_once_with(token_ids)


    def test_calls_delete_on_token_document_when_found(self,
                                                       mock_pyarango,
                                                       mock_auth_db,
                                                       mock_filled_token_collection,
                                                       mock_document_delete,
                                                       present_token_ids
                                                       ):
        authdb = LowballArangoDBAuthDB()
        assert authdb.revoke_token(present_token_ids) is None
        authdb.collection.fetchDocument.assert_called_once_with(present_token_ids)
        lowball_arangodb_authdb.authdb.Document.delete.assert_called_once()


class TestRevokeAll:

    def test_calls_revoke_all_on_the_collection(self,
                                                           mock_pyarango,
                                                           mock_auth_db,
                                                           mock_filled_token_collection,
                                                           mock_document_delete
                                                           ):

        authdb = LowballArangoDBAuthDB()
        assert authdb.revoke_all() is None
        authdb.collection.truncate.assert_called_once()

class TestListTokens:

    def test_returns_list_of_token_objects(self,
                                           mock_pyarango,
                                           mock_auth_db,
                                           mock_filled_token_collection,
                                           basic_user1_test_token1,
                                           basic_user1_test_token2,
                                           basic_user2_test_token1,
                                           basic_user2_test_token2,
                                           admin_user1_test_token1,
                                           admin_user2_test_token1,
                                           ):

        authdb = LowballArangoDBAuthDB()
        result = authdb.list_tokens()
        assert isinstance(result, list)
        assert all(isinstance(item, Token) for item in result)

        assert basic_user1_test_token1 in result
        assert basic_user1_test_token2 in result
        assert basic_user2_test_token2 in result
        assert basic_user2_test_token2 in result
        assert admin_user1_test_token1 in result
        assert admin_user2_test_token1 in result

        assert len(result) == 6

    def test_calls_delete_on_any_document_which_fails_to_load_into_a_token_object(self,
                                                                                  mock_pyarango,
                                                                                  mock_auth_db,
                                                                                  mock_filled_token_collection_bad_values,
                                                                                  basic_user1_test_token1,
                                                                                  basic_user1_test_token2,
                                                                                  basic_user2_test_token1,
                                                                                  basic_user2_test_token2,
                                                                                  admin_user1_test_token1,
                                                                                  admin_user2_test_token1,
                                                                                  ):
        authdb = LowballArangoDBAuthDB()
        result = authdb.list_tokens()
        assert isinstance(result, list)
        assert all(isinstance(item, Token) for item in result)

        assert basic_user1_test_token1 in result
        assert basic_user1_test_token2 in result
        assert basic_user2_test_token2 in result
        assert basic_user2_test_token2 in result
        assert admin_user1_test_token1 in result
        assert admin_user2_test_token1 in result

        assert len(result) == 6
        # bad values adds two bad values to the dictionary
        assert lowball_arangodb_authdb.authdb.Document.delete.call_count == 2

class TestListTokensByClientID:
    """Should expect an aql query here.
    We will probably build a constructor utility function to build it properly

    I know we want to parameterize the query

    """

    QUERY = """
FOR token in {}
FILTER token.cid == @client_id
RETURN token
"""

    def test_calls_query_as_expected_and_cleans_up_bad_tokens(self,
                                           mock_pyarango,
                                           mock_auth_db,
                                           mock_filled_token_collection,
                                           mock_document_delete,
                                           list_tokens_by_client_id_request_response
                                           ):

        authdb = LowballArangoDBAuthDB()
        expected_query = self.QUERY.format(authdb.collection_name)

        client_id, expected_response = list_tokens_by_client_id_request_response

        expected_bind_vars = {
            "client_id": client_id
        }

        results = authdb.list_tokens_by_client_id(client_id)

        assert all(token in results for token in expected_response) and all(token in expected_response for token in results)
        authdb.collection.database.AQLQuery.assert_called_once_with(expected_query, bindVars=expected_bind_vars)
        lowball_arangodb_authdb.authdb.Document.delete.assert_called_once()


class TestListTokensByRole:
    """This may be an aql queryable option as well, will hae to investigate

    """

    QUERY = """
FOR token in {}
FILTER @role in token.r
return token
"""

    def test_calls_query_as_expected_and_cleans_up_bad_tokens(self,
                                                              mock_pyarango,
                                                              mock_auth_db,
                                                              mock_filled_token_collection,
                                                              mock_document_delete,
                                                              list_tokens_by_role_request_response
                                                              ):
        authdb = LowballArangoDBAuthDB()
        expected_query = self.QUERY.format(authdb.collection_name)

        role, expected_response = list_tokens_by_role_request_response

        expected_bind_vars = {
            "role": role
        }

        results = authdb.list_tokens_by_role(role)

        assert all(token in results for token in expected_response) and all(
            token in expected_response for token in results)
        authdb.collection.database.AQLQuery.assert_called_once_with(expected_query, bindVars=expected_bind_vars)
        lowball_arangodb_authdb.authdb.Document.delete.assert_called_once()


class TestCleanupTokens:
    """i believe this is again an aql query we can do

    """
    QUERY = """
FOR token in {}
FILTER token.ets < "{}"
REMOVE token in {}
"""
    def test_aql_query_called_with_correct_inputs(self,
                                                  fake_utcnow,
                                                  simple_mock_aql_query,
                                                  mock_pyarango,
                                                  mock_auth_db
                                                  ):
        authdb = LowballArangoDBAuthDB()
        now = fake_utcnow
        search_date = str(now).split(".")[0]
        expected_query = self.QUERY.format(authdb.collection_name, search_date, authdb.collection_name)

        authdb.cleanup_tokens()

        authdb.collection.database.AQLQuery.assert_called_once_with(expected_query)
