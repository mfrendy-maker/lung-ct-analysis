"""Data acquisition: CMB-LCA (TCIA) cancer CTs and DICOM -> NIfTI conversion."""
from pathlib import Path

import SimpleITK as sitk


def download_cmb_lca(out_dir: str, max_series: int = 5) -> list[Path]:
    """Download CT series of the CMB-LCA collection from TCIA (public, no login)."""
    from tcia_utils import nbia

    series = nbia.getSeries(collection="CMB-LCA", modality="CT")
    if not series:
        raise RuntimeError("No CT series returned for CMB-LCA")
    series = series[:max_series]
    nbia.downloadSeries(series, path=out_dir, input_type="list")
    return sorted(p for p in Path(out_dir).iterdir() if p.is_dir())


def dicom_to_nifti(dicom_dir: str, out_file: str) -> str:
    reader = sitk.ImageSeriesReader()
    files = reader.GetGDCMSeriesFileNames(dicom_dir)
    if not files:
        raise FileNotFoundError(f"No DICOM series in {dicom_dir}")
    reader.SetFileNames(files)
    Path(out_file).parent.mkdir(parents=True, exist_ok=True)
    sitk.WriteImage(reader.Execute(), out_file)
    return out_file
