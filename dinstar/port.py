from dinstar.base import DinstarUC


class DinstarPort(DinstarUC):
    """
    Class for handling port-related operations using the Dinstar API.
    """

    def get_port_info(self, ports, info_types):
        """
        Get port information from the gateway.
        :param ports: List of ports to query.
        :param info_types: List of information types to retrieve.
        :return: JSON response from the API.
        """
        endpoint = "/api/get_port_info"
        data = {"port": ports, "info_type": info_types}
        return self.send_request(endpoint, data)

    def set_port_info(self, port, action, param, **kwargs):
        """
        Set port information on the gateway.
        :param port: Port number to configure.
        :param action: The action to perform (e.g., 'slot', 'reset', 'power').
        :param param: The parameter value for the action.
        :param kwargs: Additional optional parameters.
        :return: JSON response from the API.
        """
        endpoint = "/api/set_port_info"
        data = {"port": port, "action": action, "param": param}
        data.update(kwargs)
        return self.send_request(endpoint, data)
