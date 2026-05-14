"""Run the corrected micro-loop pipeline for one pilot sample.

中文：对一个 Pilot 样本运行 corrected 标签小闭环。
English: Run the corrected-label micro-loop for one pilot sample.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


TASK_ROOT = Path(r"E:\aris\meta\cst_coupling_model1")
PYTHON = Path(r"D:\software\anaconda\envs\cst\python.exe")


def run(args: list[str]) -> None:
    print("\n> " + " ".join(args), flush=True)
    subprocess.run(args, cwd=TASK_ROOT, check=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sample_id")
    parser.add_argument("--skip-solve", action="store_true")
    parser.add_argument("--new-cst-session", action="store_true")
    args = parser.parse_args()

    sample_id = args.sample_id
    same_id = f"{sample_id}_same_center"
    nonperiodic_project = TASK_ROOT / "cst_projects" / "nonperiodic" / sample_id / "model1.cst"
    same_project_dir = TASK_ROOT / "cst_projects" / "nonperiodic" / same_id
    same_project = same_project_dir / "model1.cst"
    nonperiodic_csv = TASK_ROOT / "data" / "raw" / "nonperiodic" / f"{sample_id}_five_cell_szmax2_zmin1.csv"
    same_csv = TASK_ROOT / "data" / "raw" / "nonperiodic" / f"{same_id}_szmax2_zmin1.csv"
    corrected_csv = TASK_ROOT / "data" / "processed" / f"{sample_id}_corrected_label.csv"
    corrected_json = TASK_ROOT / "data" / "processed" / f"{sample_id}_corrected_label.json"
    corrected_svg = TASK_ROOT / "reports" / "figures" / f"{sample_id}_corrected_same_center_vs_nonperiodic.svg"
    corrected_summary = TASK_ROOT / "reports" / f"{sample_id}_corrected_curve_summary.csv"

    run(
        [
            str(PYTHON),
            str(TASK_ROOT / "scripts" / "build_nonperiodic_five_cell.py"),
            "--project",
            str(nonperiodic_project),
            *(["--new-cst-session"] if args.new_cst_session else []),
        ]
    )
    run(
        [
            str(PYTHON),
            str(TASK_ROOT / "scripts" / "prepare_same_parameter_control.py"),
            "--source-sample-id",
            sample_id,
            "--sample-id",
            same_id,
            "--project-dir",
            str(same_project_dir),
            "--overwrite",
        ]
    )
    run(
        [
            str(PYTHON),
            str(TASK_ROOT / "scripts" / "build_nonperiodic_five_cell.py"),
            "--project",
            str(same_project),
            *(["--new-cst-session"] if args.new_cst_session else []),
        ]
    )

    if not args.skip_solve:
        for project in [nonperiodic_project, same_project]:
            run(
                [
                    str(PYTHON),
                    str(TASK_ROOT / "scripts" / "configure_and_run_five_cell_supercell.py"),
                    "--project",
                    str(project),
                    *(["--new-cst-session"] if args.new_cst_session else []),
                ]
            )

    run(
        [
            str(PYTHON),
            str(TASK_ROOT / "scripts" / "export_cst_1d_result.py"),
            "--project",
            str(nonperiodic_project),
            "--output",
            str(nonperiodic_csv),
            "--tree-path",
            r"1D Results\S-Parameters\SZmax(2),Zmin(1)",
        ]
    )
    run(
        [
            str(PYTHON),
            str(TASK_ROOT / "scripts" / "export_cst_1d_result.py"),
            "--project",
            str(same_project),
            "--output",
            str(same_csv),
            "--tree-path",
            r"1D Results\S-Parameters\SZmax(2),Zmin(1)",
        ]
    )
    run(
        [
            str(PYTHON),
            str(TASK_ROOT / "scripts" / "build_coupling_label.py"),
            "--baseline",
            str(same_csv),
            "--comparison",
            str(nonperiodic_csv),
            "--output",
            str(corrected_csv),
            "--summary-json",
            str(corrected_json),
            "--sample-id",
            sample_id,
        ]
    )
    run(
        [
            str(PYTHON),
            str(TASK_ROOT / "scripts" / "plot_response_comparison.py"),
            "--periodic",
            str(same_csv),
            "--nonperiodic",
            str(nonperiodic_csv),
            "--output",
            str(corrected_svg),
            "--summary",
            str(corrected_summary),
            "--baseline-label",
            "same-center five-cell baseline",
            "--comparison-label",
            "nonperiodic five-cell",
            "--title",
            f"{sample_id} corrected coupling: same-center vs nonperiodic five-cell",
        ]
    )
    print(f"\ncompleted_sample: {sample_id}")
    print(f"corrected_label: {corrected_json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
