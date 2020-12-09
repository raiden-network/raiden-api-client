# raiden api client

The raiden api client wraps the API of [raiden](https://github.com/raiden-network/raiden). It simplifies the usage of [raiden's api](https://docs.raiden.network/raiden-api-1/resources) to a few lines.


## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install raiden API client.

```bash
pip install raiden_api_client
```

## Usage

```python
import raiden_api_client

raiden = raiden_api_client.RaidenAPIWrapper(ip="localhost", port=8545) # Parity running at localhost:8545

raiden.transfer(
   partner = "0x0000000000000000000000000000000000000000",
   amount = 1,
) # Transfering 1 Token to 0x00
```
Further examples can be found in the example folder.

### Available Methods


```python
- mint_tokens(receiver, token, amount) -> AttrDict
- register_token(token) -> AttrDict
- open_channel(partner, token, deposit, settle_timeout=500) -> AttrDict
- transfer(partner, token, amount, identifier=None ) -> AttrDict
- fund_channel(partner, token, deposit) -> AttrDict
- close_channel(partner, token) -> AttrDict
- leave_token_network(token) -> List[str]

- get_channels(token=None, partner=None) -> List[AttrDict]
- get_payments(partner=None, token=None) -> List[AttrDict]
- get_token_network(token=None) -> AttrDict
- get_raiden_version() -> AttrDict
- get_address() -> AttrDict
- get_pending_transfer(token=None, partner=None) -> List[AttrDict]
- get_connections() -> AttrDict
- get_node_status() -> AttrDict
```

Checkout the [raiden api docs](https://github.com/raiden-network/raiden/blob/develop/docs/rest_api.rst) for further information about the returned objects.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)