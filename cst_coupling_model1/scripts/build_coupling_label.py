"""Build a 6-24 GHz coupling label from paired CST response CSV files.

中文：从周期/非周期两条 `SZmax(2),Zmin(1)` CSV 曲线计算耦合标签。
English: Compute a coupling label from paired periodic/nonperiodic curves.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from dataclasses import dataclass
from pathlib import Path


DEFAULT_RESPONSE_CHANNEL = "SZmax(2),Zmin(1)"
DEFAULT_BAND_MIN_GHZ = 6.0
DEFAULT_BAND_MAX_GHZ = 24.0
DEFAULT_LABEL_COLUMN = "coupling_label_6_24ghz"


@dataclass(frozen=True)
class CurvePoint:
    frequency_ghz: float
    real: float | None
    imag: float | None
    magnitude: float


def _required_float(row: dict[str, str], column: str, source: Path) -> float:
    value = row.get(column)
    if value is None or value == "":
        raise ValueError(f"Missing required column '{column}' in {source}")
    return float(value)


def _optional_float(row: dict[str, str], column: str) -> float | None:
    value = row.get(column)
    if value is None or value == "":
        return None
    return float(value)


def read_curve(path: Path) -> list[CurvePoint]:
    points: list[CurvePoint] = []
    with path.open("r", newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise ValueError(f"CSV has no header: {path}")
        for row in reader:
            freq = _required_float(row, "frequency_ghz", path)
            real = _optional_float(row, "real")
            imag = _optional_float(row, "imag")
            magnitude = _optional_float(row, "magnitude")
            if magnitude is None:
                if real is None or imag is None:
                    raise ValueError(
                        f"CSV must contain either magnitude or real+imag columns: {path}"
                    )
                magnitude = math.hypot(real, imag)
            points.append(CurvePoint(freq, real, imag, magnitude))

    if not points:
        raise ValueError(f"CSV contains no data rows: {path}")
    return points


def filter_band(
    points: list[CurvePoint], band_min_ghz: float, band_max_ghz: float
) -> list[CurvePoint]:
    return [
        point
        for point in points
        if band_min_ghz <= point.frequency_ghz <= band_max_ghz
    ]


def align_by_frequency(
    baseline: list[CurvePoint], comparison: list[CurvePoint]
) -> list[tuple[CurvePoint, CurvePoint]]:
    baseline_by_freq = {round(point.frequency_ghz, 9): point for point in baseline}
    comparison_by_freq = {round(point.frequency_ghz, 9): point for point in comparison}
    common_freqs = sorted(set(baseline_by_freq) & set(comparison_by_freq))
    if not common_freqs:
        raise ValueError(
            "No common frequency points after band filtering. "
            "Export both curves on the same frequency grid or add interpolation later."
        )
    return [(baseline_by_freq[freq], comparison_by_freq[freq]) for freq in common_freqs]


def point_difference(
    baseline: CurvePoint, comparison: CurvePoint, difference_mode: str
) -> float:
    if difference_mode == "magnitude_abs_diff":
        return abs(comparison.magnitude - baseline.magnitude)
    if difference_mode == "complex_abs_diff":
        if (
            baseline.real is None
            or baseline.imag is None
            or comparison.real is None
            or comparison.imag is None
        ):
            raise ValueError("complex_abs_diff requires real and imag columns")
        return math.hypot(comparison.real - baseline.real, comparison.imag - baseline.imag)
    raise ValueError(f"Unsupported difference mode: {difference_mode}")


def build_label(
    baseline_csv: Path,
    comparison_csv: Path,
    sample_id: str,
    band_min_ghz: float,
    band_max_ghz: float,
    difference_mode: str,
    response_channel: str,
) -> dict[str, object]:
    baseline_all = read_curve(baseline_csv)
    comparison_all = read_curve(comparison_csv)
    baseline_band = filter_band(baseline_all, band_min_ghz, band_max_ghz)
    comparison_band = filter_band(comparison_all, band_min_ghz, band_max_ghz)
    aligned = align_by_frequency(baseline_band, comparison_band)
    diffs = [point_difference(p, n, difference_mode) for p, n in aligned]
    baseline_mags = [p.magnitude for p, _ in aligned]
    comparison_mags = [n.magnitude for _, n in aligned]
    freqs = [p.frequency_ghz for p, _ in aligned]

    return {
        "sample_id": sample_id,
        "baseline_csv": str(baseline_csv.resolve()),
        "comparison_csv": str(comparison_csv.resolve()),
        "periodic_csv": str(baseline_csv.resolve()),
        "nonperiodic_csv": str(comparison_csv.resolve()),
        "response_channel": response_channel,
        "difference_mode": difference_mode,
        "label_band_min_ghz": band_min_ghz,
        "label_band_max_ghz": band_max_ghz,
        "frequency_points": len(aligned),
        "frequency_min_ghz": min(freqs),
        "frequency_max_ghz": max(freqs),
        DEFAULT_LABEL_COLUMN: sum(diffs) / len(diffs),
        "max_abs_difference": max(diffs),
        "baseline_mean_magnitude": sum(baseline_mags) / len(baseline_mags),
        "comparison_mean_magnitude": sum(comparison_mags) / len(comparison_mags),
        "periodic_mean_magnitude": sum(baseline_mags) / len(baseline_mags),
        "nonperiodic_mean_magnitude": sum(comparison_mags) / len(comparison_mags),
    }


def write_csv_row(path: Path, row: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(row.keys()))
        writer.writeheader()
        writer.writerow(row)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", type=Path)
    parser.add_argument("--comparison", type=Path)
    parser.add_argument("--periodic", type=Path)
    parser.add_argument("--nonperiodic", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--sample-id", default="sample_000000")
    parser.add_argument("--band-min-ghz", default=DEFAULT_BAND_MIN_GHZ, type=float)
    parser.add_argument("--band-max-ghz", default=DEFAULT_BAND_MAX_GHZ, type=float)
    parser.add_argument(
        "--difference-mode",
        choices=["magnitude_abs_diff", "complex_abs_diff"],
        default="magnitude_abs_diff",
    )
    parser.add_argument("--response-channel", default=DEFAULT_RESPONSE_CHANNEL)
    parser.add_argument("--summary-json", type=Path)
    args = parser.parse_args()
    baseline = args.baseline or args.periodic
    comparison = args.comparison or args.nonperiodic
    if baseline is None or comparison is None:
        parser.error("Provide --baseline/--comparison or legacy --periodic/--nonperiodic")

    row = build_label(
        baseline_csv=baseline,
        comparison_csv=comparison,
        sample_id=args.sample_id,
        band_min_ghz=args.band_min_ghz,
        band_max_ghz=args.band_max_ghz,
        difference_mode=args.difference_mode,
        response_channel=args.response_channel,
    )
    write_csv_row(args.output, row)
    if args.summary_json:
        args.summary_json.parent.mkdir(parents=True, exist_ok=True)
        args.summary_json.write_text(
            json.dumps(row, indent=2, ensure_ascii=False), encoding="utf-8"
        )
    for key, value in row.items():
        print(f"{key}: {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
