from dinstar.sms import DinstarSMS, DinstarSMSMessage, DinstarBatchSMS
from decouple import config

from pydantic import BaseModel
from typing import List

# This example demonstrates how to directly use the DinstarSMS class
# to send an SMS message, bypassing the DinstarClient wrapper.

sms_client = DinstarSMS(
    username=config("DINSTAR_USER"),
    password=config("DINSTAR_PASS"),
    gateway_url=config("DINSTAR_URL"),
    verify_ssl=config("DINSTAR_VERIFY_SSL", cast=bool, default=True)
)

messages = [
    DinstarSMSMessage(text="Hello 1", number="+123456789", user_id=1, port=[1]),
    DinstarSMSMessage(text="Hello 2", number="+987654321", user_id=2, port=[1, 2])
]

batch = DinstarBatchSMS(messages=messages)

try:
    send_result = sms_client.send_sms(batch)
    print("SMS sent successfully:", send_result)
except Exception as e:
    print(f"Error sending SMS: {e}")
