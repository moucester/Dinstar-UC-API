from dinstar.port import DinstarPort
from dinstar.models import DinstarPortInfo, DinstarApiResponse
from decouple import config
from typing import List

def main():
    client = DinstarPort(
        username=config("DINSTAR_USER"),
        password=config("DINSTAR_PASS"),
        gateway_url=config("DINSTAR_URL"),
        verify_ssl=config("DINSTAR_VERIFY_SSL", cast=bool, default=True),
    )

    # Query specific info fields for ports 0–2
    info_fields = [
        "imei", "imsi", "iccid", "number", "type", "reg", "slot", "callstate",
        "signal", "gprs", "remain_credit", "remain_monthly_credit", "remain_daily_credit",
        "remain_daily_calltime", "remain_hourly_calltime", "remain_daily_connect"
    ]

    response: DinstarApiResponse[List[DinstarPortInfo]] = client.get_port_info(
        info_type=info_fields,
        ports=[0, 1]
    )

    if response.error_code == 200 and response.data:
        print("Port Information:")
        for info in response.data:
            print(f"Port {info.port} | Type: {info.type} | Signal: {info.signal} | Reg: {info.reg}")
    else:
        print(f"Failed to fetch port info. Error code: {response.error_code}")

if __name__ == "__main__":
    main()
