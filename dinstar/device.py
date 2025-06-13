from dinstar.base import DinstarUC


class DinstarDevice(DinstarUC):
    """
    Class for handling device status operations using the Dinstar API.
    """

    def get_status(self):
        """
        Retrieve device status from the gateway.

        This method sends a request to the /api/get_status endpoint to retrieve
        various performance metrics of the device, such as CPU usage, flash memory
        usage, and RAM usage.

        :return: JSON response from the API containing performance metrics.
        """
        endpoint = "/api/get_status"
        data = ["performance"]
        return self.send_request(endpoint, data)