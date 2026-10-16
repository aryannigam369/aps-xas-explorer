# Demeter and Larch export

The explorer now offers two exports for the active element, sample, signal, scan selection, and energy window:

- **CSV**: long-form rows for spreadsheet work and general analysis.
- **Demeter/Larch `.dat`**: whitespace-delimited ASCII columns with comment headers. The first column is energy in eV (or relative energy in eV); each following column is one selected scan.

The `.dat` file can be imported in Athena through **File → Import data**. Select the first column as energy and the remaining column or columns as detector/signal data. Larch can read the same file with its ASCII reader, for example:

```python
from larch.io import read_ascii
group = read_ascii("T20-Zn-fluoA-near.dat")
```

The exported signal is the signal shown in the plot. For fluorescence A/B, it is the uncorrected ratio `flatot / i0` or `flbtot / i0`. The export does not apply calibration, smoothing, averaging, background subtraction, edge-step normalization, or structural fitting. Original SPEC files remain available for full beamline provenance.

The header records the dataset, element, sample selection, signal, energy mode, window, and source scan files. If the data are modified outside the explorer, retain the header and record the processing step in the analysis notebook or project journal.
