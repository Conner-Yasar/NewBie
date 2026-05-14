"""Generate center-matched periodic and nonperiodic sampling manifests.

中文：生成“周期全网格 + 中心匹配非周期五单元窗口”的采样表。
English: Generate the periodic full grid plus center-matched nonperiodic five-cell windows.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import random
from pathlib import Path
from typing import Any


TASK_ROOT = Path(r"E:\aris\meta\cst_coupling_model1")
DEFAULT_CONFIG = TASK_ROOT / "configs" / "sampling_pilot.json"
DEFAULT_PERIODIC_OUTPUT = TASK_ROOT / "data" / "periodic_full_grid.csv"
DEFAULT_NONPERIODIC_OUTPUT = TASK_ROOT / "data" / "nonperiodic_center_matched_samples.csv"
DEFAULT_MICRO_OUTPUT = TASK_ROOT / "data" / "micro_loop_candidates.csv"
DEFAULT_QUEUE_OUTPUT = TASK_ROOT / "data" / "cst_micro_loop_queue.csv"

CELLS = ["L2", "L1", "C", "R1", "R2"]
NEIGHBOR_CELLS = ["L2", "L1", "R1", "R2"]
VARIABLES = ["Atheta", "Pphi"]


def load_config(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def stepped_values(start: float, stop: float, step: float) -> list[float]:
    if step == 0:
        raise ValueError("step must not be zero")
    direction = 1 if stop >= start else -1
    if direction * step <= 0:
        raise ValueError(f"step {step} does not move from {start} to {stop}")

    values: list[float] = []
    current = start
    epsilon = abs(step) / 1000.0
    while direction * (stop - current) >= -epsilon:
        values.append(round(current, 6))
        current += step
    return values


def angle_grid(config: dict[str, Any]) -> list[tuple[float, float]]:
    variables = config["variables"]
    atheta_spec = variables["Atheta"]
    pphi_spec = variables["Pphi"]
    atheta_values = stepped_values(
        float(atheta_spec["start_deg"]),
        float(atheta_spec["stop_deg"]),
        float(atheta_spec["step_deg"]),
    )
    pphi_values = stepped_values(
        float(pphi_spec["start_deg"]),
        float(pphi_spec["stop_deg"]),
        float(pphi_spec["step_deg"]),
    )
    return [(atheta, pphi) for atheta in atheta_values for pphi in pphi_values]


def angle_values(config: dict[str, Any]) -> tuple[list[float], list[float]]:
    variables = config["variables"]
    atheta_spec = variables["Atheta"]
    pphi_spec = variables["Pphi"]
    return (
        stepped_values(
            float(atheta_spec["start_deg"]),
            float(atheta_spec["stop_deg"]),
            float(atheta_spec["step_deg"]),
        ),
        stepped_values(
            float(pphi_spec["start_deg"]),
            float(pphi_spec["stop_deg"]),
            float(pphi_spec["step_deg"]),
        ),
    )


def sample_id(index: int) -> str:
    return f"grid_{index:05d}"


def periodic_rows(grid: list[tuple[float, float]], config: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, (atheta, pphi) in enumerate(grid, start=1):
        sid = sample_id(index)
        rows.append(
            {
                "sample_id": sid,
                "sampling_stage": config["sampling_stage"],
                "sampling_method": "periodic_full_grid",
                "grid_index": index,
                "Atheta": atheta,
                "Pphi": pphi,
                "periodic_Atheta": atheta,
                "periodic_Pphi": pphi,
            }
        )
    return rows


def normalized_atheta(value: float) -> float:
    return (value - (-45.0)) / 45.0


def normalized_pphi(value: float) -> float:
    return (value - 50.0) / 120.0


def pair_distance(a_theta: float, p_phi: float, c_theta: float, c_phi: float) -> float:
    return math.hypot(
        normalized_atheta(a_theta) - normalized_atheta(c_theta),
        normalized_pphi(p_phi) - normalized_pphi(c_phi),
    )


def center_distance_from_midrange(c_theta: float, c_phi: float) -> float:
    return math.hypot(normalized_atheta(c_theta) - 0.5, normalized_pphi(c_phi) - 0.5)


def choose_unique_neighbors(
    atheta_values: list[float],
    pphi_values: list[float],
    center: tuple[float, float],
    rng: random.Random,
) -> dict[str, tuple[float, float]]:
    available_atheta = [value for value in atheta_values if value != center[0]]
    available_pphi = [value for value in pphi_values if value != center[1]]
    if len(available_atheta) < len(NEIGHBOR_CELLS):
        raise ValueError(f"Not enough unique Atheta values for center {center}")
    if len(available_pphi) < len(NEIGHBOR_CELLS):
        raise ValueError(f"Not enough unique Pphi values for center {center}")

    sampled_atheta = rng.sample(available_atheta, k=len(NEIGHBOR_CELLS))
    sampled_pphi = rng.sample(available_pphi, k=len(NEIGHBOR_CELLS))
    rng.shuffle(sampled_pphi)
    return {
        cell: (sampled_atheta[index], sampled_pphi[index])
        for index, cell in enumerate(NEIGHBOR_CELLS)
    }


def row_metrics(row: dict[str, Any]) -> dict[str, float]:
    c_theta = float(row["C_Atheta"])
    c_phi = float(row["C_Pphi"])
    distances = [
        pair_distance(
            float(row[f"{cell}_Atheta"]),
            float(row[f"{cell}_Pphi"]),
            c_theta,
            c_phi,
        )
        for cell in NEIGHBOR_CELLS
    ]
    return {
        "neighbor_contrast_mean": round(sum(distances) / len(distances), 6),
        "neighbor_contrast_max": round(max(distances), 6),
        "center_distance_from_midrange": round(center_distance_from_midrange(c_theta, c_phi), 6),
    }


def nonperiodic_rows(
    grid: list[tuple[float, float]],
    config: dict[str, Any],
) -> list[dict[str, Any]]:
    seed = int(config["random_seed"])
    repeat_count = int(config.get("nonperiodic_repeats_per_center", 1))
    atheta_values, pphi_values = angle_values(config)
    rows: list[dict[str, Any]] = []

    for index, center in enumerate(grid, start=1):
        center_id = sample_id(index)
        for repeat_id in range(repeat_count):
            row_seed = seed + index * 1009 + repeat_id
            rng = random.Random(row_seed)
            neighbors = choose_unique_neighbors(atheta_values, pphi_values, center, rng)
            row: dict[str, Any] = {
                "sample_id": f"{center_id}_np_r{repeat_id + 1:02d}",
                "center_sample_id": center_id,
                "sampling_stage": config["sampling_stage"],
                "sampling_method": "center_matched_random_neighbors",
                "grid_index": index,
                "repeat_id": repeat_id + 1,
                "neighbor_seed": row_seed,
                "center_Atheta": center[0],
                "center_Pphi": center[1],
            }
            for cell in CELLS:
                atheta, pphi = center if cell == "C" else neighbors[cell]
                row[f"{cell}_Atheta"] = atheta
                row[f"{cell}_Pphi"] = pphi
            row["periodic_sample_id"] = center_id
            row["periodic_Atheta"] = center[0]
            row["periodic_Pphi"] = center[1]
            row.update(row_metrics(row))
            row["selected_for_micro_loop"] = "no"
            row["micro_loop_role"] = ""
            rows.append(row)
    assign_perturbation_tiers(rows)
    return rows


def assign_perturbation_tiers(rows: list[dict[str, Any]]) -> None:
    sorted_rows = sorted(rows, key=lambda row: float(row["neighbor_contrast_mean"]))
    total = len(sorted_rows)
    for rank, row in enumerate(sorted_rows):
        fraction = rank / total
        if fraction < 1 / 3:
            tier = "low"
        elif fraction < 2 / 3:
            tier = "medium"
        else:
            tier = "high"
        row["perturbation_tier"] = tier


def assert_unique_cell_pairs(row: dict[str, Any]) -> None:
    pairs = [
        (float(row[f"{cell}_Atheta"]), float(row[f"{cell}_Pphi"]))
        for cell in CELLS
    ]
    if len(set(pairs)) != len(pairs):
        raise ValueError(f"Duplicate cell pair in {row['sample_id']}: {pairs}")
    atheta_values = [pair[0] for pair in pairs]
    if len(set(atheta_values)) != len(atheta_values):
        raise ValueError(f"Duplicate Atheta in {row['sample_id']}: {atheta_values}")
    pphi_values = [pair[1] for pair in pairs]
    if len(set(pphi_values)) != len(pphi_values):
        raise ValueError(f"Duplicate Pphi in {row['sample_id']}: {pphi_values}")


def validate_rows(periodic: list[dict[str, Any]], nonperiodic: list[dict[str, Any]]) -> None:
    periodic_pairs = {
        (row["sample_id"], float(row["Atheta"]), float(row["Pphi"]))
        for row in periodic
    }
    periodic_by_id = {
        row["sample_id"]: (float(row["Atheta"]), float(row["Pphi"]))
        for row in periodic
    }
    if len(periodic_pairs) != len(periodic):
        raise ValueError("Periodic grid contains duplicate sample IDs or angle pairs")

    for row in nonperiodic:
        assert_unique_cell_pairs(row)
        periodic_pair = periodic_by_id[str(row["periodic_sample_id"])]
        center_pair = (float(row["C_Atheta"]), float(row["C_Pphi"]))
        if periodic_pair != center_pair:
            raise ValueError(
                f"Center mismatch in {row['sample_id']}: {center_pair} != {periodic_pair}"
            )


def select_micro_loop_candidates(rows: list[dict[str, Any]], count: int) -> list[dict[str, Any]]:
    if count < 1:
        return []

    low_pool = [row for row in rows if row.get("perturbation_tier") == "low"]
    low = min(
        low_pool,
        key=lambda row: (
            float(row["center_distance_from_midrange"]),
            float(row["neighbor_contrast_mean"]),
        ),
    )
    medium_pool = [row for row in rows if row.get("perturbation_tier") == "medium"]
    median = min(
        medium_pool,
        key=lambda row: (
            float(row["center_distance_from_midrange"]),
            abs(float(row["neighbor_contrast_mean"]) - 0.5),
        ),
    )
    high_pool = [row for row in rows if row.get("perturbation_tier") == "high"]
    high = max(high_pool, key=lambda row: float(row["neighbor_contrast_max"]))

    candidates: list[tuple[str, dict[str, Any]]] = [
        ("low_perturbation_centered", low),
        ("medium_perturbation", median),
        ("high_perturbation", high),
    ]

    selected: list[dict[str, Any]] = []
    seen: set[str] = set()
    for role, row in candidates:
        if row["sample_id"] in seen:
            continue
        copied = dict(row)
        copied["selected_for_micro_loop"] = "yes"
        copied["micro_loop_role"] = role
        selected.append(copied)
        seen.add(str(row["sample_id"]))
        if len(selected) == count:
            break
    return selected


def write_rows(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"No rows to write: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    with tmp_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    tmp_path.replace(path)


def build_micro_loop_queue(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    queue: list[dict[str, Any]] = []
    for row in rows:
        sample = str(row["sample_id"])
        periodic = str(row["periodic_sample_id"])
        queue.append(
            {
                "sample_id": sample,
                "periodic_sample_id": periodic,
                "micro_loop_role": row["micro_loop_role"],
                "perturbation_tier": row["perturbation_tier"],
                "status": "queued_for_cst_project_generation",
                "periodic_Atheta": row["periodic_Atheta"],
                "periodic_Pphi": row["periodic_Pphi"],
                "periodic_project_dir": rf"{TASK_ROOT}\cst_projects\periodic\{periodic}",
                "nonperiodic_project_dir": rf"{TASK_ROOT}\cst_projects\nonperiodic\{sample}",
                "periodic_result_csv": rf"{TASK_ROOT}\data\raw\periodic\{periodic}_szmax2_zmin1.csv",
                "nonperiodic_result_csv": rf"{TASK_ROOT}\data\raw\nonperiodic\{sample}_five_cell_szmax2_zmin1.csv",
                "corrected_label_output_csv": rf"{TASK_ROOT}\data\processed\{sample}_corrected_label.csv",
            }
        )
    return queue


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default=DEFAULT_CONFIG, type=Path)
    parser.add_argument("--periodic-output", default=DEFAULT_PERIODIC_OUTPUT, type=Path)
    parser.add_argument("--nonperiodic-output", default=DEFAULT_NONPERIODIC_OUTPUT, type=Path)
    parser.add_argument("--micro-output", default=DEFAULT_MICRO_OUTPUT, type=Path)
    parser.add_argument("--queue-output", default=DEFAULT_QUEUE_OUTPUT, type=Path)
    args = parser.parse_args()

    config = load_config(args.config)
    grid = angle_grid(config)
    periodic = periodic_rows(grid, config)
    nonperiodic = nonperiodic_rows(grid, config)
    validate_rows(periodic, nonperiodic)
    micro_rows = select_micro_loop_candidates(
        nonperiodic, int(config.get("micro_loop_candidate_count", 3))
    )
    queue_rows = build_micro_loop_queue(micro_rows)

    write_rows(args.periodic_output, periodic)
    write_rows(args.nonperiodic_output, nonperiodic)
    write_rows(args.micro_output, micro_rows)
    write_rows(args.queue_output, queue_rows)

    print(f"periodic_full_grid: {len(periodic)}")
    print(f"nonperiodic_center_matched: {len(nonperiodic)}")
    print(f"micro_loop_candidates: {len(micro_rows)}")
    print(f"periodic_output: {args.periodic_output.resolve()}")
    print(f"nonperiodic_output: {args.nonperiodic_output.resolve()}")
    print(f"micro_output: {args.micro_output.resolve()}")
    print(f"queue_output: {args.queue_output.resolve()}")
    for row in micro_rows:
        print(
            f"{row['sample_id']}: {row['micro_loop_role']}, "
            f"center=({row['C_Atheta']}, {row['C_Pphi']}), "
            f"tier={row['perturbation_tier']}, "
            f"contrast_mean={row['neighbor_contrast_mean']}, "
            f"contrast_max={row['neighbor_contrast_max']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
