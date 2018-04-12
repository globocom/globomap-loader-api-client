# GloboMap Loader API Client

Python client for [GloboMap Loader API](https://github.com/globocom/globomap-core-loader/blob/master/doc/api.md)

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
self.update = Update(auth=auth_inst, driver_name='aclapi')

res = self.update.post(data)
```

## Licensing

Globo Map API is under [Apache 2 License](./LICENSE)
