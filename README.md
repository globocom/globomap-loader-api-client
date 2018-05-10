# GloboMap Loader API Client

Python client for API [Globo Map Core Loader] (https://github.com/globocom/globomap-core-loader)

## Starting Project:

` make setup `

## Running Tests:

` make setup ` (When project not started yet.)<br>
` make tests `

## Example of use:
```python
auth_inst = auth.Auth(
    api_url='http://localhost:5000',
    username='username_api',
    password='password_api'
)
self.update = Update(auth=auth_inst, driver_name='driver_x')
data = {
    "action": "<action>",
    "collection": "<edge_name>",
    "key": "<key>",
    "element": {
    "from": "<id_document>",
    "id": "<id_internal>",
    "name": "<name>",
    "properties": {
        "key_name_1": "value_1",
        "key_name_2": "value_2"
    },
    "properties_metadata": {
        "key_name_1": {
        "description": "description_1"
        },
        "key_name_2": {
        "description": "description_2"
        }
    },
    "provider": "<driver_name>",
    "timestamp": "<timestamp>",
    "to": "<id_document>"
    },
    "type": "edges"
}
res = self.update.post(data)
```

## Licensing

Globo Map API is under [Apache 2 License](./LICENSE)
