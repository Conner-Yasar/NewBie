"""Configure and optionally solve a narrow-band CST verification copy.

The script keeps the original full-band workflow untouched.  It applies the
same five-cell supercell boundary/excitation setup, but replaces the frequency
range and sweep sampling with a narrow verification band.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path


DEFAULT_CST_LIB = Path(r"D:\software\CST Studio Suite\AMD64\python_cst_libraries")
DEFAULT_CST_BIN = Path(r"D:\software\CST Studio Suite\AMD64")


def ensure_cst_python_path() -> None:
    cst_lib = str(DEFAULT_CST_LIB)
    cst_bin = str(DEFAULT_CST_BIN)
    if cst_lib not in sys.path:
        sys.path.insert(0, cst_lib)
    os.environ["PATH"] = cst_bin + os.pathsep + cst_lib + os.pathsep + os.environ.get("PATH", "")


def fixed_sample_lines(fmin: float, fmax: float, points: int) -> list[str]:
    if points < 2:
        raise ValueError("points must be at least 2")
    step = (fmax - fmin) / (points - 1)
    lines = []
    for index in range(points):
        freq = fmin + step * index
        lines.append(
            f'     .AddSampleInterval "{freq:.12g}", "{freq:.12g}", "1", "Single", '
            f'"{"True" if index == 0 else "False"}"'
        )
    return lines


def narrowband_macro(
    *,
    fmin: float,
    fmax: float,
    points: int,
    accuracy_tet: str,
    accuracy_rom: str,
    fixed_single: bool,
) -> str:
    if fixed_single:
        sample_lines = fixed_sample_lines(fmin, fmax, points)
        sampling_mode = "Automatic"
        sweep_minimum = str(points)
    else:
        sample_lines = [
            '     .AddSampleInterval "", "", "1", "Automatic", "True"',
            '     .AddSampleInterval "", "", "", "Automatic", "False"',
        ]
        sampling_mode = "Automatic"
        sweep_minimum = "3"

    sample_block = "\n".join(sample_lines)
    return f'''
' Narrow-band spike verification.
' Chinese: narrow frequency-band rerun for checking spike reproducibility.
' English: narrow frequency-band rerun for checking spike reproducibility.

Solver.FrequencyRange "{fmin:.12g}", "{fmax:.12g}"

With FloquetPort
     .Reset
     .SetDialogTheta "0"
     .SetDialogPhi "0"
     .SetSortCode "+beta/pw"
     .SetCustomizedListFlag "False"
     .Port "Zmin"
     .SetNumberOfModesConsidered "2"
     .Port "Zmax"
     .SetNumberOfModesConsidered "2"
End With

MakeSureParameterExists "theta", "0"
SetParameterDescription "theta", "spherical angle of incident plane wave"
MakeSureParameterExists "phi", "0"
SetParameterDescription "phi", "spherical angle of incident plane wave"

With Boundary
     .Xmin "unit cell"
     .Xmax "unit cell"
     .Ymin "unit cell"
     .Ymax "unit cell"
     .Zmin "expanded open"
     .Zmax "expanded open"
     .Xsymmetry "none"
     .Ysymmetry "none"
     .Zsymmetry "none"
     .XPeriodicShift "0.0"
     .YPeriodicShift "0.0"
     .ZPeriodicShift "0.0"
     .PeriodicUseConstantAngles "False"
     .SetPeriodicBoundaryAngles "theta", "phi"
     .SetPeriodicBoundaryAnglesDirection "inward"
     .UnitCellFitToBoundingBox "True"
     .UnitCellDs1 "0.0"
     .UnitCellDs2 "0.0"
     .UnitCellAngle "90.0"
End With

With FDSolver
     .Reset
     .SetMethod "Tetrahedral", "General purpose"
     .OrderTet "Second"
     .OrderSrf "First"
     .Stimulation "List", "List"
     .ResetExcitationList
     .AddToExcitationList "Zmin", "TE(0,0);TM(0,0)"
     .AddToExcitationList "Zmax", "TE(0,0);TM(0,0)"
     .AutoNormImpedance "False"
     .NormingImpedance "50"
     .ModesOnly "False"
     .ConsiderPortLossesTet "True"
     .AccuracyTet "{accuracy_tet}"
     .StoreAllResults "False"
     .StoreResultsInCache "False"
     .UseHelmholtzEquation "True"
     .LowFrequencyStabilization "False"
     .Type "Auto"
     .MeshAdaptionTet "True"
     .AcceleratedRestart "True"
     .FreqDistAdaptMode "Distributed"
     .NewIterativeSolver "True"
     .SetNumberOfResultDataSamples "{points}"
     .SetResultDataSamplingMode "{sampling_mode}"
     .SweepMinimumSamples "{sweep_minimum}"
     .SweepWeightEvanescent "1.0"
     .AccuracyROM "{accuracy_rom}"
{sample_block}
     .UseParallelization "True"
     .MaximumNumberOfCPUDevices "2"
End With

FDSolver.SetAllowFloatDirectSolver "True"
FDSolver.SetKeepSolutionCoefficients "All"
'''.strip()


def update_metadata(
    project: Path,
    *,
    status: str,
    solve_started: bool,
    fmin: float,
    fmax: float,
    points: int,
    fixed_single: bool,
    accuracy_tet: str,
    accuracy_rom: str,
) -> None:
    metadata_path = project.parent / "micro_loop_metadata.json"
    metadata = {}
    if metadata_path.exists():
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    metadata["narrowband_verification"] = {
        "status": status,
        "solve_started": solve_started,
        "frequency_min_ghz": fmin,
        "frequency_max_ghz": fmax,
        "result_points": points,
        "fixed_single_sampling": fixed_single,
        "accuracy_tet": accuracy_tet,
        "accuracy_rom": accuracy_rom,
        "updated_at": datetime.now().isoformat(timespec="seconds"),
        "zh": "窄频段固定/高精度验证设置，用于判断尖跳是否由全带自动插值造成。",
        "en": "Narrow-band fixed/high-accuracy verification setup for checking whether spikes are caused by full-band automatic interpolation.",
    }
    metadata_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True, type=Path)
    parser.add_argument("--fmin", required=True, type=float)
    parser.add_argument("--fmax", required=True, type=float)
    parser.add_argument("--points", type=int, default=81)
    parser.add_argument("--accuracy-tet", default="5e-5")
    parser.add_argument("--accuracy-rom", default="5e-5")
    parser.add_argument("--fixed-single", action="store_true")
    parser.add_argument("--skip-solve", action="store_true")
    parser.add_argument("--new-cst-session", action="store_true")
    args = parser.parse_args()

    if args.fmin >= args.fmax:
        raise ValueError("--fmin must be smaller than --fmax")

    ensure_cst_python_path()
    import cst.interface as interface  # type: ignore

    project_path = args.project.resolve()
    macro = narrowband_macro(
        fmin=args.fmin,
        fmax=args.fmax,
        points=args.points,
        accuracy_tet=args.accuracy_tet,
        accuracy_rom=args.accuracy_rom,
        fixed_single=args.fixed_single,
    )
    (project_path.parent / "configure_narrowband_verification.bas").write_text(macro, encoding="utf-8")

    if args.new_cst_session:
        design_environment = interface.DesignEnvironment.new(options=["--hide"])
    else:
        design_environment = interface.DesignEnvironment.connect_to_any_or_new()
    project = design_environment.open_project(str(project_path))
    project.model3d.add_to_history("configure narrow-band spike verification", macro)
    project.model3d.Rebuild()
    project.save()

    solve_started = False
    if not args.skip_solve:
        project.model3d.DeleteResults()
        project.save()
        project.model3d.RunSolver()
        solve_started = True
        project.save()

    project.close()
    design_environment.close()
    update_metadata(
        project_path,
        status="solver_completed" if solve_started else "configured_only",
        solve_started=solve_started,
        fmin=args.fmin,
        fmax=args.fmax,
        points=args.points,
        fixed_single=args.fixed_single,
        accuracy_tet=args.accuracy_tet,
        accuracy_rom=args.accuracy_rom,
    )
    print(f"project: {project_path}")
    print(f"frequency_range_ghz: {args.fmin}-{args.fmax}")
    print(f"points: {args.points}")
    print(f"fixed_single: {args.fixed_single}")
    print(f"skip_solve: {args.skip_solve}")
    print(f"solve_started: {solve_started}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
