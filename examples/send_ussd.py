import time
from dinstar.ussd import DinstarUSSD
from dinstar.models import DinstarUSSDResult, DinstarUSSDReply, DinstarApiResponse
from decouple import config
from typing import List

def main():
    client = DinstarUSSD(
        username=config("DINSTAR_USER"),
        password=config("DINSTAR_PASS"),
        gateway_url=config("DINSTAR_URL"),
        verify_ssl=config("DINSTAR_VERIFY_SSL", cast=bool, default=True),
    )

    port = 0

    # Step 1: Send USSD
    print(f"Sending USSD *100# on port {port}")
    send_response: DinstarApiResponse[List[DinstarUSSDResult]] = client.send_ussd(
        text="*100#",
        ports=[port],
    )

    if send_response.error_code == 202 and send_response.data:
        for result in send_response.data:
            print(f"Port {result.port}: status {result.status}")
    else:
        print(f"Failed to send USSD: error_code={send_response.error_code}")
        return

    # Step 2: Wait before querying
    print("Waiting for USSD reply...")
    time.sleep(15)

    # Step 3: Query USSD reply
    reply_response: DinstarApiResponse[List[DinstarUSSDReply]] = client.query_ussd_reply(
        ports=[port]
    )

    if reply_response.error_code == 200 and reply_response.data:
        for reply in reply_response.data:
            print(f"Port {reply.port}: reply -> {reply.text}")
    else:
        print(f"No USSD reply found or error: error_code={reply_response.error_code}")

if __name__ == "__main__":
    main()
