# PROGRESS.md: RemitCompare

Last updated: 2026-10-22

## Done ✅
- Step 1: Defined the project, stack and goals
- Step 2: Planned the MVP. See `PROJECT_SPEC.md` (4 corridors, 4 features, 4 tables, 4 endpoints, 3-4 week scope)

## Decisions made
- Corridors (revised): Qatar to India, USA, Saudi Arabia, Pakistan (Philippines, Bangladesh, Nepal, China, Japan moved to v2)
- Data: free public rates API (ExchangeRate-API Open Access) + manually maintained fee table
- Time budget for v1 (revised): 3-4 weeks

## Next up
- Step 3: create the GitHub repo, `frontend/` and `backend/` folders, first clean commit
- Test one call to the rates API for all 4 currencies (INR, USD, SAR, PKR) and read its terms

## Open items
- Real fee research is the slow part: aim for real, sourced fees for all 4 corridors, a little each week
- Choose about 4 providers to research (must be verifiable from public pages)
