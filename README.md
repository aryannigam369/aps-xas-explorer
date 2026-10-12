# APS X-ray Absorption Explorer

An interactive web interface for the **GUP38672_2014-2_12-BM** dataset acquired at the Advanced Photon Source in 2014.

The first deliverable turns the supplied beamline collection into a browsable spectrum explorer with traceable source files and explicit processing definitions.

## Explore the dataset

- Select Fe, Co, Ni, Cu, Zn, or Ga.
- Use the sample × element coverage matrix to select J14, T1, or T20.
- Overlay individual scans and switch between near-edge and full acquisition ranges.
- Inspect recorded channels or clearly labelled fluorescence/I0 ratios.
- Export the plotted measurements as CSV or download original SPEC files.
- Review the acquisition inventory and provenance notes in **Dataset & methods**.

Once GitHub Pages is enabled, the live website is linked under **Settings → Pages → Visit site**. Add that URL to this repository's About panel.

## Collection at a glance

| Measure | Count |
|---|---:|
| Sample IDs | 3 |
| Elements | 6 |
| Main spectroscopy scans | 33 |
| Main measurement points | 15,939 |
| Original source files | 39 |
| All acquisition blocks, including setup | 52 |

The coverage matrix describes measurement availability, not spatial position or elemental concentration. Every main spectrum contains 483 points. All original files remain available for inspection.

## Methods and limitations

The preparation script parses each SPEC scan block separately, validates its column count, converts energy from the supplied keV scale to eV, and retains the recorded measurements. The two fluorescence views calculate `flatot / i0` and `flbtot / i0`. No smoothing or scan averaging is applied.

These are exploratory signal views. No energy-reference calibration, edge-step normalization, EXAFS extraction, Fourier transform, or structural fitting has been applied. Sample descriptions and spatial coordinates were not supplied.

Three J14 copper files contain T20_Cu file headers. The explorer preserves the folder-based assignment and flags the conflict for confirmation. Two J14 nickel scans share the filename label b; both remain separate. A slit-alignment block appended to a T1 copper file is excluded from the main spectra and retained in the supplementary inventory.

## Files

- `docs/`: ready-to-publish static website, reviewed dataset, and source downloads.
- `FULL-SOURCE.zip`: complete editable React/Python authoring project, parser, validation script, and build instructions. Extract locally to inspect or revise the implementation.

The website requires no backend or API key. The Python preparation step runs before publication; the browser displays the prepared data. Publishing this version does not require running Python or installing Node.js.

## Publish

In this repository, select **Settings → Pages → Deploy from a branch → main → /docs → Save**. Keep `docs/.nojekyll` in place. The live site serves the original compiled explorer without a custom build workflow.

To revise the interface, edit and rebuild the authoring project in `FULL-SOURCE.zip`, then replace the contents of `docs/` with the rebuilt `dist/` contents. Preserve the complete data sidecar and download assets.

## Scientific references

- [Demeter](https://bruceravel.github.io/demeter/): XAFS analysis tools.
- [Larch](https://xraypy.github.io/xraylarch/): X-ray spectroscopy processing and analysis.
- [FEFF](https://feff.phys.washington.edu/): theoretical spectroscopy and modelling.

These projects informed the scientific context; this explorer does not claim to reproduce their processing or fitting capabilities.

## Data attribution

Dataset: GUP38672_2014-2_12-BM, supplied APS beamline collection, acquisition dates recorded as July 28, 2014. Sample labels follow the supplied directory structure. No new dataset license or authorship attribution has been invented. Add the dataset owner's approved citation and license when available.
