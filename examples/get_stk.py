from dinstar.stk import DinstarSTK
from dinstar.models import DinstarSTKView
from decouple import config

def main():
    client = DinstarSTK(
        username=config("DINSTAR_USER"),
        password=config("DINSTAR_PASS"),
        gateway_url=config("DINSTAR_URL"),
        verify_ssl=config("DINSTAR_VERIFY_SSL", cast=bool, default=True),
    )

    port = 0

    # Step 1: Query STK menu
    view: DinstarSTKView = client.query_stk_info(port=port)
    if not view:
        print("Failed to retrieve STK menu.")
        return

    print(f"\nSTK Menu Title: {view.title}")
    if view.text:
        print(f"Prompt Text: {view.text}")
    if view.item:
        print("Menu Items:")
        for item in view.item:
            print(f" - {item.item_id}: {item.item_string}")

    # Step 2: Get STK frame ID
    frame_id = client.get_stk_frame_id(port)
    if frame_id is None:
        print("Failed to get STK frame ID.")
        return

    print(f"\nCurrent STK Frame ID: {frame_id}")

    # Step 3: Cancel the menu
    result = client.send_stk_reply(port=port, action="cancle")
    if result.error_code == 200:
        print(f"\nSTK menu cancelled successfully. SN: {result.sn}")
    else:
        print(f"\nFailed to cancel STK menu. Error code: {result.error_code}")

if __name__ == "__main__":
    main()
