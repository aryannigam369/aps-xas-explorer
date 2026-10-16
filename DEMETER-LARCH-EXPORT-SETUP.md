# Adding the Demeter/Larch export

This update adds a second button beside **Export plotted CSV**:

`Export Demeter/Larch .dat`

The `.dat` file is a plain ASCII text file. It contains comment headers, energy in eV, and one numeric column for each selected scan. It is suitable for Athena/Demeter import and for Larch's `read_ascii()` reader.

## GitHub update

Copy these files into the top level of the existing repository and replace the matching files:

- `src/content/dashboard/DashboardContent.jsx`
- `src/content/dashboard/explorer.css`
- `README.md`
- `EXPORT-FORMAT.md`
- `docs/index.html`

Keep `docs/raw/`, `docs/raw-data.zip`, `docs/snapshot.*.json`, and `docs/.nojekyll` in place. Commit the source and rebuilt `docs/` together. Keep Pages configured as `main` → `/docs`.

## Scientific behavior

The export follows the current element, sample, signal, scan, energy-window, and relative-energy settings. It exports the plotted values as they are shown. It does not silently apply calibration, smoothing, averaging, background subtraction, edge-step normalization, or fitting. Original SPEC files remain the authoritative source records.
