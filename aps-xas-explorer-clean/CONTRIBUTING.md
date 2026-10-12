# Contributing

Install dependencies with `pnpm install --frozen-lockfile`, then run `pnpm dev`.

## Code organization

- `src/content/dashboard/DashboardContent.jsx`: dataset explorer and methods view.
- `src/content/dashboard/explorer.css`: explorer styling.
- `src/components/` and other `src/` modules: shared UI infrastructure.
- `tools/ingest.py`: SPEC file ingestion.
- `tools/validate.py`: collection-specific scientific checks.
- `public/raw/`: original files; do not edit acquisition records to fix metadata.

## Before committing

Run `pnpm validate` and `pnpm build:pages`. Inspect both tabs, sample and element selections, signal and energy controls, CSV export, and original downloads in a browser. Check narrow-screen layout as well.

Keep dataset metadata issues explicit. Do not describe derived or corrected signals as original measurements. Changing collection scope requires updating validation expectations and documentation.

Commit rebuilt `docs/` with the source changes. GitHub Pages serves `main:/docs`. Do not commit node_modules or development caches. Preserve dependency licenses and notices.
