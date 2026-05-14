"""Generate a publication-style PDF response plot using LaTeX/PGFPlots.

Chinese: 用 LaTeX/PGFPlots 重新绘制论文风格曲线图。
English: Replot response curves as a publication-style PDF using LaTeX/PGFPlots.
"""

from __future__ import annotations

import argparse
import csv
import math
import subprocess
from pathlib import Path


TASK_ROOT = Path(r"E:\aris\meta\cst_coupling_model1")
DEFAULT_BASELINE = (
    TASK_ROOT
    / "data"
    / "raw"
    / "nonperiodic"
    / "grid_05506_np_r04_same_center_szmax2_zmin1.csv"
)
DEFAULT_COMPARISON = (
    TASK_ROOT
    / "data"
    / "raw"
    / "nonperiodic"
    / "grid_05506_np_r04_five_cell_szmax2_zmin1.csv"
)
DEFAULT_OUTPUT = (
    TASK_ROOT
    / "reports"
    / "figures"
    / "grid_05506_np_r04_corrected_same_center_vs_nonperiodic_paper.pdf"
)
DEFAULT_WORKDIR = TASK_ROOT / "reports" / "figures" / "paper_plot_build"
PDFLATEX = Path(r"D:\software\MiKTeX\miktex\bin\x64\pdflatex.exe")


def read_curve(path: Path) -> dict[float, float]:
    with path.open("r", newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        return {
            round(float(row["frequency_ghz"]), 9): float(row["magnitude"])
            for row in reader
        }


def aligned_rows(
    baseline_path: Path,
    comparison_path: Path,
) -> list[tuple[float, float, float, float]]:
    baseline = read_curve(baseline_path)
    comparison = read_curve(comparison_path)
    freqs = sorted(set(baseline) & set(comparison))
    rows = []
    for freq in freqs:
        b = baseline[freq]
        c = comparison[freq]
        rows.append((freq, b, c, abs(c - b)))
    if not rows:
        raise ValueError("No common frequency points")
    return rows


def write_dat(path: Path, rows: list[tuple[float, float, float, float]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as f:
        f.write("freq baseline nonperiodic diff\n")
        for freq, baseline, nonperiodic, diff in rows:
            f.write(f"{freq:.9f} {baseline:.12g} {nonperiodic:.12g} {diff:.12g}\n")


def latex_escape(text: str) -> str:
    replacements = {
        "\\": r"\textbackslash{}",
        "_": r"\_",
        "%": r"\%",
        "&": r"\&",
        "#": r"\#",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def write_tex(
    path: Path,
    dat_name: str,
    sample_id: str,
    label: float,
    max_diff: float,
) -> None:
    sample = latex_escape(sample_id)
    path.write_text(
        rf"""\documentclass[tikz,border=3pt]{{standalone}}
\usepackage{{pgfplots}}
\usepackage{{siunitx}}
\pgfplotsset{{compat=1.18}}
\usepgfplotslibrary{{groupplots}}
\definecolor{{baselineblue}}{{RGB}}{{31,91,140}}
\definecolor{{comparisonorange}}{{RGB}}{{210,117,39}}
\definecolor{{diffred}}{{RGB}}{{150,45,45}}
\begin{{document}}
\begin{{tikzpicture}}
\begin{{groupplot}}[
  group style={{group size=1 by 2, vertical sep=0.55cm}},
  width=13.2cm,
  height=5.1cm,
  xmin=6, xmax=24,
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
\nextgroupplot[
  ylabel={{Magnitude $|S|$}},
  ymin=0,
  title={{\textbf{{Corrected coupling response}}: \texttt{{{sample}}}}},
  title style={{font=\small, yshift=-0.6ex}},
]
\addplot+[baselineblue, line width=0.85pt, mark=none]
  table[x=freq,y=baseline] {{{dat_name}}};
\addlegendentry{{same-center five-cell}}
\addplot+[comparisonorange, line width=0.85pt, mark=none]
  table[x=freq,y=nonperiodic] {{{dat_name}}};
\addlegendentry{{nonperiodic five-cell}}
\node[anchor=north east, font=\footnotesize, align=right, fill=white, fill opacity=0.85, text opacity=1]
  at (rel axis cs:0.985,0.965)
  {{$\overline{{\Delta |S|}}=\num{{{label:.6f}}}$\\$\max\Delta |S|=\num{{{max_diff:.6f}}}$}};

\nextgroupplot[
  xlabel={{Frequency (GHz)}},
  ylabel={{$|\Delta S|$}},
  ymin=0,
  legend style={{
    draw=none,
    fill=none,
    font=\footnotesize,
    at={{(0.02,0.98)}},
    anchor=north west,
  }},
]
\addplot+[diffred, line width=0.75pt, mark=none]
  table[x=freq,y=diff] {{{dat_name}}};
\addlegendentry{{absolute magnitude difference}}
\end{{groupplot}}
\end{{tikzpicture}}
\end{{document}}
""",
        encoding="utf-8",
    )


def compile_pdf(tex_path: Path, output_pdf: Path) -> None:
    cmd = [
        str(PDFLATEX),
        "-interaction=nonstopmode",
        "-halt-on-error",
        tex_path.name,
    ]
    subprocess.run(cmd, cwd=tex_path.parent, check=True)
    generated_pdf = tex_path.with_suffix(".pdf")
    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    generated_pdf.replace(output_pdf)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", default=DEFAULT_BASELINE, type=Path)
    parser.add_argument("--comparison", default=DEFAULT_COMPARISON, type=Path)
    parser.add_argument("--output", default=DEFAULT_OUTPUT, type=Path)
    parser.add_argument("--workdir", default=DEFAULT_WORKDIR, type=Path)
    parser.add_argument("--sample-id", default="grid_05506_np_r04")
    args = parser.parse_args()

    rows = aligned_rows(args.baseline, args.comparison)
    mean_diff = sum(row[3] for row in rows) / len(rows)
    max_diff = max(row[3] for row in rows)

    args.workdir.mkdir(parents=True, exist_ok=True)
    dat_path = args.workdir / f"{args.sample_id}_paper_plot.dat"
    tex_path = args.workdir / f"{args.sample_id}_paper_plot.tex"
    write_dat(dat_path, rows)
    write_tex(tex_path, dat_path.name, args.sample_id, mean_diff, max_diff)
    compile_pdf(tex_path, args.output)

    print(f"points: {len(rows)}")
    print(f"mean_abs_difference: {mean_diff}")
    print(f"max_abs_difference: {max_diff}")
    print(f"dat: {dat_path.resolve()}")
    print(f"tex: {tex_path.resolve()}")
    print(f"output: {args.output.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
