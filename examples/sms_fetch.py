from dinstar.sms import DinstarSMS
from dinstar.models import DinstarSMSReceiveMessage
from decouple import config

# This example demonstrates how to directly use the DinstarSMS class
# without the DinstarClient wrapper. This gives you more granular control
# if you only need access to one part of the API.

sms_client = DinstarSMS(
    username=config("DINSTAR_USER"),
    password=config("DINSTAR_PASS"),
    gateway_url=config("DINSTAR_URL"),
    verify_ssl=config("DINSTAR_VERIFY_SSL", cast=bool, default=True)
)

# Get all messages

try:
    messages: list[DinstarSMSReceiveMessage] = sms_client.receive_sms(flag="all")
    print("Fetched SMS messages:")
    for msg in messages:
        print(f"[{msg.timestamp}] Port {msg.port} From {msg.number}: {msg.text}")
except Exception as e:
    print(f"Error receiving SMS messages: {e}")

# Get all unread messages with ID greater than 90

try:
    messages: list[DinstarSMSReceiveMessage] = sms_client.receive_sms(incoming_sms_id=90, flag="unread")
    print("Fetched SMS messages:")
    for msg in messages:
        print(f"[{msg.timestamp}] Port {msg.port} From {msg.number}: {msg.text}")
except Exception as e:
    print(f"Error receiving SMS messages: {e}")