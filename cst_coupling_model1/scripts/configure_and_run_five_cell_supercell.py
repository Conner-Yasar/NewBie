"""Configure and solve the pilot_0070 five-cell nonperiodic CST supercell.

中文：配置并运行 `pilot_0070` 五单元非周期超胞 Floquet 求解。
English: Configure and run the `pilot_0070` five-cell nonperiodic Floquet supercell solve.
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
DEFAULT_PROJECT = Path(
    r"E:\aris\meta\cst_coupling_model1\cst_projects\nonperiodic\pilot_0070\model1.cst"
)


def ensure_cst_python_path() -> None:
    cst_lib = str(DEFAULT_CST_LIB)
    cst_bin = str(DEFAULT_CST_BIN)
    if cst_lib not in sys.path:
        sys.path.insert(0, cst_lib)
    os.environ["PATH"] = cst_bin + os.pathsep + cst_lib + os.pathsep + os.environ.get("PATH", "")


def supercell_boundary_macro() -> str:
    return r'''
' Configure five-cell supercell boundary and excitation.
' 中文：x 方向用 5 单元超胞周期边界，y 方向保持单元周期，z 方向 Floquet/open。
' English: Use a five-cell supercell periodic boundary in x, unit periodicity in y, and Floquet/open ports in z.

Solver.FrequencyRange "6", "24"

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
     .AccuracyTet "1e-4"
     .StoreAllResults "False"
     .StoreResultsInCache "False"
     .UseHelmholtzEquation "True"
     .LowFrequencyStabilization "False"
     .Type "Auto"
     .MeshAdaptionTet "True"
     .AcceleratedRestart "True"
     .FreqDistAdaptMode "Distributed"
     .NewIterativeSolver "True"
     .SetNumberOfResultDataSamples "1001"
     .SetResultDataSamplingMode "Automatic"
     .SweepMinimumSamples "3"
     .SweepWeightEvanescent "1.0"
     .AccuracyROM "1e-4"
     .AddSampleInterval "", "", "1", "Automatic", "True"
     .AddSampleInterval "", "", "", "Automatic", "False"
     .UseParallelization "True"
     .MaximumNumberOfCPUDevices "2"
End With

FDSolver.SetAllowFloatDirectSolver "True"
FDSolver.SetKeepSolutionCoefficients "All"
'''.strip()


def update_metadata(project: Path, status: str, solve_started: bool) -> None:
    metadata_path = project.parent / "micro_loop_metadata.json"
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    metadata["finite_array_solver_status"] = {
        "status": status,
        "solve_started": solve_started,
        "updated_at": datetime.now().isoformat(timespec="seconds"),
        "zh": "使用 5 单元超胞 Floquet 设置：x/y 为 unit cell，z 为 expanded open，Zmin/Zmax 双向入射。",
        "en": "Uses a five-cell Floquet supercell setup: x/y are unit cell boundaries, z is expanded open, with both Zmin and Zmax incidence.",
    }
    metadata_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", default=DEFAULT_PROJECT, type=Path)
    parser.add_argument("--skip-solve", action="store_true")
    parser.add_argument("--new-cst-session", action="store_true")
    args = parser.parse_args()

    ensure_cst_python_path()
    import cst.interface as interface  # type: ignore

    project_path = args.project.resolve()
    if args.new_cst_session:
        design_environment = interface.DesignEnvironment.new(options=["--hide"])
    else:
        design_environment = interface.DesignEnvironment.connect_to_any_or_new()
    project = design_environment.open_project(str(project_path))
    project.model3d.add_to_history(
        "configure five-cell supercell boundary and excitation",
        supercell_boundary_macro(),
    )
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
    update_metadata(project_path, "solver_completed" if solve_started else "configured_only", solve_started)
    print(f"project: {project_path}")
    print(f"skip_solve: {args.skip_solve}")
    print(f"solve_started: {solve_started}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
