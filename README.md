# AI Dropship Week 0 Starter

This is the Week-0 infrastructure starter for your AI-driven dropshipping agent.

## Prerequisites
- Docker & Docker Compose
- ngrok (or Cloudflare Tunnel)
- A Shopify dev store with custom app (free)
- Optional: Razorpay, Shiprocket, WhatsApp Cloud API sandbox creds

## Setup Steps

### 1. Clone & configure environment
```bash
cp .env.example .env
# edit .env with your Shopify API secret, etc.
```

### 2. Start services (FastAPI + Postgres + Redis)
```bash
docker compose up --build
```
Check:
```bash
curl http://localhost:8000/health   # {"ok": true}
curl http://localhost:8000/ready    # {"ready": true}
```

### 3. Expose API via ngrok
```bash
ngrok http 8000
```
Copy the HTTPS URL shown, e.g. `https://abc123.ngrok.io`.
http://localhost:8000 
### 4. Shopify webhook setup
- Go to **Shopify Admin → Settings → Notifications → Webhooks**
- Add new webhook:
  - Event: **Orders Create**
  - URL: `https://<ngrok-url>/webhooks/shopify/orders/create`
- Place a test order using **Bogus Gateway**
- Check your FastAPI logs for order payload.

### 5. Optional integrations
- **Razorpay sandbox**: add webhook to `/webhooks/payments/razorpay`
- **Shiprocket**: test serviceability API with creds from `.env`
- **WhatsApp Cloud API**: send a test message using your access token.

---

✅ By the end of Week 0, you should see Shopify test orders, Razorpay payment events, Shiprocket shipment updates, and WhatsApp messages arriving in your FastAPI logs.
