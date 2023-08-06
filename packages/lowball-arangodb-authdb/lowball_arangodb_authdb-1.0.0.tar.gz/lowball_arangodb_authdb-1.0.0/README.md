# lowball-arangodb-authdb
A simple Authentication Database implementation of the specification for  [Lowball](https://github.com/EmersonElectricCo/lowball) 
`AuthDatabase` provider leveraging ArangoDB.

## Installation

lowball arangodb authdb has been tested to work with only Python 3.6+ and with ArangoDB Versions 3.4-3.7

```
pip install lowball-arangodb-authdb
```

## Configuration

In the lowball configuration's `auth_db` section, the following fields can be set.
These are the default values, and if you do not wish to change them, they do not need to appear in the configuration. 

```yaml
...
auth_db:
  url: "http://127.0.0.1"
  port: 8529
  user: "root"
  password: 
  verify: true
  database_name: "lowball_authdb"
  collection_name: "authentication_tokens"
...
```

__Field Descriptions__

- url - the full url to the server, including http or https
- port - the port to connect with
- user - the user to authenticate to the arango instance
- password - the password for the user
- verify - Irrelevant for non-TLS connections, true to validate certificates, false to skip validation. 
           Can also be set to a path to a certificate file that will be used for validation.
- database_name - the name to give the database which will hold the collection storing the tokens
- collection_name - the name to give the collection to hold the tokens. 


## Example Usage

```python

from lowball import Lowball, config_from_file
from lowball_arangodb_authdb import LowballArangoDBAuthDB

lowball_config = config_from_file("/path/to/config.yaml")

lowball = Lowball(config=lowball_config, auth_database=LowballArangoDBAuthDB)


```

__Notes__

The authentication database implementation expects to have a collection to itself. Documents it attempts to 
load which do not match the `Token` specification will be deleted.

Multiple Lowball Applications should have no issue interacting with the same ArangoDB backend.







