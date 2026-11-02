# lung-ct-analysis

Detects lung lesions on CT, grades severity and classifies the abnormality.

- Cancer data: [CMB-LCA on TCIA](https://www.cancerimagingarchive.net/collection/cmb-lca/)
- Lung segmentation / normal-lung reference: [TotalSegmentator](https://github.com/wasserth/TotalSegmentator)

Note: TotalSegmentator is a segmentation model, not a dataset of normal CTs. Use it to
extract lung masks; for normal-lung controls use CT scans with no lesions
(e.g. its Zenodo training set, or any healthy CT) and run the same pipeline.

## Pipeline
1. `lungct download` - fetch CMB-LCA CT series (TCIA NBIA API).
2. `lungct convert <dicom_dir> <out.nii.gz>` - DICOM to NIfTI.
3. `lungct analyse <ct.nii.gz>` - TotalSegmentator lung lobes, then lesion candidates
   (HU > -400 inside the eroded lung, vessel-removing opening, connected components).
4. Each lesion gets diameter, mean HU, sphericity, a type
   (ground-glass / part-solid / solid / spiculated nodule / mass) and a severity
   (low / moderate / high / critical) using Lung-RADS-style size thresholds.
5. Scan label: `normal` (no lesions) or `abnormal` with worst severity. Output: `outputs/report.json`.

## Install
```
pip install -e .
```

Rule-based and not validated clinically; research use only, not for diagnosis.
