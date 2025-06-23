from dinstar.port import DinstarPort
from dinstar.models import DinstarApiResponse
from decouple import config

def main():
    client = DinstarPort(
        username=config("DINSTAR_USER"),
        password=config("DINSTAR_PASS"),
        gateway_url=config("DINSTAR_URL"),
        verify_ssl=config("DINSTAR_VERIFY_SSL", cast=bool, default=True),
    )

    port_number = 1

    # Turn OFF the port
    print(f"Turning OFF port {port_number}...")
    off_response: DinstarApiResponse[None] = client.set_port_info(
        port=port_number,
        action="power",
        param="off"
    )
    print(f"Response: error_code={off_response.error_code}, sn={off_response.sn}")

    # Turn ON the port
    print(f"Turning ON port {port_number}...")
    on_response: DinstarApiResponse[None] = client.set_port_info(
        port=port_number,
        action="power",
        param="on"
    )
    print(f"Response: error_code={on_response.error_code}, sn={on_response.sn}")

if __name__ == "__main__":
    main()
