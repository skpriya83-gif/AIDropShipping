import hmac, hashlib, base64, os,logging
from fastapi import APIRouter, Request, Header, HTTPException


router = APIRouter(prefix="/webhooks")

SHOPIFY_CREATE_WH_SECRET = os.getenv("SHOPIFY_CREATE_WH_SECRET", "test_secret")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET", "test_secret")

# 🔹 Configure logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.debug("🚀 webhook.py loaded")


# --- Helpers ---
def verify_hmac(data: bytes, hmac_header: str, secret: str) -> bool:
    digest = hmac.new(secret.encode("utf-8"), data, hashlib.sha256).digest()
    computed_hmac = base64.b64encode(digest).decode()
    logger.info("📩 Raw body received: %s", data.decode())
    logger.info("🔑 Computed HMAC: %s", computed_hmac)
    logger.info("🔑 Header HMAC:   %s", hmac_header)
    return hmac.compare_digest(computed_hmac, hmac_header or "")


# --- Shopify Webhooks ---
@router.post("/shopify/orders/create")
async def shopify_order_webhook(
    request: Request, x_shopify_hmac_sha256: str = Header(None)
):
    logger.debug("🚀 Debug message should now appear 1")
    body = await request.body()
    logger.debug("Raw body received - indide shopify order book:   %s", body)
    logger.debug("🚀 Debug message should now appear 2")
    logger.info("ℹ️ Info message appears")
    logger.warning("⚠️ Warning message appears")
    hmac_header = str(request.headers.get("x-shopify-hmac-sha256"))

    hmac_verification = verify_hmac(body, hmac_header, SHOPIFY_CREATE_WH_SECRET)
    if not hmac_verification:
         logger.debug("🚀 Debug message should now appear 3")
         raise HTTPException(status_code=401, detail="Shopify HMAC verification failed 9")
    data = await request.json()
    print("✅ Shopify Order:", data)
    return {"status": "shopify_order_received", "id": data.get("id")}

# --- Razorpay Webhooks ---
@router.post("/payments/razorpay")
async def razorpay_payment_webhook(
    request: Request, x_razorpay_signature: str = Header(None)
):
    body = await request.body()
    if not verify_hmac(body, x_razorpay_signature, RAZORPAY_KEY_SECRET):
        raise HTTPException(status_code=401, detail="Razorpay signature failed")
    data = await request.json()
    print("✅ Razorpay Payment:", data)
    return {"status": "razorpay_payment_received", "id": data.get("id")}

# --- Shiprocket Webhooks ---
@router.post("/shiprocket/shipment-update")
async def shiprocket_update_webhook(request: Request):
    data = await request.json()
    print("✅ Shiprocket Update:", data)
    return {"status": "shiprocket_update_received", "awb": data.get("awb")}

# --- WhatsApp Cloud API Webhooks ---
@router.post("/whatsapp/messages")
async def whatsapp_message_webhook(request: Request):
    data = await request.json()
    print("✅ WhatsApp Message:", data)
    return {"status": "whatsapp_message_received"}

@router.get("/webhook-test")
async def webhook_test():
    logger.debug("🔥 /webhook-test route hit")
    return {"msg": "webhook test ok"}
