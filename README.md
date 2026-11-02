# lung-ct-analysis

> Superseded by [Lung-Cancer-Imaging-Analysis](https://github.com/mfrendy-maker/Lung-Cancer-Imaging-Analysis),
> which contains this lesion pipeline plus tests, CI, a torch-free lung mask and cancer-vs-normal comparison.
> This repository is kept only as the original prototype.

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
5. Scan label: `normal` (no lesions) or `abnormal` with worst severity. Output: `outputs/report.json` plus annotated PNGs in `outputs/images/` (one per lesion: axial slice, lung outline, lesion contour coloured by severity, type/size/severity title; or `overview.png` for normal scans).

## Install
```
pip install -e .
```

Rule-based and not validated clinically; research use only, not for diagnosis.
