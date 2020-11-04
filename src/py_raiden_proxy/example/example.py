from py_raiden_proxy.RaidenAPIWrapper import RaidenAPIWrapper
from py_raiden_proxy.exceptions.exceptions import RaidenAPIException, RaidenAPIConflictException

URL = "localhost"
PORT = "5001"
TOKEN = "0x3ed0DaEDC3217615bde34FEDd023bC81ae49251B"
TARGET = "0x1F916ab5cf1B30B22f24Ebf435f53Ee665344Acf"  # Raiden Hub

rdn = RaidenAPIWrapper(ip=URL, port=PORT)

try:
    # Try to send payment to Raiden hub
    result = rdn.transfer(amount=1, target=TARGET, token=TOKEN)
    print(result)

# If no path to Hub exists open new channel
except RaidenAPIConflictException as e:
    print("Looks like we have to open a new channel!")
    rdn.open_channel(target=TARGET, deposit=1000, token=TOKEN)

