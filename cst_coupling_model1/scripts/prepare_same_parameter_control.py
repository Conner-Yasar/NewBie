"""Prepare a same-parameter five-cell control project for pilot_0070.

中文：生成五个单元都等于中心单元参数的对照 CST 工程。
English: Generate a CST control project where all five cells equal the center-cell parameters.
"""

from __future__ import annotations

import argparse
import csv
import json
import shutil
from datetime import datetime
from pathlib import Path


TASK_ROOT = Path(r"E:\aris\meta\cst_coupling_model1")
DEFAULT_SOURCE_DIR = TASK_ROOT / "cst_projects" / "export_probe_ascii"
DEFAULT_SAMPLE_ID = "pilot_0070_same_center"
DEFAULT_SOURCE_SAMPLE = "grid_05506_np_r04"
DEFAULT_MANIFEST = TASK_ROOT / "data" / "nonperiodic_center_matched_samples.csv"
DEFAULT_PROJECT_DIR = TASK_ROOT / "cst_projects" / "nonperiodic" / DEFAULT_SAMPLE_ID


def read_manifest_row(path: Path, sample_id: str) -> dict[str, str]:
    with path.open("r", newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            if row["sample_id"] == sample_id:
                return row
    raise ValueError(f"Sample not found: {sample_id}")


def copy_project(source_dir: Path, project_dir: Path, overwrite: bool) -> Path:
    source_dir = source_dir.resolve()
    project_dir = project_dir.resolve()
    task_root = TASK_ROOT.resolve()
    if task_root not in project_dir.parents:
        raise ValueError(f"Project directory must stay under task root: {project_dir}")
    if project_dir.exists():
        if overwrite:
            shutil.rmtree(project_dir)
        else:
            return project_dir / "model1.cst"
    shutil.copytree(source_dir, project_dir)
    return project_dir / "model1.cst"


def write_metadata(project_dir: Path, source_row: dict[str, str], sample_id: str) -> None:
    c_atheta = float(source_row["C_Atheta"])
    c_pphi = float(source_row["C_Pphi"])
    metadata = {
        "sample_id": sample_id,
        "project_kind": "nonperiodic_same_parameter_control",
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "source_sample_id": source_row["sample_id"],
        "center_sample_id": source_row.get("center_sample_id", source_row["sample_id"]),
        "periodic_sample_id": source_row.get("periodic_sample_id", ""),
        "repeat_id": source_row.get("repeat_id", ""),
        "perturbation_tier": source_row.get("perturbation_tier", ""),
        "neighbor_contrast_mean": source_row.get("neighbor_contrast_mean", ""),
        "neighbor_contrast_max": source_row.get("neighbor_contrast_max", ""),
        "response_channel": "SZmax(2),Zmin(1)",
        "label_band_ghz": [6.0, 24.0],
        "periodic_baseline": {
            "Atheta": c_atheta,
            "Pphi": c_pphi,
            "rule_zh": "周期基准使用中心单元 C 的 Atheta/Pphi。",
            "rule_en": "The periodic baseline uses the center-cell C Atheta/Pphi.",
        },
        "five_cell_parameters": {
            cell: {"Atheta": c_atheta, "Pphi": c_pphi}
            for cell in ["L2", "L1", "C", "R1", "R2"]
        },
        "control_purpose": {
            "zh": "五个单元全部等于中心单元参数，用于检查五单元超胞边界/端口是否自身引入大差异。",
            "en": "All five cells equal the center-cell parameters, testing whether the five-cell supercell boundary/ports introduce a large difference by themselves.",
        },
    }
    (project_dir / "micro_loop_metadata.json").write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", default=DEFAULT_SOURCE_DIR, type=Path)
    parser.add_argument("--manifest", default=DEFAULT_MANIFEST, type=Path)
    parser.add_argument("--source-sample-id", default=DEFAULT_SOURCE_SAMPLE)
    parser.add_argument("--sample-id", default=DEFAULT_SAMPLE_ID)
    parser.add_argument("--project-dir", default=DEFAULT_PROJECT_DIR, type=Path)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    source_row = read_manifest_row(args.manifest, args.source_sample_id)
    cst = copy_project(args.source_dir, args.project_dir, args.overwrite)
    write_metadata(args.project_dir, source_row, args.sample_id)
    print(f"sample_id: {args.sample_id}")
    print(f"project: {cst.resolve()}")
    print(f"C_Atheta: {source_row['C_Atheta']}")
    print(f"C_Pphi: {source_row['C_Pphi']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
