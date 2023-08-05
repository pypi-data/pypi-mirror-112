[![Run Tests](https://github.com/acdh-oeaw/nerdpool-client/actions/workflows/test.yml/badge.svg)](https://github.com/acdh-oeaw/nerdpool-client/actions/workflows/test.yml)

[![codecov](https://codecov.io/gh/acdh-oeaw/nerdpool-client/branch/master/graph/badge.svg?token=LXKIMGDXXF)](https://codecov.io/gh/acdh-oeaw/nerdpool-client)

# nerdpool-client

## install

`pip install nerdpool_client`

## usage

### list data set titles


```python

from nerdpool_client import NerdPoolClient

client = NerdPoolClient()
print(client.data_sets)
# ['RTA', 'RITA', 'MRP', 'Chronik Aldersbach', 'DIPKO']
```

