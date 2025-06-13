from dinstar.base import DinstarUC


class DinstarUSSD(DinstarUC):
    """
    Class for handling USSD operations using the Dinstar API.
    """

    def send_ussd(self, text, ports, command="send"):
        """
        Send a USSD request.
        :param text: The USSD string to send.
        :param ports: List of ports to use.
        :param command: 'send' or 'cancel' (default: 'send').
        :return: JSON response from the API.
        """
        endpoint = "/api/send_ussd"
        data = {
            "text": text,
            "port": ports,
            "command": command
        }
        return self.send_request(endpoint, data)

    def query_ussd_reply(self, ports):
        """
        Query USSD replies from the gateway.
        :param ports: List of ports to check.
        :return: JSON response from the API.
        """
        endpoint = "/api/query_ussd_reply"
        data = {"port": ports}
        return self.send_request(endpoint, data)
