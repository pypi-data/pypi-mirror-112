import socket

from . import const, Message
from . import OppleLightDevice

MESSAGE_TYPE = const.MESSAGE_TYPE
SEARCH_RES_OFFSET = const.SEARCH_RES_OFFSET


def _search(host: str = '255.255.255.255'):
    message = Message.build_message(MESSAGE_TYPE['SEARCH'])
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.sendto(message.to_bytes(), (host, const.BROADCAST_PORT))
    s.settimeout(2)

    device_list = []

    while True:
        try:
            data, address = s.recvfrom(1024)
            message = Message.parse_message(data)

            if message.get(SEARCH_RES_OFFSET['CLASS_SKU'], 4, value_type=int) == 0x100010E:
                device = OppleLightDevice.OppleLightDevice(message=message)
            else:
                break

            yield device

            device_list.append(device)

            if address == host:
                break

        except socket.timeout:
            break

    return device_list


def search():
    return _search()


async def search_one(host: str):
    for device in _search(host):
        return device
    return None
