"""Prepare CST project copies for queued micro-loop samples.

中文：根据 `cst_micro_loop_queue.csv` 复制周期/非周期 CST 工程副本，并写入参数元数据。
English: Copy periodic/nonperiodic CST project templates for queued micro-loop samples and write parameter metadata.
"""

from __future__ import annotations

import argparse
import csv
import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any


TASK_ROOT = Path(r"E:\aris\meta\cst_coupling_model1")
DEFAULT_SOURCE_DIR = TASK_ROOT / "cst_projects" / "export_probe_ascii"
DEFAULT_QUEUE = TASK_ROOT / "data" / "cst_micro_loop_queue.csv"
DEFAULT_MANIFEST = TASK_ROOT / "data" / "nonperiodic_center_matched_samples.csv"
DEFAULT_PREPARED_QUEUE = TASK_ROOT / "data" / "cst_micro_loop_queue_prepared.csv"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"No rows to write: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def safe_copy_project(source_dir: Path, dest_dir: Path, overwrite: bool) -> Path:
    source_dir = source_dir.resolve()
    dest_dir = dest_dir.resolve()
    task_root = TASK_ROOT.resolve()
    if task_root not in dest_dir.parents and dest_dir != task_root:
        raise ValueError(f"Destination must stay under task root: {dest_dir}")
    if not (source_dir / "model1.cst").exists():
        raise FileNotFoundError(f"Missing source CST file: {source_dir / 'model1.cst'}")
    if dest_dir.exists():
        if not overwrite:
            return dest_dir / "model1.cst"
        shutil.rmtree(dest_dir)
    shutil.copytree(source_dir, dest_dir)
    return dest_dir / "model1.cst"


def update_parameter_json(project_dir: Path, atheta: float, pphi: float) -> None:
    parameter_path = project_dir / "model1" / "Model" / "Parameters.json"
    if not parameter_path.exists():
        return
    data = json.loads(parameter_path.read_text(encoding="utf-8"))
    for parameter in data.get("parameters", []):
        if parameter.get("name") == "Atheta":
            parameter["expr"] = f"{atheta:.6f}"
            parameter["value"] = f"{atheta:.6f}"
        elif parameter.get("name") == "Pphi":
            parameter["expr"] = f"{pphi:.6f}"
            parameter["value"] = f"{pphi:.6f}"
        elif parameter.get("name") == "gap":
            gap = 180.0 - pphi
            parameter["expr"] = f"{gap:.6f}"
            parameter["value"] = f"{gap:.6f}"
    parameter_path.write_text(json.dumps(data, indent=4, ensure_ascii=False), encoding="utf-8")


def sample_parameters(sample: dict[str, str]) -> dict[str, Any]:
    cells = ["L2", "L1", "C", "R1", "R2"]
    return {
        cell: {
            "Atheta": float(sample[f"{cell}_Atheta"]),
            "Pphi": float(sample[f"{cell}_Pphi"]),
        }
        for cell in cells
    }


def write_metadata(
    project_dir: Path,
    sample: dict[str, str],
    queue_row: dict[str, str],
    project_kind: str,
) -> None:
    periodic_atheta = float(queue_row["periodic_Atheta"])
    periodic_pphi = float(queue_row["periodic_Pphi"])
    metadata = {
        "sample_id": sample["sample_id"],
        "center_sample_id": sample.get("center_sample_id", sample["sample_id"]),
        "periodic_sample_id": sample.get(
            "periodic_sample_id", queue_row.get("periodic_sample_id", "")
        ),
        "repeat_id": sample.get("repeat_id", ""),
        "neighbor_seed": sample.get("neighbor_seed", ""),
        "perturbation_tier": sample.get("perturbation_tier", ""),
        "neighbor_contrast_mean": sample.get("neighbor_contrast_mean", ""),
        "neighbor_contrast_max": sample.get("neighbor_contrast_max", ""),
        "project_kind": project_kind,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "source_project": str(DEFAULT_SOURCE_DIR),
        "response_channel": "SZmax(2),Zmin(1)",
        "label_band_ghz": [6.0, 24.0],
        "periodic_baseline": {
            "Atheta": periodic_atheta,
            "Pphi": periodic_pphi,
            "rule_zh": "周期基准使用中心单元 C 的 Atheta/Pphi。",
            "rule_en": "The periodic baseline uses the center-cell C Atheta/Pphi.",
        },
        "five_cell_parameters": sample_parameters(sample),
        "neighbor_uniqueness_rule": {
            "zh": "五个单元的参数对、Atheta、Pphi 均不能重复。",
            "en": "The five cells must have unique parameter pairs, unique Atheta values, and unique Pphi values.",
        },
        "cst_model_status": {
            "zh": (
                "当前为标准单元工程副本。periodic 副本可作为周期单元模板；"
                "nonperiodic 副本已记录五单元参数，但尚未完成五单元几何拼接。"
            ),
            "en": (
                "This is currently a standard unit-cell project copy. The periodic copy "
                "can serve as the periodic unit-cell template; the nonperiodic copy records "
                "the five-cell parameters but does not yet contain the assembled five-cell geometry."
            ),
        },
    }
    (project_dir / "micro_loop_metadata.json").write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", default=DEFAULT_SOURCE_DIR, type=Path)
    parser.add_argument("--queue", default=DEFAULT_QUEUE, type=Path)
    parser.add_argument("--manifest", default=DEFAULT_MANIFEST, type=Path)
    parser.add_argument("--prepared-queue", default=DEFAULT_PREPARED_QUEUE, type=Path)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    queue_rows = read_csv(args.queue)
    manifest_rows = {row["sample_id"]: row for row in read_csv(args.manifest)}
    prepared_rows: list[dict[str, Any]] = []

    for queue_row in queue_rows:
        sample_id = queue_row["sample_id"]
        sample = manifest_rows[sample_id]
        periodic_dir = Path(queue_row["periodic_project_dir"])
        nonperiodic_dir = Path(queue_row["nonperiodic_project_dir"])

        periodic_cst = safe_copy_project(args.source_dir, periodic_dir, args.overwrite)
        nonperiodic_cst = safe_copy_project(args.source_dir, nonperiodic_dir, args.overwrite)

        periodic_atheta = float(queue_row["periodic_Atheta"])
        periodic_pphi = float(queue_row["periodic_Pphi"])
        update_parameter_json(periodic_dir, periodic_atheta, periodic_pphi)
        update_parameter_json(
            nonperiodic_dir, float(sample["C_Atheta"]), float(sample["C_Pphi"])
        )
        write_metadata(periodic_dir, sample, queue_row, "periodic")
        write_metadata(nonperiodic_dir, sample, queue_row, "nonperiodic")

        prepared = dict(queue_row)
        prepared.update(
            {
                "status": "project_copies_prepared",
                "periodic_project_cst": str(periodic_cst),
                "nonperiodic_project_cst": str(nonperiodic_cst),
                "periodic_project_status": "unit_cell_template_copy_prepared",
                "nonperiodic_project_status": "metadata_prepared_geometry_assembly_pending",
            }
        )
        prepared_rows.append(prepared)

    write_csv(args.prepared_queue, prepared_rows)
    print(f"prepared_rows: {len(prepared_rows)}")
    print(f"prepared_queue: {args.prepared_queue.resolve()}")
    for row in prepared_rows:
        print(f"{row['sample_id']}: {row['status']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
