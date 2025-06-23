from dinstar.device import DinstarDevice
from dinstar.models import DinstarDeviceStatus
from decouple import config
from typing import Optional

def main():
    client = DinstarDevice(
        username=config("DINSTAR_USER"),
        password=config("DINSTAR_PASS"),
        gateway_url=config("DINSTAR_URL"),
        verify_ssl=config("DINSTAR_VERIFY_SSL", cast=bool, default=True),
    )

    status: Optional[DinstarDeviceStatus] = client.get_device_status()

    if status:
        print("Device Performance Status:")
        print(f"CPU Used: {status.cpu_used}%")
        print(f"Flash Total: {status.flash_total} KB")
        print(f"Flash Used: {status.flash_used} KB")
        print(f"Memory Total: {status.memory_total} KB")
        print(f"Memory Cached: {status.memory_cached} KB")
        print(f"Memory Buffers: {status.memory_buffers} KB")
        print(f"Memory Free: {status.memory_free} KB")
        print(f"Memory Used: {status.memory_used} KB")
    else:
        print("Failed to retrieve device status.")

if __name__ == "__main__":
    main()
