# RemitCompare: Project Spec (v1)

Last updated: 2026-10-22 · Status: Step 2 done (MVP planned, scope updated: 4 corridors, 3-4 weeks)

## 1. What it is

RemitCompare helps people in Qatar compare how much money their family
**actually receives** when sending abroad. It shows the transfer fee **and**
the hidden exchange-rate markup.

**Portfolio goal:** a live, tested, well-documented fullstack app for
fintech frontend/fullstack roles in Doha.

## 2. User story

**As a** person living in Qatar who sends money home,
**I want to** enter an amount and a destination country and see providers
ranked by how much the recipient receives,
**so that** I can pick the cheapest option without doing the maths myself.

**Acceptance checks**
- I pick a country and an amount in QAR.
- I see a ranked list, and the best option is highlighted.
- Each row shows: fee, estimated rate, recipient gets, true total cost.
- I can see where each number came from and when it was last verified.

## 3. Core features (max 4)

### 3.1 Compare calculator
- Inputs: destination country, amount in QAR (the total the sender pays; the fee is included in it).
- Output: providers ranked by "recipient gets" (highest first). Best deal highlighted.
- Each row: fee (QAR), estimated rate, recipient gets, hidden markup cost (QAR), true total cost (QAR).

### 3.2 Daily mid-market rates
- Source: ExchangeRate-API Open Access endpoint (`open.er-api.com`): no API key, updates once a day, attribution required, rate limited.
- The backend fetches QAR-based rates, stores them in the DB, and serves from the DB. Never call the external API on every user request.
- Footer shows the attribution link and "rates updated at ...".
- Step 3 task: read their terms page and test one call for all 4 currencies (INR, USD, SAR, PKR) before building on it.

### 3.3 Honest data labels
- Every fee quote shows a source link and a "last verified" date.
- Sample data shows a **SAMPLE** badge.
- A warning appears if the quote was verified more than 30 days ago.
- Footer disclaimer: estimates only, not financial advice, check with the provider before sending.

### 3.4 Shareable link
- The URL stores the selection, for example `/?to=INR&amount=1000`.
- Opening that link restores the same comparison.

## 4. Corridors (all from Qatar, QAR)

| Country | Currency |
|---|---|
| India | INR |
| United States | USD |
| Saudi Arabia | SAR |
| Pakistan | PKR |

- All 4 get live mid-market rates and real, sourced fee data.
- If a corridor has no verified fee data yet, the app shows "Fee data coming soon" instead of an empty page.
- More countries (Philippines, Bangladesh, Nepal, China, Japan) are a v2 job: a corridor is just a new database row plus its fee quotes.

## 5. Data rules (non-negotiable)

- Never invent real fee or rate data.
- Seed/demo data goes in a seed file with `is_sample = true` and is always shown with a SAMPLE badge.
- Real fee data is collected manually from each provider's public pages or calculators. Save the `source_url` and `last_verified_on` date.
- Never scrape a site that forbids it. Check each site's terms.
- Everything shown is an **estimate**.

## 6. How the numbers are calculated

```
amount_qar        = total the sender pays
amount_after_fee  = amount_qar - fee_qar
effective_rate    = mid_market_rate * (1 - markup_percent / 100)
recipient_gets    = amount_after_fee * effective_rate
markup_cost_qar   = amount_after_fee * markup_percent / 100
true_cost_qar     = fee_qar + markup_cost_qar
```

- Money uses `NUMERIC` in PostgreSQL and `Decimal` in Python. **Never float.**
- Assumption (stated in the UI): the fee is taken out of the amount the sender pays.
- `markup_percent` = how much worse the provider's rate was than the mid-market rate when you checked their public calculator on `last_verified_on`.

## 7. Database (PostgreSQL)

**corridors**
- `id` (PK)
- `country_name`
- `currency_code` (3 letters, unique)
- `is_active` (boolean)

**providers**
- `id` (PK)
- `name` (unique)
- `website_url`

**fee_quotes**
- `id` (PK)
- `provider_id` (FK)
- `corridor_id` (FK)
- `fee_qar` NUMERIC(10,2), must be >= 0
- `markup_percent` NUMERIC(5,2), must be >= 0
- `source_url`
- `last_verified_on` (date)
- `is_sample` (boolean)
- UNIQUE (`provider_id`, `corridor_id`)

**exchange_rates**
- `currency_code` (PK, 3 letters)
- `rate_per_qar` NUMERIC(18,6)
- `fetched_at` (timestamptz)

Tech notes: SQLAlchemy 2.0 + Alembic migrations, Pydantic schemas.

## 8. API (FastAPI)

**GET /api/health**
- Returns `{"status": "ok"}`.

**GET /api/corridors**
- Returns active corridors: `id`, `country_name`, `currency_code`, `has_fee_data`.

**GET /api/compare?to=INR&amount=1000**
- `to`: currency code (required). `amount`: number greater than 0 (required).
- Response fields:
  - `to`, `amount_qar`, `mid_market_rate`, `rates_updated_at`
  - `results[]`: `provider_name`, `website_url`, `fee_qar`, `effective_rate`, `recipient_gets`, `markup_cost_qar`, `true_cost_qar`, `source_url`, `last_verified_on`, `is_sample`, `is_stale`
- Errors:
  - 400: invalid amount
  - 404: unknown or inactive currency
  - 503: no rate stored yet
- No fee data yet: 200 with an empty `results` list.

**POST /api/admin/refresh-rates**
- Header `X-Admin-Token` must match an environment variable.
- 401 if wrong. Returns how many rates were updated.
- v1 refresh is triggered manually through this endpoint.

## 9. Tests (pytest)

- Calculation function: normal amounts, zero markup, rounding.
- Ranking order.
- Stale-quote detection (30 days).
- `/api/compare`: happy path, bad amount, unknown currency.
- Rate refresh with the external API **mocked** (no real network in tests).

## 10. NOT in v1

- User accounts / login
- Sending real money, payments, KYC
- Scraping provider websites
- Live provider quotes or real-time rates
- Rate-history charts and rate alerts
- Arabic / RTL support (good v2)
- Delivery speed and payout-method comparison
- Admin UI (data is updated via seed file / script)
- More destination countries (see section 4)
- Sending countries other than Qatar
- Promo codes and affiliate links

## 11. Definition of done (v1)

- [ ] Live URL works
- [ ] README with screenshots, setup steps, data sources and disclaimer
- [ ] pytest passing locally and on every push (GitHub Actions)
- [ ] Clean, small commits with clear messages
- [ ] Real sourced fee data for all 4 corridors; sample data (if any) clearly labelled
- [ ] Responsive layout, plus loading, error and empty states

## 12. Rough 3-4 week plan

- Week 1: repo, FastAPI skeleton, PostgreSQL, tables, sample seed data
- Week 2: rates fetch, compare logic + tests, GitHub Actions
- Week 3: React + TypeScript UI connected to the API
- Week 4: real fee data for all 4 corridors, states, polish, deploy, README, screenshots

Tip: real fee research (4 corridors x about 4 providers) is the slow part. Do a little each week instead of leaving it all for the end.
