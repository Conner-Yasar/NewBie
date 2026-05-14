"""Build a five-cell nonperiodic geometry in a CST project copy.

中文：在 nonperiodic CST 工程副本中重建 `[L2, L1, C, R1, R2]` 五单元几何。
English: Rebuild `[L2, L1, C, R1, R2]` five-cell geometry inside a nonperiodic CST copy.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
from pathlib import Path
from typing import Any


DEFAULT_CST_LIB = Path(r"D:\software\CST Studio Suite\AMD64\python_cst_libraries")
DEFAULT_CST_BIN = Path(r"D:\software\CST Studio Suite\AMD64")
DEFAULT_PROJECT = Path(
    r"E:\aris\meta\cst_coupling_model1\cst_projects\nonperiodic\pilot_0070\model1.cst"
)
CELL_ORDER = ["L2", "L1", "C", "R1", "R2"]
CELL_X_INDEX = {"L2": -2, "L1": -1, "C": 0, "R1": 1, "R2": 2}


def ensure_cst_python_path() -> None:
    cst_lib = str(DEFAULT_CST_LIB)
    cst_bin = str(DEFAULT_CST_BIN)
    if cst_lib not in sys.path:
        sys.path.insert(0, cst_lib)
    os.environ["PATH"] = cst_bin + os.pathsep + cst_lib + os.pathsep + os.environ.get("PATH", "")


def q(value: str | float | int) -> str:
    return f'"{value}"'


def fmt(value: float) -> str:
    text = f"{value:.9f}".rstrip("0").rstrip(".")
    return text if text else "0"


def brick(name: str, component: str, material: str, xr: tuple[float, float], yr: tuple[float, float], zr: tuple[float, float]) -> str:
    return "\n".join(
        [
            "With Brick",
            "    .Reset",
            f"    .Name {q(name)}",
            f"    .Component {q(component)}",
            f"    .Material {q(material)}",
            f"    .Xrange {q(fmt(xr[0]))}, {q(fmt(xr[1]))}",
            f"    .Yrange {q(fmt(yr[0]))}, {q(fmt(yr[1]))}",
            f"    .Zrange {q(fmt(zr[0]))}, {q(fmt(zr[1]))}",
            "    .Create",
            "End With",
        ]
    )


def transform_translate(shape: str, dx: float, dy: float, dz: float, multiple: bool = False) -> str:
    return "\n".join(
        [
            "With Transform",
            "    .Reset",
            f"    .Name {q(shape)}",
            f"    .Vector {q(fmt(dx))}, {q(fmt(dy))}, {q(fmt(dz))}",
            '    .UsePickedPoints "False"',
            '    .InvertPickedPoints "False"',
            f"    .MultipleObjects {q(str(multiple))}",
            '    .GroupObjects "False"',
            '    .Repetitions "1"',
            '    .MultipleSelection "False"',
            '    .Destination ""',
            '    .Material ""',
            '    .AutoDestination "True"',
            '    .Transform "Shape", "Translate"',
            "End With",
        ]
    )


def transform_rotate_shape(shape: str, cx: float, cy: float, angle_deg: float, multiple: bool = False) -> str:
    return "\n".join(
        [
            "With Transform",
            "    .Reset",
            f"    .Name {q(shape)}",
            '    .Origin "Free"',
            f"    .Center {q(fmt(cx))}, {q(fmt(cy))}, {q('0')}",
            f"    .Angle {q('0')}, {q('0')}, {q(fmt(angle_deg))}",
            f"    .MultipleObjects {q(str(multiple))}",
            '    .GroupObjects "False"',
            '    .Repetitions "1"',
            '    .MultipleSelection "False"',
            '    .Destination ""',
            '    .Material ""',
            '    .AutoDestination "True"',
            '    .Transform "Shape", "Rotate"',
            "End With",
        ]
    )


def transform_rotate_curve(curve_item: str, cx: float, cy: float, angle_deg: float) -> str:
    return "\n".join(
        [
            "With Transform",
            "    .Reset",
            f"    .Name {q(curve_item)}",
            '    .Origin "Free"',
            f"    .Center {q(fmt(cx))}, {q(fmt(cy))}, {q('0')}",
            f"    .Angle {q('0')}, {q('0')}, {q(fmt(angle_deg))}",
            '    .MultipleObjects "True"',
            '    .GroupObjects "False"',
            '    .Repetitions "1"',
            '    .MultipleSelection "False"',
            '    .Destination ""',
            '    .Transform "Curve", "Rotate"',
            "End With",
        ]
    )


def cylinder(name: str, component: str, x0: float, ry: float, ryin: float, zrange: tuple[float, float]) -> str:
    return "\n".join(
        [
            "With Cylinder",
            "    .Reset",
            f"    .Name {q(name)}",
            f"    .Component {q(component)}",
            '    .Material "Copper (annealed)"',
            f"    .OuterRadius {q(fmt(ry))}",
            f"    .InnerRadius {q(fmt(ryin))}",
            '    .Axis "z"',
            f"    .Zrange {q(fmt(zrange[0]))}, {q(fmt(zrange[1]))}",
            f"    .Xcenter {q(fmt(x0))}",
            f"    .Ycenter {q('0')}",
            '    .Segments "0"',
            "    .Create",
            "End With",
        ]
    )


def cell_macro(cell: str, atheta: float, pphi: float) -> str:
    pp = 6.0
    wg = 1.0
    dg = 1.0
    lc = 5.3
    wc = 1.2
    tm = 0.036
    t1 = 2.0
    t2 = 2.0
    ta = 0.1
    ry = 2.8
    ryin = 2.4
    x0 = CELL_X_INDEX[cell] * pp
    component = f"np_{cell}"
    curve = f"curve_{cell}"
    gap = 180.0 - pphi
    angle_rad = (-atheta - gap / 2.0) * math.pi / 180.0
    gapx = x0 + ry * math.sin(angle_rad)
    gapy = ry * math.cos(angle_rad)
    blocks: list[str] = [
        f"' ---- {cell}: Atheta={fmt(atheta)}, Pphi={fmt(pphi)}, x0={fmt(x0)} ----",
        f'Component.New "{component}"',
        brick("substrate1", component, "F4B", (x0 - pp / 2, x0 + pp / 2), (-pp / 2, pp / 2), (-tm - t1, -tm)),
        brick("grating-x", component, "Copper (annealed)", (x0 - pp / 2, x0 + pp / 2), (-wg / 2, wg / 2), (-tm - t1 - tm, -tm - t1)),
        transform_translate(f"{component}:grating-x", 0, wg + dg, 0, multiple=True),
        transform_translate(f"{component}:grating-x", 0, -wg - dg, 0, multiple=True),
        f'Solid.Add "{component}:grating-x", "{component}:grating-x_1"',
        f'Solid.Add "{component}:grating-x", "{component}:grating-x_2"',
        brick("center-rod", component, "Copper (annealed)", (x0 - lc / 2, x0 + lc / 2), (-wc / 2, wc / 2), (-tm, 0)),
        transform_rotate_shape(f"{component}:center-rod", x0, 0, atheta),
        cylinder("yanshenbi", component, x0, ry, ryin, (-tm, 0)),
        "\n".join(
            [
                "With Arc",
                "    .Reset",
                '    .Name "arc1"',
                f"    .Curve {q(curve)}",
                '    .Orientation "Clockwise"',
                f"    .XCenter {q(fmt(x0))}",
                f"    .YCenter {q('0')}",
                f"    .X1 {q(fmt(gapx))}",
                f"    .Y1 {q(fmt(gapy))}",
                f"    .X2 {q(fmt(x0))}",
                f"    .Y2 {q('0')}",
                f"    .Angle {q(fmt(gap))}",
                '    .UseAngle "True"',
                '    .Segments "0"',
                "    .Create",
                "End With",
            ]
        ),
        "\n".join(
            [
                "With Line",
                "    .Reset",
                '    .Name "line1"',
                f"    .Curve {q(curve)}",
                f"    .X1 {q(fmt(gapx))}",
                f"    .Y1 {q(fmt(gapy))}",
                f"    .X2 {q(fmt(x0))}",
                f"    .Y2 {q('0')}",
                "    .Create",
                "End With",
            ]
        ),
        transform_rotate_curve(f"{curve}:line1", x0, 0, -gap),
        "\n".join(
            [
                "With ExtrudeCurve",
                "    .Reset",
                '    .Name "solid1"',
                f"    .Component {q(component)}",
                '    .Material "Copper (annealed)"',
                f"    .Thickness {q(fmt(tm))}",
                '    .Twistangle "0.0"',
                '    .Taperangle "0.0"',
                '    .DeleteProfile "True"',
                f"    .Curve {q(curve)}",
                "    .Create",
                "End With",
            ]
        ),
        transform_rotate_shape(f"{component}:solid1", x0, 0, 180, multiple=True),
        f'Solid.Subtract "{component}:yanshenbi", "{component}:solid1"',
        f'Solid.Subtract "{component}:yanshenbi", "{component}:solid1_1"',
        f'Solid.Add "{component}:center-rod", "{component}:yanshenbi"',
        brick("air-layer", component, "Air", (x0 - pp / 2, x0 + pp / 2), (-pp / 2, pp / 2), (-tm, -tm + ta)),
        f'Solid.Insert "{component}:air-layer", "{component}:center-rod"',
        brick("substrate2", component, "F4B", (x0 - pp / 2, x0 + pp / 2), (-pp / 2, pp / 2), (-tm + ta, -tm + ta + t2)),
        brick("grating-y", component, "Copper (annealed)", (x0 - wg / 2, x0 + wg / 2), (-pp / 2, pp / 2), (-tm + ta + t2, -tm + ta + t2 + tm)),
        transform_translate(f"{component}:grating-y", wg + dg, 0, 0, multiple=True),
        transform_translate(f"{component}:grating-y", -wg - dg, 0, 0, multiple=True),
        f'Solid.Add "{component}:grating-y", "{component}:grating-y_1"',
        f'Solid.Add "{component}:grating-y", "{component}:grating-y_2"',
    ]
    return "\n\n".join(blocks)


def build_macro(parameters: dict[str, Any]) -> str:
    cells = parameters["five_cell_parameters"]
    blocks = [
        "' Auto-generated by build_nonperiodic_five_cell.py",
        "' Rebuild nonperiodic five-cell geometry for pilot_0070.",
        'On Error Resume Next',
        'Component.Delete "component1"',
    ]
    for cell in CELL_ORDER:
        blocks.append(f'Component.Delete "np_{cell}"')
    blocks.append("On Error GoTo 0")
    blocks.append('Solver.FrequencyRange "6", "24"')
    # Keep the current Unit Cell/Floquet setup for the first geometry build.
    # Boundary conversion for a finite-array solve is handled as a separate validated step.
    for cell in CELL_ORDER:
        blocks.append(cell_macro(cell, float(cells[cell]["Atheta"]), float(cells[cell]["Pphi"])))
    return "\n\n".join(blocks)


def metadata_path_for_project(project: Path) -> Path:
    return project.parent / "micro_loop_metadata.json"


def update_metadata(project: Path, macro_path: Path) -> None:
    metadata_path = metadata_path_for_project(project)
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    metadata["cst_model_status"] = {
        "zh": "已通过自动化 history 重建为五单元非周期几何；边界/端口仍沿用模板，有限阵列求解边界待单独验证。",
        "en": "The project has been rebuilt as a five-cell nonperiodic geometry through automated history; boundaries/ports still follow the template and finite-array solver boundaries remain to be validated separately.",
    }
    metadata["five_cell_geometry"] = {
        "component_names": [f"np_{cell}" for cell in CELL_ORDER],
        "x_offsets_mm": {cell: CELL_X_INDEX[cell] * 6.0 for cell in CELL_ORDER},
        "macro_path": str(macro_path.resolve()),
    }
    metadata_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")


def apply_macro(project: Path, macro: str, new_cst_session: bool) -> None:
    ensure_cst_python_path()
    import cst.interface as interface  # type: ignore

    if new_cst_session:
        design_environment = interface.DesignEnvironment.new(options=["--hide"])
    else:
        design_environment = interface.DesignEnvironment.connect_to_any_or_new()
    cst_project = design_environment.open_project(str(project.resolve()))
    cst_project.model3d.add_to_history("build nonperiodic five-cell geometry", macro)
    cst_project.model3d.Rebuild()
    cst_project.save()
    cst_project.close()
    design_environment.close()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", default=DEFAULT_PROJECT, type=Path)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--new-cst-session", action="store_true")
    args = parser.parse_args()

    metadata = json.loads(metadata_path_for_project(args.project).read_text(encoding="utf-8"))
    macro = build_macro(metadata)
    macro_path = args.project.parent / "build_nonperiodic_five_cell.bas"
    macro_path.write_text(macro, encoding="utf-8")
    if not args.dry_run:
        apply_macro(args.project, macro, args.new_cst_session)
        update_metadata(args.project, macro_path)
    print(f"project: {args.project.resolve()}")
    print(f"macro: {macro_path.resolve()}")
    print(f"dry_run: {args.dry_run}")
    print("components: " + ", ".join(f"np_{cell}" for cell in CELL_ORDER))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
