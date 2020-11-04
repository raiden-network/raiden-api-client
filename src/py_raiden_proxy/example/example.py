from py_raiden_proxy.RaidenAPIWrapper import RaidenAPIWrapper
from py_raiden_proxy.exceptions.exceptions import RaidenAPIException, RaidenAPIConflictException

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


def get_channel():
    channels = rdn.get_channels()
    for channel in channels:
        print(channel)


def get_payments():
    print(f"List of all payments: {rdn.get_payments()}")
    print(f"List of payments with Hub: {rdn.get_payments(partner=PARTNER, token=TOKEN)}")


def get_address():
    print(rdn.get_address().our_address)


if __name__ == "__main__":
    get_address()
