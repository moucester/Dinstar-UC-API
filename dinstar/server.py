from fastapi import FastAPI, Request
from pydantic import BaseModel
import sqlite3
import uvicorn
from db.sqlite import init_db

app = FastAPI()

# Initialize the database
DATABASE_PATH = 'data/events.db'
init_db(DATABASE_PATH)


class SMSData(BaseModel):
    incoming_sms_id: int
    port: int
    number: str
    smsc: str
    timestamp: str
    text: str


class SMSResult(BaseModel):
    port: int
    number: str
    time: str
    status: str
    count: int
    succ_count: int
    ref_id: int
    imsi: str


class SMSDeliveryStatus(BaseModel):
    port: int
    number: str
    time: str
    ref_id: int
    status_code: int
    imsi: str


class USSDData(BaseModel):
    port: int
    text: str


class CDRData(BaseModel):
    port: int
    start_date: str
    answer_date: str
    duration: int
    source_number: str
    destination_number: str
    direction: str
    ip: str
    codec: str
    hangup: str
    gsm_code: int
    bcch: str


class DeviceData(BaseModel):
    port_number: int
    IP: str
    MAC: str
    status: str


class ExceptionInfo(BaseModel):
    port: int
    type: str
    action: str


@app.post("/")
async def receive_event(request: Request):
    """
    Endpoint to receive various push events.

    The remote API calls this endpoint and passes data via JSON.
    The first parameter is always the SN, and the second parameter determines the event type.

    :return: JSON response confirming receipt of the data.
    """
    data = await request.json()
    sn = data.get("sn")
    event_type, event_data = next((k, v) for k, v in data.items() if k != "sn")

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    match event_type:
        case "sms":
            sms_data = [SMSData(**sms) for sms in event_data]
            for sms in sms_data:
                cursor.execute('''
                    INSERT INTO sms (incoming_sms_id, port, number, smsc, timestamp, text, delivered)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (sms.incoming_sms_id, sms.port, sms.number, sms.smsc, sms.timestamp, sms.text, False))
        case "sms_result":
            sms_result_data = [SMSResult(**result) for result in event_data]
            for result in sms_result_data:
                cursor.execute('''
                    INSERT INTO sms_result (port, number, time, status, count, succ_count, ref_id, imsi, delivered)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                result.port, result.number, result.time, result.status, result.count, result.succ_count, result.ref_id,
                result.imsi, False))
        case "sms_deliver_status":
            sms_delivery_status_data = [SMSDeliveryStatus(**status) for status in event_data]
            for status in sms_delivery_status_data:
                cursor.execute('''
                    INSERT INTO sms_deliver_status (port, number, time, ref_id, status_code, imsi, delivered)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (status.port, status.number, status.time, status.ref_id, status.status_code, status.imsi, False))
        case "ussd":
            ussd_data = [USSDData(**ussd) for ussd in event_data]
            for ussd in ussd_data:
                cursor.execute('''
                    INSERT INTO ussd (port, text, delivered)
                    VALUES (?, ?, ?)
                ''', (ussd.port, ussd.text, False))
        case "cdr":
            cdr_data = [CDRData(**cdr) for cdr in event_data]
            for cdr in cdr_data:
                cursor.execute('''
                    INSERT INTO cdr (port, start_date, answer_date, duration, source_number, destination_number, direction, ip, codec, hangup, gsm_code, bcch, delivered)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                cdr.port, cdr.start_date, cdr.answer_date, cdr.duration, cdr.source_number, cdr.destination_number,
                cdr.direction, cdr.ip, cdr.codec, cdr.hangup, cdr.gsm_code, cdr.bcch, False))
        case "device":
            device_data = DeviceData(**event_data)
            cursor.execute('''
                INSERT INTO device (port_number, IP, MAC, status, delivered)
                VALUES (?, ?, ?, ?, ?)
            ''', (device_data.port_number, device_data.IP, device_data.MAC, device_data.status, False))
        case "exception_info":
            exception_info_data = ExceptionInfo(**event_data)
            cursor.execute('''
                INSERT INTO exception_info (port, type, action, delivered)
                VALUES (?, ?, ?, ?)
            ''', (exception_info_data.port, exception_info_data.type, exception_info_data.action, False))
        case _:
            print(f"Unknown event type: {event_type}")

    conn.commit()
    conn.close()

    return {"status": "success", "message": f"{event_type} data received"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)