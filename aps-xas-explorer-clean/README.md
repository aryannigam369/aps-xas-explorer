# APS X-ray Absorption Explorer

[Open the live explorer](https://aryannigam369.github.io/aps-xas-explorer/)

An interactive browser interface for the **GUP38672_2014-2_12-BM** collection acquired at APS in July 2014. Explore 33 individual spectra, three sample labels, six elements, and 15,939 main measurement points.

## Features

- Sample–element coverage matrix and individual scan selection.
- Full-range and near-edge spectra with absolute or relative energy.
- Fluorescence/I0 ratios and recorded signal channels.
- CSV exports, original SPEC downloads, and a methods inventory.

The coverage matrix shows measurement availability, not physical sample positions. Signals are uncorrected; no normalization, smoothing, averaging, or structural fitting is applied.

## Browse the implementation

| Path | Purpose |
| --- | --- |
| [DashboardContent.jsx](src/content/dashboard/DashboardContent.jsx) | Spectrum explorer, plots, controls, and methods view |
| [explorer.css](src/content/dashboard/explorer.css) | Explorer styling |
| [ingest.py](tools/ingest.py) | Parses SPEC blocks and prepares the reviewed dataset |
| [validate.py](tools/validate.py) | Checks counts, source hashes, energy ordering, and calculated ratios |
| [build_site.py](tools/build_site.py) | Builds and validates the website for Pages |
| `src/components/` | Shared interface components |
| `src/data.json` | Prepared dataset and metadata |
| `public/raw/` | Original acquisition files |
| `docs/` | Published website |

## Run locally

Requirements: Node.js 22.12 or later, pnpm, and Python 3. Install dependencies using the supplied lockfile:

```sh
pnpm install --frozen-lockfile
pnpm dev
```

Open the local URL printed by Vite. The implementation uses JavaScript/JSX with React, CSS, HTML, and Python. React is a JavaScript library, not a separate programming language.

To inspect the already-built website without installing JavaScript dependencies:

```sh
python3 -m http.server 4173 --bind 127.0.0.1 --directory docs
```

Open http://127.0.0.1:4173/.

## Validate and build

```sh
python3 tools/validate.py
python3 tools/build_site.py
```

The build compiles the editable source, copies original download assets, validates data, and updates `docs/`. See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidance.

To regenerate the prepared dataset after changing original inputs:

```sh
python3 tools/ingest.py public/raw src/data.json
python3 tools/validate.py
python3 tools/build_site.py
```

The validation script intentionally checks this collection's expected counts; a different collection requires reviewing those expectations.

## GitHub Pages

Keep **Settings → Pages → Deploy from a branch → main → /docs**. Commit updated source and rebuilt `docs/` together. The included validation workflow checks data on pushes and pull requests; it does not deploy or rebuild the website.

Compiled files are marked in `.gitattributes` so GitHub language statistics describe editable code rather than the bundled HTML. No language percentages are manually assigned.

## Scientific scope

The sample labels are J14, T1, and T20; sample compositions were not supplied. Each main scan contains 483 points. Energy is converted from keV to eV; fluorescence ratios use the recorded I0. Nominal edges come from acquisition headers and are not fitted edge positions.

Known metadata issues include three J14 Cu files whose headers identify T20 and duplicate J14 Ni filename labels. Extra setup scans are preserved in the inventory but excluded from main spectra. Acquisition dates use `#D` headers because epoch fields are inconsistent.

## Development and reuse

This project combines dataset-specific Python/React code with a shared interface runtime and open-source dependencies. Dataset provenance and calculation checks are included for review. No new license for the supplied experimental data is asserted; original notices are retained.
