from dinstar.sms import DinstarSMS
from dinstar.models import DinstarSMSReceiveMessage, DinstarApiResponse
from decouple import config
from typing import List

# Initialize the SMS client
sms_client = DinstarSMS(
    username=config("DINSTAR_USER"),
    password=config("DINSTAR_PASS"),
    gateway_url=config("DINSTAR_URL"),
    verify_ssl=config("DINSTAR_VERIFY_SSL", cast=bool, default=True)
)

try:
    # Receive unread SMS messages with incoming_sms_id greater than 0
    response: DinstarApiResponse[List[DinstarSMSReceiveMessage]] = sms_client.receive_sms(flag="all")

    if response.error_code == 200 and response.data:
        print("Fetched SMS messages:")
        for msg in response.data:
            print(f"[{msg.timestamp}] Port {msg.port} From {msg.number}: {msg.text}")
    else:
        print(f"Failed to fetch SMS messages. Error code: {response.error_code}")
except Exception as e:
    print(f"Error receiving SMS messages: {e}")

# Get all unread messages with ID greater than 90

try:
    # Receive unread SMS messages with incoming_sms_id greater than 0
    response: DinstarApiResponse[List[DinstarSMSReceiveMessage]] = sms_client.receive_sms(flag="unread",incoming_sms_id=90)

    if response.error_code == 200 and response.data:
        print("Fetched SMS messages:")
        for msg in response.data:
            print(f"[{msg.timestamp}] Port {msg.port} From {msg.number}: {msg.text}")
    else:
        print(f"Failed to fetch SMS messages. Error code: {response.error_code}")
except Exception as e:
    print(f"Error receiving SMS messages: {e}")