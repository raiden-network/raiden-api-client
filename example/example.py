from raiden_api_client.exceptions import (
    RaidenAPIConflictException
)
from raiden_api_client.wrapper import RaidenAPIWrapper

URL = "localhost"
PORT = "5001"
TOKEN = "0x3ed0DaEDC3217615bde34FEDd023bC81ae49251B"
PARTNER = "0x1F916ab5cf1B30B22f24Ebf435f53Ee665344Acf"  # Raiden Hub

rdn = RaidenAPIWrapper(ip=URL, port=PORT)


def transfer():
    try:
        # Try to send payment to Raiden hub
        result = rdn.transfer(amount=1, partner=PARTNER, token=TOKEN)
        print(result)

    # If no path to receiver exists open new channel
    except RaidenAPIConflictException:
        print("Transfer not successful - No Path to receiver found")


def open_channel():
    rdn.open_channel(partner=PARTNER, deposit=1000, token=TOKEN)


def get_channel(token=None, partner=None):
    if token and partner:
        channels = rdn.get_channels(token, partner)
    elif token:
        channels = rdn.get_channels(token)
    else:
        channels = rdn.get_channels()
    for channel in channels:
        print(channel)


def get_payments():
    print(f"List of all payments: {rdn.get_payments()}")
    print(
        f"List of payments with Hub: {rdn.get_payments(partner=PARTNER, token=TOKEN)}"
    )


def get_address():
    print(rdn.get_address().our_address)


def get_token_network():
    print(rdn.get_token_network())
    print(rdn.get_token_network(token=TOKEN))


def get_raiden_version():
    print(rdn.get_raiden_version())


def get_pending_transfer():
    print(rdn.get_pending_transfer())


def get_connections():
    print(rdn.get_connections())


def get_node_status():
    print(rdn.get_node_status())


def leave_token_network(token):
    print(rdn.leave_token_network(token))


def register_token(token):
    print(rdn.register_token(token=token))


def fund_channel(partner, token, deposit):
    print(rdn.fund_channel(partner=partner, token=token, deposit=deposit))


def mint_tokens(token, receiver, amount):
    print(rdn.mint_tokens(token=token, receiver=receiver, amount=amount))


if __name__ == "__main__":
    amount = 1000
    print(f"Minting {amount} Tokens for {PARTNER}")
    mint_tokens(token=TOKEN, receiver=PARTNER, amount=1000)
