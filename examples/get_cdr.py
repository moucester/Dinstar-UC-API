from dinstar.cdr import DinstarCDR
from dinstar.models import DinstarApiResponse, DinstarCDRRecord
from decouple import config
from typing import List, Optional

def main():
    client = DinstarCDR(
        username=config("DINSTAR_USER"),
        password=config("DINSTAR_PASS"),
        gateway_url=config("DINSTAR_URL"),
        verify_ssl=config("DINSTAR_VERIFY_SSL", cast=bool, default=True),
    )

    # Example: Fetch CDRs for ports 1 and 2 after a given time
    response: DinstarApiResponse[List[DinstarCDRRecord]] = client.get_cdr(
        ports=[0, 1],
        time_after="2024-01-01 00:00:00",
    )

    if response.error_code == 200 and response.data:
        print("Fetched CDR records:")
        for cdr in response.data:
            print(f"Port {cdr.port}: Call from {cdr.source_number} to {cdr.destination_number} started at {cdr.start_date}, duration {cdr.duration}s")
    else:
        print(f"Failed to fetch CDR records, error code: {response.error_code}")

if __name__ == "__main__":
    main()
