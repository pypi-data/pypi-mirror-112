from pyArango.validation import Validator, ValidationError
from lowball.models.authentication_models.token import TOKEN_ID_PATTERN
import re
from datetime import datetime

class TokenIDValidator(Validator):
    """Simple Validator to make sure the token id
    is checked against lowball's token id format

    """

    validation_message = f"Token ID Must match {TOKEN_ID_PATTERN}"

    def validate(self, value):

        try:
            result = re.fullmatch(TOKEN_ID_PATTERN, value)
        except:
            result = None
        if not result:
            raise ValidationError(self.validation_message)
        return True


class ClientIDValidator(Validator):
    """Simple validator to make sure the
    client id and requesting client id are
    valid strings that are nonempty

    """
    validation_message = "Client ID must be a non empty string"

    def validate(self, value):

        if not isinstance(value, str) or not value:
            raise ValidationError(self.validation_message)
        return True


class TimestampValidator(Validator):
    """simple validator to ensure that the
    creation and expiration timestamps are in
    the correct format

    """
    FORMAT = "%Y-%m-%d %H:%M:%S"

    validation_message = f"Timestamps must be strings of the format {FORMAT}"

    def validate(self, value):
        if not isinstance(value, str):
            raise ValidationError(self.validation_message)

        try:
            t = datetime.strptime(value, self.FORMAT)
        except:
            raise ValidationError(f"Timestamps must be strings of the format {self.FORMAT}")
        return True

class RolesValidator(Validator):
    """simple validator to ensure that the
    roles field is a list of strings

    """
    validation_message = "Roles must be an empty list or a list of strings"
    def validate(self, value):

        if not isinstance(value, list) or not all(isinstance(element, str) for element in value):
            raise ValidationError(self.validation_message)

        return True


