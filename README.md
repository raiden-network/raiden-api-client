# raiden api client

The raiden api client wraps the API of [raiden](https://github.com/raiden-network/raiden). It simplifies the usage of [raidens api](https://docs.raiden.network/raiden-api-1/resources) to a few lines.


## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install raiden API client.

```bash
pip install raiden-api-client
```

## Usage

```python
import raiden-api-client

raiden = raiden-api-client.RaidenAPIWrapper(ip=localhost, port=8545) # Parity running at localhost:8545

raiden.transfer(
   partner = "0x0000000000000000000000000000000000000000",
   amount = 1,
) # Transfering 1 Token to 0x00
```
Further examples can be found in the example folder.


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Note
This project has been set up using PyScaffold 3.2.3. For details and usage information on PyScaffold see https://pyscaffold.org/.

## License
[MIT](https://choosealicense.com/licenses/mit/)