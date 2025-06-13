from dataclasses import dataclass


@dataclass
class DinstarSendSMSResponse:
    error_code: int
    sn: str
    sms_in_queue: int
    task_id: int

@dataclass
class DinstarSMSResult:
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
class DinstarSMSReceiveMessage:
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
    error_code: int
    sn: str

