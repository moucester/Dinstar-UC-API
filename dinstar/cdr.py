from dinstar.base import DinstarUC


class DinstarCDR(DinstarUC):
    """
    Class for handling Call Detail Records (CDR) operations using the Dinstar API.
    """

    def get_cdr(self, ports=None, time_after=None, time_before=None):
        """
        Retrieve call detail records (CDR) from the gateway.
        :param ports: List of ports to query (optional).
        :param time_after: Retrieve records after this time (YYYY-MM-DD HH:MM:SS) (optional).
        :param time_before: Retrieve records before this time (YYYY-MM-DD HH:MM:SS) (optional).
        :return: JSON response from the API.
        """
        endpoint = "/api/get_cdr"
        data = {}
        if ports:
            data["port"] = ports
        if time_after:
            data["time_after"] = time_after
        if time_before:
            data["time_before"] = time_before
        return self.send_request(endpoint, data)
