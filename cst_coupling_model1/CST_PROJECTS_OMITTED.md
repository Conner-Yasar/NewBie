# CST 工程文件未上传说明 / CST Project Files Omitted

## 中文

本目录保存了 `cst_coupling_model1` 任务的文档、脚本、采样表、导出曲线、分析报告和论文风格图。

完整 CST 工程目录未上传：

- 本地路径：`E:\aris\meta\cst_coupling_model1\cst_projects`
- 主要原因：该目录约 `19 GB`，包含 CST 二进制工程、网格、求解结果、临时文件和重复求解副本，不适合直接提交到 GitHub。

已上传的可复现实验材料包括：

- `scripts/`：采样、CST 配置/导出、标签计算、尖跳分析、绘图脚本。
- `configs/`：采样与标签配置。
- `data/`：采样表、队列、导出的 S 参数 CSV、处理后的标签与相位数据。
- `reports/`：曲线汇总、尖跳同步/复现性分析、窄频段验证结果、PDF/SVG 图。
- `docs/`：中英文任务说明、数据集规范、尖跳复现性说明。

如需复现实验，应在本地重新准备 CST 工程副本，或从导师提供的标准模型 `E:\aris\模型1` 重新生成。

## English

This directory stores the documents, scripts, sampling manifests, exported curves, analysis reports, and publication-style figures for the `cst_coupling_model1` task.

The full CST project directory is not uploaded:

- Local path: `E:\aris\meta\cst_coupling_model1\cst_projects`
- Reason: the directory is about `19 GB` and contains CST binary projects, meshes, solver results, temporary files, and repeated-solve copies. It is not suitable for direct GitHub commits.

Uploaded reproducibility materials include:

- `scripts/`: sampling, CST configuration/export, label computation, spike analysis, and plotting scripts.
- `configs/`: sampling and label configurations.
- `data/`: sampling manifests, queues, exported S-parameter CSV files, processed labels, and phase data.
- `reports/`: curve summaries, spike synchrony/reproducibility analyses, narrow-band verification results, and PDF/SVG figures.
- `docs/`: bilingual task notes, dataset schema, and spike reproducibility notes.

To reproduce the full CST simulations, recreate the CST project copies locally or regenerate them from the advisor-provided standard model at `E:\aris\模型1`.
