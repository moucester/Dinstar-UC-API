import json
from dinstar.base import DinstarUC


class DinstarSMS(DinstarUC):
    def send_sms(self, text, recipients, port=None, encoding="unicode", request_status_report=True):
        """
        Send an SMS to one or multiple recipients.
        :param text: The content of the SMS.
        :param recipients: List of recipient phone numbers.
        :param port: List of ports to use (optional).
        :param encoding: Encoding type ('unicode' or 'gsm-7bit').
        :param request_status_report: Whether to request an SMS delivery report.
        :return: JSON response from the API.
        """
        endpoint = "/api/send_sms"
        data = {
            "text": text,
            "param": [{"number": num, "user_id": i} for i, num in enumerate(recipients, start=1)],
            "encoding": encoding,
            "request_status_report": request_status_report
        }
        if port:
            data["port"] = port
        return self.send_request(endpoint, data)

    def query_sms_result(self, user_ids=None, numbers=None, ports=None, time_after=None, time_before=None):
        """
        Query SMS sending results.
        :param user_ids: List of user IDs to match sent SMS.
        :param numbers: List of recipient numbers.
        :param ports: List of ports used for sending.
        :param time_after: Query messages sent after this time (YYYY-MM-DD HH:MM:SS).
        :param time_before: Query messages sent before this time (YYYY-MM-DD HH:MM:SS).
        :return: JSON response from the API.
        """
        endpoint = "/api/query_sms_result"
        data = {}
        if user_ids:
            data["user_id"] = user_ids
        if numbers:
            data["number"] = numbers
        if ports:
            data["port"] = ports
        if time_after:
            data["time_after"] = time_after
        if time_before:
            data["time_before"] = time_before
        return self.send_request(endpoint, data)

    def query_sms_delivery_status(self, numbers=None, ports=None, time_after=None, time_before=None):
        """
        Query the delivery status of sent SMS.
        :param numbers: List of recipient numbers.
        :param ports: List of ports used for sending.
        :param time_after: Query messages sent after this time (YYYY-MM-DD HH:MM:SS).
        :param time_before: Query messages sent before this time (YYYY-MM-DD HH:MM:SS).
        :return: JSON response from the API.
        """
        endpoint = "/api/query_sms_deliver_status"
        data = {}
        if numbers:
            data["number"] = numbers
        if ports:
            data["port"] = ports
        if time_after:
            data["time_after"] = time_after
        if time_before:
            data["time_before"] = time_before
        return self.send_request(endpoint, data)

    def query_sms_queue(self):
        """
        Query the number of SMS messages waiting to be sent.
        :return: JSON response from the API.
        """
        endpoint = "/api/query_sms_in_queue"
        return self.send_request(endpoint, {})

    def receive_sms(self, incoming_sms_id=0, flag="unread", ports=None):
        """
        Receive incoming SMS messages.
        :param incoming_sms_id: Fetch messages with an ID greater than this value.
        :param flag: 'unread', 'read', or 'all'.
        :param ports: List of ports to fetch messages from.
        :return: JSON response from the API.
        """
        endpoint = "/api/query_incoming_sms"
        data = {"incoming_sms_id": incoming_sms_id, "flag": flag}
        if ports:
            data["port"] = ports
        return self.send_request(endpoint, data)

    def stop_sms(self, task_id):
        """
        Stop an SMS sending task.
        :param task_id: ID of the task to be stopped.
        :return: JSON response from the API.
        """
        endpoint = f"/api/stop_sms?task_id={task_id}"
        return self.send_request(endpoint, {})