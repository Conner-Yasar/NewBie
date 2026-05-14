"""Generate a publication-style PDF for narrow-band spike verification."""

from __future__ import annotations

import argparse
import csv
import math
import subprocess
from pathlib import Path


TASK_ROOT = Path(r"E:\aris\meta\cst_coupling_model1")
PDFLATEX = Path(r"D:\software\MiKTeX\miktex\bin\x64\pdflatex.exe")
DEFAULT_OUTPUT = TASK_ROOT / "reports" / "figures" / "grid_05506_np_r04_narrowband_verification.pdf"
DEFAULT_WORKDIR = TASK_ROOT / "reports" / "figures" / "narrowband_plot_build"


BANDS = [
    (
        "7.8--8.4 GHz",
        TASK_ROOT / "data" / "raw" / "nonperiodic" / "grid_05506_np_r04_nb_7p8_8p4_szmax2_zmin1.csv",
    ),
    (
        "9.2--9.9 GHz",
        TASK_ROOT / "data" / "raw" / "nonperiodic" / "grid_05506_np_r04_nb_9p2_9p9_szmax2_zmin1.csv",
    ),
    (
        "20.3--22.4 GHz",
        TASK_ROOT / "data" / "raw" / "nonperiodic" / "grid_05506_np_r04_nb_20p3_22p4_szmax2_zmin1.csv",
    ),
]


def read_curve(path: Path) -> list[tuple[float, float]]:
    with path.open(newline="", encoding="utf-8-sig") as f:
        rows = []
        for row in csv.DictReader(f):
            freq = float(row["frequency_ghz"])
            if row.get("magnitude"):
                mag = float(row["magnitude"])
            else:
                mag = math.hypot(float(row["real"]), float(row["imag"]))
            rows.append((freq, mag))
        return rows


def interpolate(curve: list[tuple[float, float]], freq: float) -> float:
    if freq <= curve[0][0]:
        return curve[0][1]
    if freq >= curve[-1][0]:
        return curve[-1][1]
    for left, right in zip(curve, curve[1:]):
        if left[0] <= freq <= right[0]:
            span = right[0] - left[0]
            if span == 0:
                return left[1]
            ratio = (freq - left[0]) / span
            return left[1] + ratio * (right[1] - left[1])
    raise ValueError(f"frequency outside curve: {freq}")


def write_dat_files(
    workdir: Path,
    original: list[tuple[float, float]],
    repeat: list[tuple[float, float]],
) -> list[str]:
    workdir.mkdir(parents=True, exist_ok=True)
    names = []
    for index, (_, narrow_path) in enumerate(BANDS, 1):
        dat_name = f"grid_05506_np_r04_narrowband_{index}.dat"
        names.append(dat_name)
        with (workdir / dat_name).open("w", newline="\n", encoding="utf-8") as f:
            f.write("freq original repeat narrow\n")
            narrow = read_curve(narrow_path)
            for freq, narrow_mag in narrow:
                f.write(
                    f"{freq:.12g} {interpolate(original, freq):.12g} "
                    f"{interpolate(repeat, freq):.12g} {narrow_mag:.12g}\n"
                )


    return names


def write_tex(path: Path, dat_names: list[str]) -> None:
    band_titles = [band[0] for band in BANDS]
    panels = []
    for index, title in enumerate(band_titles):
        dat_name = dat_names[index]
        options = [
            rf"title={{\textbf{{{title}}}}}",
            r"title style={font=\small, yshift=-0.7ex}",
            r"ylabel={$|S|$}",
            "ymin=0",
        ]
        if index == len(band_titles) - 1:
            options.insert(3, "xlabel={Frequency (GHz)}")
        option_block = ",\n  ".join(options)
        panels.append(
            rf"""
\nextgroupplot[
  {option_block},
]
\addplot+[origblue, line width=0.7pt, mark=none]
  table[x=freq,y=original] {{{dat_name}}};
\addplot+[repeatgreen, line width=0.7pt, mark=none]
  table[x=freq,y=repeat] {{{dat_name}}};
\addplot+[narrowred, line width=0.95pt, mark=none]
  table[x=freq,y=narrow] {{{dat_name}}};
"""
        )
    path.write_text(
        rf"""\documentclass[tikz,border=3pt]{{standalone}}
\usepackage{{pgfplots}}
\pgfplotsset{{compat=1.18}}
\usepgfplotslibrary{{groupplots}}
\definecolor{{origblue}}{{RGB}}{{35,82,135}}
\definecolor{{repeatgreen}}{{RGB}}{{43,125,83}}
\definecolor{{narrowred}}{{RGB}}{{175,62,54}}
\begin{{document}}
\begin{{tikzpicture}}
\begin{{groupplot}}[
  group style={{group size=1 by 3, vertical sep=0.55cm}},
  width=13.2cm,
  height=4.25cm,
  grid=both,
  major grid style={{line width=0.25pt, draw=black!18}},
  minor grid style={{line width=0.15pt, draw=black!8}},
  tick align=outside,
  tick style={{black, line width=0.35pt}},
  axis line style={{black, line width=0.45pt}},
  label style={{font=\small}},
  tick label style={{font=\footnotesize}},
  legend style={{
    draw=none,
    fill=none,
    font=\footnotesize,
    at={{(0.02,0.98)}},
    anchor=north west,
    cells={{anchor=west}},
  }},
]
{''.join(panels)}
\end{{groupplot}}
\node[anchor=south west, font=\footnotesize] at (current bounding box.north west)
  {{\textbf{{grid\_05506\_np\_r04 narrow-band verification}}}};
\matrix[draw=none, fill=none, anchor=south east, font=\footnotesize] at (current bounding box.north east) {{
  \draw[origblue, line width=0.8pt] (0,0) -- (0.45,0); & \node{{original full band}}; &
  \draw[repeatgreen, line width=0.8pt] (0,0) -- (0.45,0); & \node{{repeat full band}}; &
  \draw[narrowred, line width=0.95pt] (0,0) -- (0.45,0); & \node{{narrow fixed samples}}; \\
}};
\end{{tikzpicture}}
\end{{document}}
""",
        encoding="utf-8",
    )


def compile_pdf(tex_path: Path, output: Path) -> None:
    subprocess.run(
        [str(PDFLATEX), "-interaction=nonstopmode", "-halt-on-error", tex_path.name],
        cwd=tex_path.parent,
        check=True,
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    tex_path.with_suffix(".pdf").replace(output)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--original",
        default=TASK_ROOT / "data" / "raw" / "nonperiodic" / "grid_05506_np_r04_five_cell_szmax2_zmin1.csv",
        type=Path,
    )
    parser.add_argument(
        "--repeat",
        default=TASK_ROOT / "data" / "raw" / "nonperiodic" / "grid_05506_np_r04_repeat01_five_cell_szmax2_zmin1.csv",
        type=Path,
    )
    parser.add_argument("--workdir", default=DEFAULT_WORKDIR, type=Path)
    parser.add_argument("--output", default=DEFAULT_OUTPUT, type=Path)
    args = parser.parse_args()

    args.workdir.mkdir(parents=True, exist_ok=True)
    tex_path = args.workdir / "grid_05506_np_r04_narrowband_verification.tex"
    dat_names = write_dat_files(args.workdir, read_curve(args.original), read_curve(args.repeat))
    write_tex(tex_path, dat_names)
    compile_pdf(tex_path, args.output)
    for dat_name in dat_names:
        print(f"dat: {(args.workdir / dat_name).resolve()}")
    print(f"tex: {tex_path.resolve()}")
    print(f"output: {args.output.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
