import os

# WhatsApp notifications are sent via Twilio's WhatsApp API.
# If the credentials below aren't set, this silently does nothing —
# order creation will never fail because of a missing/broken notification.

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_FROM = os.getenv("TWILIO_WHATSAPP_FROM")  # e.g. "whatsapp:+14155238886" (Twilio's sandbox number)
OWNER_WHATSAPP_NUMBER = os.getenv("OWNER_WHATSAPP_NUMBER", "+923134618471")


def send_order_whatsapp(order) -> None:
    """Send a WhatsApp message to the owner with the new order's details.
    Never raises — a failed/misconfigured notification should never block
    an order from being placed.
    """
    if not (TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN and TWILIO_WHATSAPP_FROM):
        print("[WhatsApp] Twilio isn't configured (see .env) — skipping notification.")
        return

    try:
        from twilio.rest import Client  # imported here so the app still runs without twilio installed

        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

        items_text = "\n".join(f"- {it['name']} x{it['qty']} (${it['price']})" for it in order.items)
        body = (
            f"*New Watch Valley order — {order.code}*\n\n"
            f"Customer: {order.name}\n"
            f"Phone: {order.phone}\n"
            f"Address: {order.address}\n\n"
            f"Items:\n{items_text}\n\n"
            f"Total: ${order.total:.2f}\n"
            f"Status: {order.status}"
        )

        to_number = OWNER_WHATSAPP_NUMBER
        if not to_number.startswith("whatsapp:"):
            to_number = f"whatsapp:{to_number}"

        client.messages.create(from_=TWILIO_WHATSAPP_FROM, to=to_number, body=body)
        print(f"[WhatsApp] Order {order.code} notification sent to {OWNER_WHATSAPP_NUMBER}.")
    except Exception as e:
        # Log and move on — never let a notification failure break checkout.
        print(f"[WhatsApp] Failed to send notification for order {order.code}: {e}")
