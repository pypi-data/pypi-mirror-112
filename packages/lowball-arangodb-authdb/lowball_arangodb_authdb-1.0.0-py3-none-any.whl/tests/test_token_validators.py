
"""According to https://github.com/ArangoDB-Community/pyArango/blob/dev/README.rst

Validators must Inherit Validator and implement a validate function
which returns True or raises a Validation Error

"""
import pytest
from pyArango.validation import ValidationError
from lowball_arangodb_authdb.token_validators import TokenIDValidator, ClientIDValidator, TimestampValidator, \
    RolesValidator
from lowball.models.authentication_models.token import TOKEN_ID_PATTERN, Token
import re
from datetime import datetime

class TestTokenIDValidator:

    def test_validate_raises_validation_error_for_invalid_token_ids_that_dont_match_token_regex(self, invalid_token_ids,
                                                                                                wrapped_re_fullmatch):
        validator = TokenIDValidator()
        with pytest.raises(ValidationError):
            validator.validate(invalid_token_ids)

        re.fullmatch.assert_called_once_with(TOKEN_ID_PATTERN, invalid_token_ids)

    def test_validate_returns_true_for_valid_token_ids(self, valid_token_ids, wrapped_re_fullmatch):
        validator = TokenIDValidator()

        assert validator.validate(valid_token_ids) == True
        re.fullmatch.assert_called_once_with(TOKEN_ID_PATTERN, valid_token_ids)


class TestClientIDValidator:

    def test_validate_raises_validation_error_for_non_string_client_ids(self):

        validator = ClientIDValidator()

        with pytest.raises(ValidationError):
            validator.validate(["not", "string"])

        with pytest.raises(ValidationError):
            validator.validate(None)

        with pytest.raises(ValidationError):
            validator.validate(12345)

    def test_validate_raises_validation_error_for_empty_client_id(self):
        validator = ClientIDValidator()

        with pytest.raises(ValidationError):
            validator.validate("")

    def test_validate_returns_true_for_nonempty_strings(self, nonemptystrings):
        validator = ClientIDValidator()

        assert validator.validate(nonemptystrings) == True


class TestRolesValidator:

    def test_validate_raises_validation_error_when_roles_is_not_list(self):

        validator = RolesValidator()

        with pytest.raises(ValidationError):
            validator.validate(None)

        with pytest.raises(ValidationError):
            validator.validate(1234)

        with pytest.raises(ValidationError):
            validator.validate("still not a list")

    def test_validate_raises_validation_error_when_roles_in_list_are_not_strings(self):
        validator = RolesValidator()


        with pytest.raises(ValidationError):
            validator.validate([1,2,3,4])

        with pytest.raises(ValidationError):
            validator.validate(["string", "string again", 1])

    def test_validate_returns_true_for_list_of_strings_or_empty_list(self, valid_roles):
        validator = RolesValidator()

        assert validator.validate(valid_roles) == True


class TestTimestampValidator:

    # From lowball.models.authentication_models.token.Token

    FORMAT = "%Y-%m-%d %H:%M:%S"

    def test_validate_raises_validation_error_when_value_not_string(self):
        validator = TimestampValidator()

        with pytest.raises(ValidationError):
            validator.validate(["not", "string"])

        with pytest.raises(ValidationError):
            validator.validate(None)

        with pytest.raises(ValidationError):
            validator.validate(12345)

    def test_validate_raises_validation_error_when_string_is_incorrect_date_format(self, invalid_datetimes):
        validator = TimestampValidator()

        with pytest.raises(ValidationError):
            validator.validate(invalid_datetimes)

    def test_validate_returns_true_for_strings_with_correct_date_format(self, valid_datetimes):

        validator = TimestampValidator()

        assert validator.validate(valid_datetimes) == True


