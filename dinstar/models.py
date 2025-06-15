from dataclasses import dataclass
from typing import Generic, Optional, TypeVar

T = TypeVar("T")

@dataclass
class DinstarApiResponse(Generic[T]):
    """
    Generic API response wrapper for Dinstar API calls.

    This class encapsulates the standard metadata returned by
    the Dinstar API together with the typed payload data.

    Attributes:
        error_code (int): The status code returned by the API.
            Common codes:
            - 200: Request processed successfully
            - 202: Request accepted (for async operations)
            - 400: Bad request format
            - 413: Too many phone numbers (max 32)
            - 500: Internal server error or other errors
        sn (str): The serial number of the Dinstar gateway device.
        data (Optional[T]): The typed response data payload on success,
            or None if the request failed or returned no data.

    Usage:
        response = client.query_sms_result(...)
        if response.error_code == 200 and response.data:
            for item in response.data:
                print(item)
    """
    error_code: int
    sn: str
    data: Optional[T] = None

@dataclass
class DinstarSendSMSResponse:
    """
    Response returned after sending an SMS.

    Attributes:
        error_code (int): Status code indicating the result of the send operation.
        sn (str): Serial number of the gateway.
        sms_in_queue (int): Number of SMS messages waiting in the queue.
        task_id (int): Identifier for the SMS sending task.
    """
    error_code: int
    sn: str
    sms_in_queue: int
    task_id: int

@dataclass
class DinstarSMSResult:
    """
    Represents the result of an SMS sending operation.

    Attributes:
        port (int): Port used to send the SMS.
        user_id (int): Unique user ID assigned to the SMS.
        number (str): Recipient phone number.
        time (str): Timestamp of the send operation.
        status (str): Status of the SMS sending process.
        count (int): Number of SMS segments sent.
        succ_count (int): Number of SMS segments sent successfully.
        ref_id (int): Reference ID used to match delivery status.
        imsi (str): IMSI of the SIM card.
    """
    port: int
    user_id: int
    number: str
    time: str
    status: str
    count: int
    succ_count: int
    ref_id: int
    imsi: str

@dataclass
class DinstarSMSDeliveryStatus:
    """
    Represents the delivery status of a sent SMS.

    Attributes:
        port (int): Port used to send the SMS.
        number (str): Recipient phone number.
        time (str): Timestamp when the delivery status was reported.
        ref_id (int): Reference ID to match delivery status.
        status_code (int): Delivery status code (0 = received, 32-63 = temporary error, 64-255 = permanent error).
        imsi (str): IMSI of the SIM card.
    """
    port: int
    number: str
    time: str
    ref_id: int
    status_code: int
    imsi: str

@dataclass
class DinstarSMSQueueStatus:
    """
    Represents the status of the SMS queue in the gateway.

    Attributes:
        error_code (int): Status code of the queue query operation.
        sn (str): Serial number of the gateway.
        in_queue (int): Number of SMS messages waiting in the queue.
    """
    error_code: int
    sn: str
    in_queue: int

@dataclass
class DinstarSMSReceiveMessage:
    """
    Represents an incoming SMS message retrieved from the Dinstar gateway.

    Attributes:
        incoming_sms_id (int): Unique identifier for the incoming SMS.
        port (int): Port number that received the SMS.
        number (str): Sender's phone number.
        smsc (str): SMS center number.
        timestamp (str): Timestamp when the SMS was received.
        text (str): Content of the SMS message.
        imsi (str): IMSI of the SIM card.
    """
    incoming_sms_id: int
    port: int
    number: str
    smsc: str
    timestamp: str
    text: str
    imsi: str

    @staticmethod
    def from_dict(data: dict) -> "DinstarSMSReceiveMessage":
        return DinstarSMSReceiveMessage(
            incoming_sms_id=data.get("incoming_sms_id", 0),
            port=data.get("port", -1),
            number=data.get("number", ""),
            smsc=data.get("smsc", ""),
            timestamp=data.get("timestamp", ""),
            text=data.get("text", ""),
            imsi=data.get("imsi", "")
        )

@dataclass
class DinstarStopSMSTaskResponse:
    """
    Response returned after stopping an SMS sending task.

    Attributes:
        error_code (int): Status code indicating the result of the stop operation.
        sn (str): Serial number of the gateway.
    """
    error_code: int
    sn: str

