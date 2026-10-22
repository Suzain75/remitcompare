# PROGRESS.md: RemitCompare

Last updated: 2026-10-22

## Done ✅
- Step 1: Defined the project, stack and goals
- Step 2: Planned the MVP. See `docs/PROJECT_SPEC.md` (4 corridors, 4 features, 4 tables, 4 endpoints, 3-4 week scope)
- Step 3: Repo + rates API check
  - Public GitHub repo created: https://github.com/Suzain75/remitcompare
  - Folders: `backend/`, `frontend/`, `docs/`; `.gitignore` keeps `.env` out of Git; README placeholder
  - First commit pushed to `main`
  - Rates API test passed: `open.er-api.com` returned QAR-based rates for INR, USD, SAR and PKR

## Decisions made
- Corridors (v1): Qatar to India, USA, Saudi Arabia, Pakistan
- Data: free public rates API (`open.er-api.com`, no key) + manually maintained fee table
- Time budget for v1: 3-4 weeks
- Rates API rules:
  - Show the attribution link "Rates By Exchange Rate API" in the footer
  - Cache rates in the DB, never call the API per user request (once a day is enough)
  - Do not redistribute raw rates (no "all rates" endpoint)
  - Too many requests = HTTP 429, blocked for 20 minutes
  - Watch the `time_eol_unix` field for a shutdown warning
- Plan B if the terms become a problem: free keyed plan (no attribution, 1,500 requests/month)

## Next up
- Step 4: FastAPI skeleton in `backend/` (virtual environment, `/api/health`, first pytest test)

## Open items
- Skim the full Terms page once: https://www.exchangerate-api.com/terms
- Choose about 4 providers to research (must be verifiable from public pages)
- Real fee research: do a little each week
