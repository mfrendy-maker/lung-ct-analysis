import argparse
import json
from pathlib import Path

import nibabel as nib
import numpy as np

from . import data, lesions, segment


def analyse(ct_nifti: str, work_dir: str, fast: bool = True) -> dict:
    img = nib.load(ct_nifti)
    hu = np.asarray(img.dataobj, dtype=np.float32)
    spacing = img.header.get_zooms()[:3]
    lung = segment.segment_lungs(ct_nifti, work_dir, fast=fast)
    found = lesions.detect_lesions(hu, lung, spacing)
    return lesions.classify_scan(found)


def main():
    p = argparse.ArgumentParser(prog="lungct")
    sub = p.add_subparsers(dest="cmd", required=True)

    d = sub.add_parser("download", help="download CMB-LCA CT series from TCIA")
    d.add_argument("--out", default="data/cmb-lca")
    d.add_argument("--max-series", type=int, default=5)

    c = sub.add_parser("convert", help="DICOM series folder -> NIfTI")
    c.add_argument("dicom_dir")
    c.add_argument("out_file")

    a = sub.add_parser("analyse", help="segment lungs, detect lesions, grade and classify")
    a.add_argument("ct_nifti")
    a.add_argument("--out", default="outputs")
    a.add_argument("--full", action="store_true", help="full-resolution TotalSegmentator (slower)")

    args = p.parse_args()
    if args.cmd == "download":
        data.download_cmb_lca(args.out, args.max_series)
    elif args.cmd == "convert":
        print(data.dicom_to_nifti(args.dicom_dir, args.out_file))
    else:
        out = Path(args.out)
        out.mkdir(parents=True, exist_ok=True)
        result = analyse(args.ct_nifti, str(out), fast=not args.full)
        (out / "report.json").write_text(json.dumps(result, indent=2))
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
