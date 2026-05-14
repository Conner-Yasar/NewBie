"""Analyze S-parameter magnitude/phase spike synchrony for one sample.

Chinese: 分析目标 S 参数的幅值/相位尖峰，并检查其它通道是否同步变化。
English: Analyze target S-parameter magnitude/phase spikes and synchrony in other channels.
"""

from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path


TASK_ROOT = Path(r"E:\aris\meta\cst_coupling_model1")
DEFAULT_TARGET = (
    TASK_ROOT
    / "data"
    / "raw"
    / "nonperiodic"
    / "grid_05506_np_r04_five_cell_szmax2_zmin1.csv"
)
DEFAULT_SPARAM_DIR = TASK_ROOT / "data" / "raw" / "sparam_probe" / "grid_05506_np_r04"
DEFAULT_OUTPUT = TASK_ROOT / "reports" / "grid_05506_np_r04_sparam_spike_analysis.csv"
DEFAULT_PHASE_OUTPUT = TASK_ROOT / "data" / "processed" / "grid_05506_np_r04_target_phase.csv"


def read_complex_csv(path: Path) -> list[dict[str, float]]:
    with path.open("r", newline="", encoding="utf-8-sig") as f:
        rows = []
        for row in csv.DictReader(f):
            real = float(row["real"])
            imag = float(row["imag"])
            phase = math.atan2(imag, real)
            rows.append(
                {
                    "frequency_ghz": float(row["frequency_ghz"]),
                    "real": real,
                    "imag": imag,
                    "magnitude": float(row["magnitude"]),
                    "phase_rad": phase,
                    "phase_deg": math.degrees(phase),
                }
            )
    return rows


def unwrap(phases: list[float]) -> list[float]:
    if not phases:
        return []
    unwrapped = [phases[0]]
    offset = 0.0
    previous = phases[0]
    for phase in phases[1:]:
        delta = phase - previous
        if delta > math.pi:
            offset -= 2 * math.pi
        elif delta < -math.pi:
            offset += 2 * math.pi
        unwrapped.append(phase + offset)
        previous = phase
    return unwrapped


def add_unwrapped_phase(rows: list[dict[str, float]]) -> None:
    phases = unwrap([row["phase_rad"] for row in rows])
    for row, phase in zip(rows, phases):
        row["phase_unwrapped_rad"] = phase
        row["phase_unwrapped_deg"] = math.degrees(phase)


def point_jumps(rows: list[dict[str, float]]) -> list[dict[str, float]]:
    jumps = []
    for i in range(len(rows) - 1):
        jumps.append(
            {
                "index": i,
                "frequency_left_ghz": rows[i]["frequency_ghz"],
                "frequency_right_ghz": rows[i + 1]["frequency_ghz"],
                "frequency_mid_ghz": (rows[i]["frequency_ghz"] + rows[i + 1]["frequency_ghz"]) / 2,
                "magnitude_jump": abs(rows[i + 1]["magnitude"] - rows[i]["magnitude"]),
                "phase_jump_deg": abs(
                    rows[i + 1]["phase_unwrapped_deg"] - rows[i]["phase_unwrapped_deg"]
                ),
            }
        )
    return jumps


def channel_name(path: Path) -> str:
    return path.stem.replace("__", "),").replace("_", "")


def write_phase_csv(path: Path, rows: list[dict[str, float]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "frequency_ghz",
                "real",
                "imag",
                "magnitude",
                "phase_deg",
                "phase_unwrapped_deg",
            ],
        )
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row[key] for key in writer.fieldnames})


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", default=DEFAULT_TARGET, type=Path)
    parser.add_argument("--sparam-dir", default=DEFAULT_SPARAM_DIR, type=Path)
    parser.add_argument("--output", default=DEFAULT_OUTPUT, type=Path)
    parser.add_argument("--phase-output", default=DEFAULT_PHASE_OUTPUT, type=Path)
    parser.add_argument("--top-k", default=20, type=int)
    args = parser.parse_args()

    target = read_complex_csv(args.target)
    add_unwrapped_phase(target)
    write_phase_csv(args.phase_output, target)
    target_jumps = sorted(point_jumps(target), key=lambda row: row["magnitude_jump"], reverse=True)

    channels: dict[str, list[dict[str, float]]] = {}
    for path in sorted(args.sparam_dir.glob("*.csv")):
        rows = read_complex_csv(path)
        add_unwrapped_phase(rows)
        channels[path.stem] = rows

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "rank",
            "frequency_left_ghz",
            "frequency_right_ghz",
            "frequency_mid_ghz",
            "target_magnitude_jump",
            "target_phase_jump_deg",
            "channel",
            "channel_magnitude_jump",
            "channel_phase_jump_deg",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for rank, jump in enumerate(target_jumps[: args.top_k], start=1):
            idx = int(jump["index"])
            for name, rows in channels.items():
                if idx >= len(rows) - 1:
                    continue
                writer.writerow(
                    {
                        "rank": rank,
                        "frequency_left_ghz": jump["frequency_left_ghz"],
                        "frequency_right_ghz": jump["frequency_right_ghz"],
                        "frequency_mid_ghz": jump["frequency_mid_ghz"],
                        "target_magnitude_jump": jump["magnitude_jump"],
                        "target_phase_jump_deg": jump["phase_jump_deg"],
                        "channel": name,
                        "channel_magnitude_jump": abs(
                            rows[idx + 1]["magnitude"] - rows[idx]["magnitude"]
                        ),
                        "channel_phase_jump_deg": abs(
                            rows[idx + 1]["phase_unwrapped_deg"]
                            - rows[idx]["phase_unwrapped_deg"]
                        ),
                    }
                )

    print(f"target_points: {len(target)}")
    print(f"channels: {len(channels)}")
    print(f"phase_output: {args.phase_output.resolve()}")
    print(f"output: {args.output.resolve()}")
    print("top_target_jumps:")
    for jump in target_jumps[:5]:
        print(
            f"  {jump['frequency_left_ghz']:.3f}-{jump['frequency_right_ghz']:.3f} GHz: "
            f"mag_jump={jump['magnitude_jump']:.6f}, "
            f"phase_jump_deg={jump['phase_jump_deg']:.3f}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
