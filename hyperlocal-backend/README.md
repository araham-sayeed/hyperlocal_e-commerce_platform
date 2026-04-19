# Hyperlocal Backend (FastAPI)

Run from this directory so imports resolve (`app` package on `PYTHONPATH`).

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

Open **Swagger**: `http://127.0.0.1:8000/docs`  
**Health**: `GET http://127.0.0.1:8000/health`

## Postman (base URL)

Use `http://127.0.0.1:8000` and prefix **`/api/v1`** for all business routes below.

### Auth headers

- **Shop owner / customer / rider (after token):** `Authorization: Bearer <access_token>`

### Shop owners

| Method | Path | Body / notes |
|--------|------|----------------|
| POST | `/api/v1/shop-owners/register` | JSON: `email`, `password`, `full_name`, `shop_name`, `phone`, optional `latitude`, `longitude` |
| POST | `/api/v1/shop-owners/login` | `email`, `password` → returns `access_token` |
| GET | `/api/v1/shop-owners/me` | Bearer shop owner token |
| POST | `/api/v1/shop-owners/me/kyc` | `aadhaar_last_four` (4 digits, demo) |
| GET | `/api/v1/shop-owners/subscription/tiers` | Public |

### Riders

| Method | Path | Body / notes |
|--------|------|----------------|
| POST | `/api/v1/riders/apply` | `email`, `full_name`, `phone`, `aadhaar_last_four`, `reason_to_join` (≥10 chars) |
| POST | `/api/v1/riders/verify` | Demo admin: `rider_id`, `approve` |
| GET | `/api/v1/riders/me/status` | Bearer rider token |
| GET | `/api/v1/riders/{id}/status` | Public status lookup |
| POST | `/api/v1/riders/{id}/token` | Issue token after verified |

### Customers (OTP)

| Method | Path | Body / notes |
|--------|------|----------------|
| POST | `/api/v1/customers/otp/send` | `phone` — dev OTP is **`424242`** when `OTP_DEV_FIXED_CODE` is set (default in `.env.example`) |
| POST | `/api/v1/customers/otp/verify` | `phone`, `code` → `access_token` |
| GET | `/api/v1/customers/me` | Bearer customer token |
| PATCH | `/api/v1/customers/me` | Optional `email` |

### Catalog & discovery

| Method | Path | Notes |
|--------|------|--------|
| GET | `/api/v1/catalog/categories` | Seeded on first startup |
| GET | `/api/v1/catalog/categories/{id}/subcategories` | |
| GET | `/api/v1/catalog/stores/search?q=...` | Store name search |
| GET | `/api/v1/catalog/stores/nearby?lat=&lon=` | Optional `radius_km`, `limit` |

### Products

| Method | Path | Notes |
|--------|------|--------|
| GET | `/api/v1/products?q=&subcategory_id=&shop_owner_id=&limit=&offset=` | Paginated JSON |
| GET | `/api/v1/products/{id}` | |
| POST | `/api/v1/products` | Bearer **shop owner** — `subcategory_id`, `name`, `price`, `stock_quantity`, optional `description` |
| PATCH | `/api/v1/products/{id}` | Shop owner |
| DELETE | `/api/v1/products/{id}` | Shop owner |

### Orders

| Method | Path | Notes |
|--------|------|--------|
| POST | `/api/v1/orders` | Bearer **customer** — `shop_owner_id`, `lines[]` `{product_id, quantity}`, optional delivery lat/lon |
| GET | `/api/v1/orders/{id}` | Customer |
| POST | `/api/v1/orders/{id}/cancel` | Customer |

### Chat (demo bot + handoff JSON)

| Method | Path | Notes |
|--------|------|--------|
| POST | `/api/v1/chat/sessions` | Optional Bearer customer |
| POST | `/api/v1/chat/sessions/{id}/messages` | `content` — response may include `handoff` |
| WebSocket | `/api/v1/chat/ws/{session_id}?token=` | JSON send: `{"content":"..."}` |

### Reviews

| Method | Path | Notes |
|--------|------|--------|
| POST | `/api/v1/reviews` | Customer — `product_id`, `rating`, optional `comment` |
| GET | `/api/v1/reviews/product/{product_id}` | |
| PATCH | `/api/v1/reviews/{id}/moderate?visible=true` | Demo moderator |

### Returns

| Method | Path | Notes |
|--------|------|--------|
| POST | `/api/v1/returns` | Customer — `order_id`, `reason` |
| GET | `/api/v1/returns/{id}` | Customer |
| POST | `/api/v1/returns/{id}/approve?approve=true` | Demo admin |

### Support

| Method | Path | Notes |
|--------|------|--------|
| GET | `/api/v1/support/faqs` | |
| GET | `/api/v1/support/contacts` | Pune demo regions |
| POST | `/api/v1/support/tickets` | `user_role`, `user_ref`, `issue_description` |
| GET | `/api/v1/support/status` | DB ping JSON |

## Tests

```bash
pytest
```

## Docker (Level 3 preview)

```bash
docker compose up --build
```

SQLite file is stored under `./data` in the compose file.
