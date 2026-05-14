"""Export a CST 1D complex result curve to CSV.

导出 CST 1D 复数结果曲线为 CSV。
"""

from __future__ import annotations

import argparse
import csv
import math
import os
import sys
from pathlib import Path


DEFAULT_CST_LIB = Path(r"D:\software\CST Studio Suite\AMD64\python_cst_libraries")
DEFAULT_CST_BIN = Path(r"D:\software\CST Studio Suite\AMD64")
DEFAULT_TREE_PATH = r"1D Results\S-Parameters\SZmax(2),Zmin(1)"


def ensure_cst_python_path() -> None:
    cst_lib = str(DEFAULT_CST_LIB)
    cst_bin = str(DEFAULT_CST_BIN)
    if cst_lib not in sys.path:
        sys.path.insert(0, cst_lib)
    os.environ["PATH"] = cst_bin + os.pathsep + cst_lib + os.pathsep + os.environ.get("PATH", "")


def export_result(project: Path, tree_path: str, output: Path) -> dict[str, object]:
    ensure_cst_python_path()
    import cst.results as results  # type: ignore

    project = project.resolve()
    output = output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)

    result_project = results.ProjectFile(str(project), allow_interactive=True)
    result_3d = result_project.get_3d()
    item = result_3d.get_result_item(tree_path)
    data = item.get_data()

    with output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["frequency_ghz", "real", "imag", "magnitude"])
        for freq, value in data:
            writer.writerow([freq, value.real, value.imag, abs(value)])

    freqs = [row[0] for row in data]
    mags = [abs(row[1]) for row in data]
    return {
        "project": str(project),
        "tree_path": tree_path,
        "output": str(output),
        "points": len(data),
        "freq_min_ghz": min(freqs) if freqs else None,
        "freq_max_ghz": max(freqs) if freqs else None,
        "mag_min": min(mags) if mags else None,
        "mag_max": max(mags) if mags else None,
        "run_ids": result_3d.get_all_run_ids(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--tree-path", default=DEFAULT_TREE_PATH)
    args = parser.parse_args()

    summary = export_result(args.project, args.tree_path, args.output)
    for key, value in summary.items():
        print(f"{key}: {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
