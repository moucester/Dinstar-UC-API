from dinstar import DinstarClient
from decouple import config

# Load credentials and config from .env
client = DinstarClient(
    username=config("DINSTAR_USER"),
    password=config("DINSTAR_PASS"),
    gateway_url=config("DINSTAR_URL"),
    verify_ssl=config("DINSTAR_VERIFY_SSL", cast=bool, default=True)
)

# 1. Receive all SMS messages
try:
    messages = client.sms.receive_sms(flag="all")
    print("Fetched SMS messages:")
    for msg in messages:
        print(msg)
except Exception as e:
    print(f"Error receiving SMS messages: {e}")

# 2. Send a new SMS message
try:
    send_result = client.sms.send_sms(
        port="1",  # Replace with actual port
        destination="+1234567890",
        content="Hello from Dinstar!"
    )
    print("SMS sent successfully:", send_result)
except Exception as e:
    print(f"Error sending SMS: {e}")
