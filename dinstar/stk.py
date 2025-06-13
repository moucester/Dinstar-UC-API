from dinstar.base import DinstarUC


class DinstarSTK(DinstarUC):
    """
    Class for handling SIM Toolkit (STK) operations using the Dinstar API.
    """

    def query_stk_info(self, port):
        """
        Query STK information for a specific port.
        :param port: The port number to query.
        :return: JSON response from the API.
        """
        endpoint = "/GetSTKView"
        data = {"port": port}
        return self.send_request(endpoint, data)

    def stk_operation(self, port, action, item=None, param=None):
        """
        Perform an STK operation such as selecting an item or canceling an action.
        :param port: The port number.
        :param action: Action to perform ('ok', 'cancel', or 'home').
        :param item: Item ID to select (optional).
        :param param: Additional parameter for STK operation (optional).
        :return: JSON response from the API.
        """
        endpoint = "/STKGo"
        data = {"port": port, "action": action}
        if item is not None:
            data["item"] = item
        if param is not None:
            data["param"] = param
        return self.send_request(endpoint, data)

    def query_stk_frame_id(self, port):
        """
        Query the current STK frame ID for a specific port.
        :param port: The port number.
        :return: JSON response from the API.
        """
        endpoint = "/GetSTKCurrFrameIndex"
        data = {"port": port}
        return self.send_request(endpoint, data)
