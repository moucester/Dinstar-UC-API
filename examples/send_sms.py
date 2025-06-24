from dinstar.sms import DinstarSMS, DinstarSMSMessage, DinstarBatchSMS
from dinstar.models import (
    DinstarApiResponse,
    DinstarSendSMSResponse,
    DinstarSMSResult,
    DinstarSMSDeliveryStatus,
    DinstarSMSQueueStatus,
)
from decouple import config
from typing import List, Optional
import time


def main():
    # Initialize SMS client
    sms_client = DinstarSMS(
        username=config("DINSTAR_USER"),
        password=config("DINSTAR_PASS"),
        gateway_url=config("DINSTAR_URL"),
        verify_ssl=config("DINSTAR_VERIFY_SSL", cast=bool, default=True),
    )

    # 1. Prepare batch messages to send
    batch = DinstarBatchSMS(
        messages=[
            DinstarSMSMessage(text="Hello user 1", number="+123456789", user_id=1),
            DinstarSMSMessage(text="Hello user 2", number="+987654321", user_id=2),
        ]
    )

    # 2. Send SMS batch
    send_response: DinstarApiResponse[DinstarSendSMSResponse] = sms_client.send_sms(batch)
    if send_response.error_code == 200 and send_response.data:
        print(f"SMS queued successfully. Task ID: {send_response.data.task_id}")
    else:
        print(f"Failed to send SMS. Error code: {send_response.error_code}")
        return

    # 3. Check SMS queue to verify messages are queued
    queue_response: DinstarApiResponse[DinstarSMSQueueStatus] = sms_client.query_sms_queue()
    if queue_response.error_code == 200 and queue_response.data:
        print(f"Current SMS queue length: {queue_response.data.in_queue}")
    else:
        print(f"Failed to get SMS queue status, error code: {queue_response.error_code}")

    # Wait a bit before querying results (adjust timing as needed)
    time.sleep(5)

    # 4. Query SMS sending result by user_ids
    user_ids = [msg.user_id for msg in batch.messages if msg.user_id is not None]
    if not user_ids:
        print("No user IDs provided in messages to query result.")
        return

    result_response: DinstarApiResponse[List[DinstarSMSResult]] = sms_client.query_sms_result(user_ids=user_ids)
    if result_response.error_code == 200 and result_response.data:
        print("SMS send results:")
        for res in result_response.data:
            print(f"User ID {res.user_id}: status {res.status}, sent at {res.time}")
    else:
        print(f"Failed to query SMS send results. Error code: {result_response.error_code}")

    # 5. Query SMS delivery status by numbers and ports
    numbers = [msg.number for msg in batch.messages]
    ports: Optional[List[int]] = None
    ports_set = set()
    for msg in batch.messages:
        if msg.port:
            ports_set.update(msg.port)
    if ports_set:
        ports = sorted(ports_set)

    delivery_response: DinstarApiResponse[List[DinstarSMSDeliveryStatus]] = sms_client.query_sms_delivery_status(
        numbers=numbers,
        ports=ports,
    )
    if delivery_response.error_code == 200 and delivery_response.data:
        print("SMS delivery statuses:")
        for status in delivery_response.data:
            print(f"Number {status.number}: status code {status.status_code}, reported at {status.time}")
    else:
        print(f"Failed to query SMS delivery status. Error code: {delivery_response.error_code}")


if __name__ == "__main__":
    main()
