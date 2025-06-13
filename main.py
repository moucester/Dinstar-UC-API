from dinstar.sms import DinstarSMS
from decouple import config, Csv

# Credentials are set in ENV
username = config('username')
password = config('password')
gateway_url = config('gateway_url')
verify_ssl = config('verify_ssl')

# Create an instance of DinstarSMS
sms = DinstarSMS(username, password, gateway_url, verify_ssl=verify_ssl)

# Get SMS
response = sms.receive_sms(flag="all")
print("Get SMS Response:", response)

