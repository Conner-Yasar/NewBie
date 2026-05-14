"""Plot periodic vs nonperiodic CST response curves.

中文：绘制周期/非周期 `SZmax(2),Zmin(1)` 幅值曲线对比。
English: Plot periodic/nonperiodic `SZmax(2),Zmin(1)` magnitude comparison.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


DEFAULT_PERIODIC = Path(
    r"E:\aris\meta\cst_coupling_model1\data\raw\periodic\pilot_0070_periodic_szmax2_zmin1.csv"
)
DEFAULT_NONPERIODIC = Path(
    r"E:\aris\meta\cst_coupling_model1\data\raw\nonperiodic\pilot_0070_five_cell_szmax2_zmin1.csv"
)
DEFAULT_OUTPUT = Path(
    r"E:\aris\meta\cst_coupling_model1\reports\figures\pilot_0070_periodic_vs_five_cell.svg"
)
DEFAULT_SUMMARY = Path(
    r"E:\aris\meta\cst_coupling_model1\reports\pilot_0070_curve_summary.csv"
)


def read_curve(path: Path) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    with path.open("r", newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(
                {
                    "frequency_ghz": float(row["frequency_ghz"]),
                    "magnitude": float(row["magnitude"]),
                }
            )
    if not rows:
        raise ValueError(f"No curve rows found: {path}")
    return rows


def align_curves(
    periodic: list[dict[str, float]], nonperiodic: list[dict[str, float]]
) -> list[tuple[float, float, float, float]]:
    p_by_freq = {round(row["frequency_ghz"], 9): row["magnitude"] for row in periodic}
    n_by_freq = {round(row["frequency_ghz"], 9): row["magnitude"] for row in nonperiodic}
    freqs = sorted(set(p_by_freq) & set(n_by_freq))
    return [(freq, p_by_freq[freq], n_by_freq[freq], abs(n_by_freq[freq] - p_by_freq[freq])) for freq in freqs]


def write_summary(path: Path, aligned: list[tuple[float, float, float, float]]) -> None:
    diffs = [row[3] for row in aligned]
    periodic = [row[1] for row in aligned]
    nonperiodic = [row[2] for row in aligned]
    max_row = max(aligned, key=lambda row: row[3])
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["metric", "value"])
        writer.writerow(["frequency_points", len(aligned)])
        writer.writerow(["frequency_min_ghz", aligned[0][0]])
        writer.writerow(["frequency_max_ghz", aligned[-1][0]])
        writer.writerow(["periodic_mean_magnitude", sum(periodic) / len(periodic)])
        writer.writerow(["nonperiodic_mean_magnitude", sum(nonperiodic) / len(nonperiodic)])
        writer.writerow(["mean_abs_difference", sum(diffs) / len(diffs)])
        writer.writerow(["max_abs_difference", max_row[3]])
        writer.writerow(["max_abs_difference_freq_ghz", max_row[0]])


def _polyline(points: list[tuple[float, float]], color: str, width: float = 1.5) -> str:
    coord_text = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
    return (
        f'<polyline fill="none" stroke="{color}" stroke-width="{width}" '
        f'stroke-linejoin="round" stroke-linecap="round" points="{coord_text}" />'
    )


def _scale_points(
    freqs: list[float],
    values: list[float],
    x0: float,
    y0: float,
    width: float,
    height: float,
    y_max: float,
) -> list[tuple[float, float]]:
    f_min = min(freqs)
    f_max = max(freqs)
    return [
        (
            x0 + (freq - f_min) / (f_max - f_min) * width,
            y0 + height - (value / y_max) * height,
        )
        for freq, value in zip(freqs, values)
    ]


def plot(
    aligned: list[tuple[float, float, float, float]],
    output: Path,
    baseline_label: str,
    comparison_label: str,
    title: str,
) -> None:
    freqs = [row[0] for row in aligned]
    periodic = [row[1] for row in aligned]
    nonperiodic = [row[2] for row in aligned]
    diffs = [row[3] for row in aligned]
    y_max_top = max(max(periodic), max(nonperiodic)) * 1.05
    y_max_bottom = max(diffs) * 1.05
    width = 1000
    height = 650
    left = 80
    plot_width = 860
    top_y = 70
    plot_height = 220
    bottom_y = 380
    output.parent.mkdir(parents=True, exist_ok=True)
    top_periodic = _scale_points(freqs, periodic, left, top_y, plot_width, plot_height, y_max_top)
    top_nonperiodic = _scale_points(freqs, nonperiodic, left, top_y, plot_width, plot_height, y_max_top)
    bottom_diff = _scale_points(freqs, diffs, left, bottom_y, plot_width, plot_height, y_max_bottom)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="100%" height="100%" fill="white"/>
  <text x="{left}" y="30" font-family="Arial" font-size="20">{title}</text>
  <line x1="{left}" y1="{top_y + plot_height}" x2="{left + plot_width}" y2="{top_y + plot_height}" stroke="#444"/>
  <line x1="{left}" y1="{top_y}" x2="{left}" y2="{top_y + plot_height}" stroke="#444"/>
  <line x1="{left}" y1="{bottom_y + plot_height}" x2="{left + plot_width}" y2="{bottom_y + plot_height}" stroke="#444"/>
  <line x1="{left}" y1="{bottom_y}" x2="{left}" y2="{bottom_y + plot_height}" stroke="#444"/>
  {_polyline(top_periodic, "#1f5a9d", 1.6)}
  {_polyline(top_nonperiodic, "#b66a00", 1.6)}
  {_polyline(bottom_diff, "#8a1f1f", 1.4)}
  <text x="{left + 10}" y="{top_y + 20}" font-family="Arial" font-size="13" fill="#1f5a9d">{baseline_label}</text>
  <text x="{left + 230}" y="{top_y + 20}" font-family="Arial" font-size="13" fill="#b66a00">{comparison_label}</text>
  <text x="{left + 10}" y="{bottom_y + 20}" font-family="Arial" font-size="13" fill="#8a1f1f">absolute difference</text>
  <text x="15" y="{top_y + 120}" font-family="Arial" font-size="13" transform="rotate(-90 15,{top_y + 120})">|S| magnitude</text>
  <text x="15" y="{bottom_y + 120}" font-family="Arial" font-size="13" transform="rotate(-90 15,{bottom_y + 120})">abs difference</text>
  <text x="{left}" y="{top_y + plot_height + 25}" font-family="Arial" font-size="12">{min(freqs):.1f} GHz</text>
  <text x="{left + plot_width - 55}" y="{top_y + plot_height + 25}" font-family="Arial" font-size="12">{max(freqs):.1f} GHz</text>
  <text x="{left}" y="{bottom_y + plot_height + 35}" font-family="Arial" font-size="12">{min(freqs):.1f} GHz</text>
  <text x="{left + plot_width - 55}" y="{bottom_y + plot_height + 35}" font-family="Arial" font-size="12">{max(freqs):.1f} GHz</text>
  <text x="{left + 380}" y="{bottom_y + plot_height + 35}" font-family="Arial" font-size="13">Frequency (GHz)</text>
  <text x="{left + plot_width + 8}" y="{top_y + 5}" font-family="Arial" font-size="11">{y_max_top:.3g}</text>
  <text x="{left + plot_width + 8}" y="{bottom_y + 5}" font-family="Arial" font-size="11">{y_max_bottom:.3g}</text>
</svg>
'''
    output.write_text(svg, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--periodic", default=DEFAULT_PERIODIC, type=Path)
    parser.add_argument("--nonperiodic", default=DEFAULT_NONPERIODIC, type=Path)
    parser.add_argument("--output", default=DEFAULT_OUTPUT, type=Path)
    parser.add_argument("--summary", default=DEFAULT_SUMMARY, type=Path)
    parser.add_argument("--baseline-label", default="baseline")
    parser.add_argument("--comparison-label", default="comparison")
    parser.add_argument("--title", default="pilot_0070 SZmax(2),Zmin(1): baseline vs comparison")
    args = parser.parse_args()

    aligned = align_curves(read_curve(args.periodic), read_curve(args.nonperiodic))
    if not aligned:
        raise ValueError("No common frequency points")
    plot(aligned, args.output, args.baseline_label, args.comparison_label, args.title)
    write_summary(args.summary, aligned)
    print(f"points: {len(aligned)}")
    print(f"frequency_min_ghz: {aligned[0][0]}")
    print(f"frequency_max_ghz: {aligned[-1][0]}")
    print(f"output: {args.output.resolve()}")
    print(f"summary: {args.summary.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
