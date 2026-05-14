# 实验日志 / Experiment Log

## 2026-05-14 M0.13：新 grid low 样本 CST 小闭环 / New Grid Low-Sample CST Micro Loop

中文：
- 已将 CST 小闭环从旧 `pilot_*` 样本切换到新 `grid_*_np_r*` 样本。
- 更新脚本：`prepare_cst_micro_loop_projects.py` 和 `prepare_same_parameter_control.py` 默认读取 `data/nonperiodic_center_matched_samples.csv`；`build_nonperiodic_five_cell.py`、`configure_and_run_five_cell_supercell.py`、`run_corrected_micro_loop_sample.py` 支持 `--new-cst-session`，避免连接到旧 CST GUI 锁住工程。
- 已完成 low 样本 `grid_05506_np_r04` 端到端验证：非周期五单元工程和 same-center 五单元对照工程均完成求解并导出 `SZmax(2),Zmin(1)`。
- 导出曲线均为 `1001` 点，频段 `6.0-24.0 GHz`。
- corrected label: `coupling_label_6_24ghz = 0.18938352792641058`，`max_abs_difference = 0.5849298844519564`。
- 输出文件：`data/raw/nonperiodic/grid_05506_np_r04_five_cell_szmax2_zmin1.csv`、`data/raw/nonperiodic/grid_05506_np_r04_same_center_szmax2_zmin1.csv`、`data/processed/grid_05506_np_r04_corrected_label.json/csv`、`reports/figures/grid_05506_np_r04_corrected_same_center_vs_nonperiodic.svg`。
- 运行结束后无 `Solver_HF_Tet_FD_AMD64` 或 `CST DESIGN ENVIRONMENT_AMD64` 残留。

English:
- Switched the CST micro loop from old `pilot_*` samples to the new `grid_*_np_r*` samples.
- Updated scripts: `prepare_cst_micro_loop_projects.py` and `prepare_same_parameter_control.py` now default to `data/nonperiodic_center_matched_samples.csv`; `build_nonperiodic_five_cell.py`, `configure_and_run_five_cell_supercell.py`, and `run_corrected_micro_loop_sample.py` support `--new-cst-session` to avoid connecting to stale CST GUI sessions that lock projects.
- Completed end-to-end validation for the low sample `grid_05506_np_r04`: both the nonperiodic five-cell project and the same-center five-cell control project solved and exported `SZmax(2),Zmin(1)`.
- Both exported curves have `1001` points over `6.0-24.0 GHz`.
- Corrected label: `coupling_label_6_24ghz = 0.18938352792641058`, `max_abs_difference = 0.5849298844519564`.
- Output files: `data/raw/nonperiodic/grid_05506_np_r04_five_cell_szmax2_zmin1.csv`, `data/raw/nonperiodic/grid_05506_np_r04_same_center_szmax2_zmin1.csv`, `data/processed/grid_05506_np_r04_corrected_label.json/csv`, and `reports/figures/grid_05506_np_r04_corrected_same_center_vs_nonperiodic.svg`.
- No `Solver_HF_Tet_FD_AMD64` or `CST DESIGN ENVIRONMENT_AMD64` process remained after completion.

## 2026-05-14 M0.12：K=5 与严格唯一性采样 / K=5 and Strict-Uniqueness Sampling

中文：
- 用户确认每个中心参数生成 `K=5` 组邻居。
- 非周期五单元窗口要求五个 `(Atheta, Pphi)` 参数对不能重复，五个 `Atheta` 单独不能重复，五个 `Pphi` 单独也不能重复。
- 新增 `perturbation_tier` 字段，按 `neighbor_contrast_mean` 三分位分为 `low/medium/high`。
- 重新生成采样表：周期 `11011` 条，非周期 `55055` 条。
- 校验结果：中心匹配错误 `0`，参数对重复错误 `0`，`Atheta` 重复错误 `0`，`Pphi` 重复错误 `0`；每个中心最少/最多均为 `5` 条。
- 扰动分层计数：`low=18352`，`medium=18352`，`high=18351`。

English:
- The user confirmed `K=5` neighbor groups for each center pair.
- The nonperiodic five-cell window requires no duplicated `(Atheta, Pphi)` pair, no duplicated `Atheta`, and no duplicated `Pphi` across the five cells.
- Added `perturbation_tier`, split into `low/medium/high` by tertiles of `neighbor_contrast_mean`.
- Regenerated the manifests: `11011` periodic rows and `55055` nonperiodic rows.
- Verification result: `0` center-matching errors, `0` duplicated-pair errors, `0` duplicated-`Atheta` errors, and `0` duplicated-`Pphi` errors; every center has exactly `5` rows.
- Perturbation-tier counts: `low=18352`, `medium=18352`, `high=18351`.

## 2026-05-14 M0.11：采样口径更新 / Sampling Definition Update

中文：
- 用户确认新采样口径：`Atheta` 为幅度调控几何角，范围 `0` 到 `-45` 度、步长 `0.5` 度；`Pphi` 为相位调控几何角，范围 `50` 到 `170` 度、步长 `1` 度。
- 周期数据集改为单元级全网格基准，共 `91 × 121 = 11011` 条。
- 非周期数据集改为中心匹配五单元窗口：每个周期中心参数至少对应一条 `[L2, L1, C, R1, R2]` 样本，中心 `C` 与周期样本完全一致，`L2/L1/R1/R2` 随机，且五个 `(Atheta, Pphi)` 参数对不能重复。
- 已更新采样配置、采样脚本和核心双语文档。
- 已生成并校验 `data/periodic_full_grid.csv`、`data/nonperiodic_center_matched_samples.csv`、`data/micro_loop_candidates.csv`、`data/cst_micro_loop_queue.csv`。
- 校验结果：周期 `11011` 条，非周期 `11011` 条，中心匹配错误 `0` 条，五单元参数重复错误 `0` 条。
- 旧的 `pilot_0024/pilot_0019` 不再继续作为当前采样口径的小闭环样本。

English:
- The user confirmed the new sampling definition: `Atheta` is the amplitude-control geometry angle from `0` to `-45` deg with `0.5` deg step; `Pphi` is the phase-control geometry angle from `50` to `170` deg with `1` deg step.
- The periodic dataset is now a unit-cell full-grid baseline with `91 × 121 = 11011` samples.
- The nonperiodic dataset is now center-matched five-cell windows: each periodic center pair has at least one `[L2, L1, C, R1, R2]` sample; center `C` exactly matches the periodic sample; `L2/L1/R1/R2` are random; all five `(Atheta, Pphi)` pairs must be unique.
- Updated the sampling config, sampling script, and core bilingual documents.
- Generated and verified `data/periodic_full_grid.csv`, `data/nonperiodic_center_matched_samples.csv`, `data/micro_loop_candidates.csv`, and `data/cst_micro_loop_queue.csv`.
- Verification result: `11011` periodic rows, `11011` nonperiodic rows, `0` center-matching errors, and `0` five-cell duplicate-pair errors.
- The old `pilot_0024/pilot_0019` runs should not continue as micro-loop samples under the current sampling definition.

创建日期：2026-05-13  
Created: 2026-05-13

## 2026-05-13 M0.10：扩展 corrected micro-loop / Extend Corrected Micro-Loop

中文：
- 新增 `scripts/run_corrected_micro_loop_sample.py`，用于按统一流程运行单个 Pilot 样本的 corrected 小闭环。
- 目标样本：`pilot_0024` 与 `pilot_0019`。

English:
- Added `scripts/run_corrected_micro_loop_sample.py` to run a single pilot sample through the corrected micro-loop pipeline.
- Target samples: `pilot_0024` and `pilot_0019`.

## 2026-05-13 M0.9：修正标签口径 / Corrected Label Definition

中文：
- 主标签从“非周期五单元超胞 vs 单元周期基准”修正为“非周期五单元超胞 vs 同中心参数五单元超胞基准”。
- 已更新 `configs/label_config.json`, `RESEARCH_CONTRACT.md`, `REQUIREMENTS_AND_TASK_BREAKDOWN.md`, `docs/DATASET_SCHEMA.md`。
- `scripts/build_coupling_label.py` 增加 `--baseline/--comparison` 参数，同时保留旧的 `--periodic/--nonperiodic` 兼容入口。
- 使用已有 `pilot_0070_same_center_szmax2_zmin1.csv` 和 `pilot_0070_five_cell_szmax2_zmin1.csv` 重算 corrected 标签。

English:
- The primary label was corrected from "nonperiodic five-cell supercell vs unit-cell periodic baseline" to "nonperiodic five-cell supercell vs same-center five-cell supercell baseline".
- Updated `configs/label_config.json`, `RESEARCH_CONTRACT.md`, `REQUIREMENTS_AND_TASK_BREAKDOWN.md`, and `docs/DATASET_SCHEMA.md`.
- `scripts/build_coupling_label.py` now supports `--baseline/--comparison` while keeping the legacy `--periodic/--nonperiodic` interface.
- Recomputed the corrected label from the existing `pilot_0070_same_center_szmax2_zmin1.csv` and `pilot_0070_five_cell_szmax2_zmin1.csv`.

结果 / Result:
- 中文：`pilot_0070` corrected `coupling_label_6_24ghz = 0.37355874533438677`。
- English: `pilot_0070` corrected `coupling_label_6_24ghz = 0.37355874533438677`.

## 2026-05-13 M0.8：曲线与同参数对照检查 / Curve and Same-Parameter Control Check

中文：
- 新增 `scripts/plot_response_comparison.py`，绘制 `pilot_0070` 周期基准与五单元非周期响应曲线。
- 新增 `docs/CURVE_AND_CONTROL_CHECK.md`，记录曲线检查和同参数对照样本目的。
- 后续同参数对照样本将使用五个单元都等于中心单元 `C_Atheta/C_Pphi`，用于检验五单元超胞边界/端口是否自身引入大差异。

English:
- Added `scripts/plot_response_comparison.py` to plot the `pilot_0070` periodic baseline and five-cell nonperiodic response curves.
- Added `docs/CURVE_AND_CONTROL_CHECK.md` to record the purpose of the curve check and same-parameter control sample.
- The same-parameter control sample will set all five cells equal to the center-cell `C_Atheta/C_Pphi` to test whether the five-cell supercell boundary/ports introduce a large difference by themselves.

产物 / Artifacts:
- `reports/figures/pilot_0070_periodic_vs_five_cell.svg`
- `reports/figures/pilot_0070_periodic_vs_same_center_control.svg`
- `data/raw/nonperiodic/pilot_0070_same_center_szmax2_zmin1.csv`
- `data/processed/pilot_0070_same_center_label.csv`
- `data/processed/pilot_0070_same_center_label.json`

结果 / Results:
- 中文：`pilot_0070` 五单元非周期标签为 `0.5229127991565287`。
- English: The `pilot_0070` five-cell nonperiodic label is `0.5229127991565287`.
- 中文：`pilot_0070_same_center` 同参数五单元对照标签为 `0.8949670486897399`。
- English: The `pilot_0070_same_center` same-parameter five-cell control label is `0.8949670486897399`.
- 中文：同参数对照差异更大，说明当前“单元周期基准 vs 五单元超胞”的比较口径不可信；需要先建立五单元同参数超胞基准或修正有限阵列边界/端口。
- English: The same-parameter control differs even more, so the current "unit-cell periodic baseline vs five-cell supercell" comparison is not trustworthy yet. A five-cell same-parameter supercell baseline or corrected finite-array boundaries/ports must be established first.

## 2026-05-13 M0.7：五单元超胞边界与求解 / Five-Cell Supercell Boundary and Solve

中文：
- 新增 `scripts/configure_and_run_five_cell_supercell.py`，用于给 `pilot_0070` 的五单元非周期工程追加超胞 Floquet 边界/激励设置并运行求解。
- 新结果必须导出到新文件名，旧的 `data/raw/nonperiodic/pilot_0070_szmax2_zmin1.csv` 是几何重建前模板导出，不作为新几何结果。

English:
- Added `scripts/configure_and_run_five_cell_supercell.py` to append five-cell Floquet supercell boundary/excitation settings to the `pilot_0070` nonperiodic project and run the solver.
- New results must be exported to a new filename. The old `data/raw/nonperiodic/pilot_0070_szmax2_zmin1.csv` was exported before geometry rebuild and is not treated as the new-geometry result.

验证 / Verification:
- 中文：第一次新几何求解只产生 2 个频点，不满足 `6-24 GHz` 标签要求；随后补齐宽带扫频设置并重新运行。
- English: The first new-geometry solve produced only 2 frequency points, which did not satisfy the `6-24 GHz` label requirement; broadband sweep settings were then completed and the solve was rerun.
- 中文：第二次求解在目标通道 `SZmax(2),Zmin(1)` 上成功导出 `1001` 个频点，范围 `6.0-24.0 GHz`。
- English: The second solve successfully exported `1001` points over `6.0-24.0 GHz` on the target channel `SZmax(2),Zmin(1)`.
- 中文：`pilot_0070` 五单元标签为 `coupling_label_6_24ghz = 0.5229127991565287`。
- English: The five-cell label for `pilot_0070` is `coupling_label_6_24ghz = 0.5229127991565287`.
- 中文：CST 仍报告 solver 进程在后台响应/收尾；已尝试官方接口优雅停止但未及时返回。结果文件已经落盘。
- English: CST still reports a responsive solver process in the background; a graceful stop through the official interface was attempted but did not return in time. Result files have been written.

## 2026-05-13 M0.6：pilot_0070 五单元非周期几何 / pilot_0070 Five-Cell Nonperiodic Geometry

中文：
- 新增 `scripts/build_nonperiodic_five_cell.py`，从 `pilot_0070` 的 `micro_loop_metadata.json` 读取 `[L2, L1, C, R1, R2]` 参数并生成 CST VBA history。
- 几何组件命名为 `np_L2`, `np_L1`, `np_C`, `np_R1`, `np_R2`，中心位置分别为 `x = -12, -6, 0, 6, 12 mm`。
- 本步骤目标是让 nonperiodic 工程真实包含五个不同参数单元；有限阵列的边界/端口设置仍需下一步单独验证。

English:
- Added `scripts/build_nonperiodic_five_cell.py` to read `[L2, L1, C, R1, R2]` parameters from `pilot_0070` `micro_loop_metadata.json` and generate CST VBA history.
- The geometry components are named `np_L2`, `np_L1`, `np_C`, `np_R1`, and `np_R2`, centered at `x = -12, -6, 0, 6, 12 mm`.
- This step targets true five-cell nonperiodic geometry in the nonperiodic project; finite-array boundary/port settings still need separate validation in the next step.

验证 / Verification:
- 中文：`build_nonperiodic_five_cell.py` 已成功对 `cst_projects/nonperiodic/pilot_0070/model1.cst` 追加并保存 `build nonperiodic five-cell geometry` history。
- English: `build_nonperiodic_five_cell.py` successfully appended and saved the `build nonperiodic five-cell geometry` history to `cst_projects/nonperiodic/pilot_0070/model1.cst`.
- 中文：`Model.mod` 与 `ModelHistory.json` 中确认存在 `np_L2`, `np_L1`, `np_C`, `np_R1`, `np_R2` 五个组件。
- English: `Model.mod` and `ModelHistory.json` confirm the presence of the five components `np_L2`, `np_L1`, `np_C`, `np_R1`, and `np_R2`.
- 中文：队列中 `pilot_0070` 状态更新为 `five_cell_geometry_built_boundary_pending`。
- English: The queue status for `pilot_0070` was updated to `five_cell_geometry_built_boundary_pending`.

## 2026-05-13 M0.5：CST 小闭环工程副本准备 / CST Micro-Loop Project Copies

中文：
- 新增 `scripts/prepare_cst_micro_loop_projects.py`，根据 `data/cst_micro_loop_queue.csv` 复制 3 条小闭环候选的 periodic/nonperiodic CST 工程副本。
- 新增 `docs/CST_MICRO_LOOP_PREP.md`，记录工程副本边界和当前限制。
- 周期副本写入中心单元 `C_Atheta/C_Pphi` 参数，可作为周期单元模板。
- 非周期副本写入完整五单元参数元数据，但五单元几何拼接仍待实现，因此当前 nonperiodic 副本导出仅可用于流程 smoke test，不能作为物理有效非周期结果。

English:
- Added `scripts/prepare_cst_micro_loop_projects.py` to copy periodic/nonperiodic CST project templates for the 3 micro-loop candidates in `data/cst_micro_loop_queue.csv`.
- Added `docs/CST_MICRO_LOOP_PREP.md` to record the project-copy boundary and current limitations.
- The periodic copy stores the center-cell `C_Atheta/C_Pphi` parameters and can serve as the periodic unit-cell template.
- The nonperiodic copy stores the full five-cell parameter metadata, but five-cell geometry assembly is still pending. Therefore, current nonperiodic exports are only valid as workflow smoke tests, not as physically valid nonperiodic results.

产物 / Artifacts:
- `data/cst_micro_loop_queue_prepared.csv`: 3 条已准备工程副本的队列 / 3 queued samples with prepared project copies.
- `cst_projects/periodic/pilot_0070`, `cst_projects/periodic/pilot_0024`, `cst_projects/periodic/pilot_0019`: 周期模板副本 / periodic template copies.
- `cst_projects/nonperiodic/pilot_0070`, `cst_projects/nonperiodic/pilot_0024`, `cst_projects/nonperiodic/pilot_0019`: 非周期模板副本与五单元参数元数据 / nonperiodic template copies with five-cell parameter metadata.

第一条导出验证 / First-sample export verification:
- 中文：`pilot_0070` 的 periodic 与 nonperiodic 模板副本均成功导出 `SZmax(2),Zmin(1)`，频点数 `1001`，范围 `6.0-24.0 GHz`。
- English: The periodic and nonperiodic template copies for `pilot_0070` both exported `SZmax(2),Zmin(1)` successfully, with `1001` points over `6.0-24.0 GHz`.
- 中文：标签脚本生成 `data/processed/pilot_0070_label.csv/json`，`coupling_label_6_24ghz = 0.0`。该值仅为模板流程 smoke test，不代表真实非周期五单元耦合。
- English: The label script generated `data/processed/pilot_0070_label.csv/json`, with `coupling_label_6_24ghz = 0.0`. This value is only a template workflow smoke test and does not represent true nonperiodic five-cell coupling.

## 2026-05-14 M0.9：尖跳同步与复现性检查 / Spike Synchrony and Reproducibility Check

中文：
- 针对 `grid_05506_np_r04` 导出目标通道和多个相关 S 参数通道，检查幅度尖跳与相位跳变是否同步。
- 新增 `scripts/analyze_sparam_spikes.py`，输出目标通道相位与多通道尖跳对照表。
- 创建并重跑 `cst_projects/nonperiodic/grid_05506_np_r04_repeat01/model1.cst`，使用完整 `DeleteResults()` 后重新求解。
- CST 日志显示 interpolative broadband sweep 实际计算 `105` 个频率样本，最终输出 `1001` 个线性频点；总求解时间 `15702 s`，即 `4 h 21 m 42 s`。
- 重复运行导出的 `SZmax(2),Zmin(1)` 与原始曲线的相邻幅度跳变相关系数为 `0.858689`，主要尖跳频段大体复现。

English:
- Exported the target channel and several related S-parameter channels for `grid_05506_np_r04` to check whether magnitude spikes and phase jumps are synchronized.
- Added `scripts/analyze_sparam_spikes.py` to generate target-channel phase data and a multi-channel spike comparison table.
- Created and reran `cst_projects/nonperiodic/grid_05506_np_r04_repeat01/model1.cst` with a full recomputation after `DeleteResults()`.
- The CST log shows that the interpolative broadband sweep calculated `105` actual frequency samples and produced `1001` final linear output points; total solver time was `15702 s`, or `4 h 21 m 42 s`.
- The repeated `SZmax(2),Zmin(1)` curve has an adjacent magnitude-jump correlation of `0.858689` against the original curve, and the major spike bands are broadly reproduced.

产物 / Artifacts:
- `docs/SPIKE_REPRODUCIBILITY_NOTE.md`
- `reports/grid_05506_np_r04_sparam_spike_analysis.csv`
- `reports/grid_05506_np_r04_repeat01_reproducibility.csv`
- `data/processed/grid_05506_np_r04_target_phase.csv`
- `data/raw/nonperiodic/grid_05506_np_r04_repeat01_five_cell_szmax2_zmin1.csv`

## 2026-05-14 M0.10：窄频段固定采样验证 / Narrow-Band Fixed-Sampling Verification

中文：
- 新增 `scripts/configure_and_run_narrowband_verification.py`，用于从非周期五单元工程副本配置窄频段验证求解。
- 新增三个工程副本：`grid_05506_np_r04_nb_7p8_8p4`、`grid_05506_np_r04_nb_9p2_9p9`、`grid_05506_np_r04_nb_20p3_22p4`。
- 三段均完成 CST 求解并导出 `SZmax(2),Zmin(1)`，每段 `81` 个固定单频采样点。
- 结果显示：`9.2-9.9 GHz` 与 `20.3-22.4 GHz` 的尖跳/快速变化在窄频固定采样中仍明显存在；`7.8-8.4 GHz` 中，原全带 `8.295 GHz` 最大尖跳在窄频固定采样下变平滑，但同段出现新的强变化区 `8.1225-8.1300 GHz`。
- 结论：尖跳不是简单导出错误，但全带自动插值会影响部分尖跳位置；后续模型标签/特征应标记这些快速响应频段。

English:
- Added `scripts/configure_and_run_narrowband_verification.py` to configure narrow-band verification solves from nonperiodic five-cell project copies.
- Added three project copies: `grid_05506_np_r04_nb_7p8_8p4`, `grid_05506_np_r04_nb_9p2_9p9`, and `grid_05506_np_r04_nb_20p3_22p4`.
- All three CST solves completed and exported `SZmax(2),Zmin(1)`, with `81` fixed single-frequency samples per band.
- Results show that spikes/fast variation remain clear in `9.2-9.9 GHz` and `20.3-22.4 GHz`; in `7.8-8.4 GHz`, the original full-band `8.295 GHz` top spike becomes smooth under narrow fixed sampling, while a new strong variation appears at `8.1225-8.1300 GHz`.
- Conclusion: the spikes are not simple export errors, but full-band automatic interpolation can shift or emphasize some spike locations. Later labels/features should flag these fast-response bands.

产物 / Artifacts:
- `scripts/configure_and_run_narrowband_verification.py`
- `scripts/plot_narrowband_verification_pdf.py`
- `reports/grid_05506_np_r04_narrowband_verification_summary.csv`
- `reports/grid_05506_np_r04_narrowband_verification_points.csv`
- `reports/figures/grid_05506_np_r04_narrowband_verification.pdf`

## 2026-05-13 M0.4：Pilot 采样表 / Pilot Sampling Manifest

中文：
- 新增 `configs/sampling_pilot.json`，固定 Pilot 样本数为 80，采样方法为 Latin Hypercube，随机种子为 `20260513`。
- 新增 `scripts/generate_pilot_samples.py`，生成五单元 `[L2, L1, C, R1, R2]` 的 10 维 `Atheta/Pphi` 样本。
- 周期基准规则：每条样本的周期模型使用中心单元 `C_Atheta/C_Pphi`。
- 非周期规则：每条样本的非周期模型使用完整五单元窗口。

English:
- Added `configs/sampling_pilot.json` with 80 pilot samples, Latin Hypercube sampling, and fixed random seed `20260513`.
- Added `scripts/generate_pilot_samples.py` to generate 10-dimensional five-cell `[L2, L1, C, R1, R2]` `Atheta/Pphi` samples.
- Periodic baseline rule: each sample's periodic model uses the center-cell `C_Atheta/C_Pphi`.
- Nonperiodic rule: each sample's nonperiodic model uses the full five-cell window.

产物 / Artifacts:
- `data/sample_manifest_pilot.csv`: 80 条 Pilot 样本 / 80 pilot samples.
- `data/micro_loop_candidates.csv`: 3 条小闭环候选 / 3 micro-loop candidates.
- `data/cst_micro_loop_queue.csv`: 3 条已排队 CST 小闭环任务 / 3 queued CST micro-loop tasks.

验证 / Verification:
- 中文：角度范围检查通过，`Atheta` 全部在 `[-90, 0]`，`Pphi` 全部在 `[50, 170]`；Pilot 行数 80，小闭环候选 3，队列任务 3。
- English: Range checks passed: all `Atheta` values are within `[-90, 0]`, all `Pphi` values are within `[50, 170]`; there are 80 pilot rows, 3 micro-loop candidates, and 3 queued tasks.
- 候选 / Candidates: `pilot_0070` low perturbation, `pilot_0024` medium perturbation, `pilot_0019` high perturbation.

## 2026-05-13 M0.3：标签计算管线 / Label Computation Pipeline

中文：
- 新增 `configs/label_config.json`，固定主标签频段为 `6-24 GHz`。
- 新增 `scripts/build_coupling_label.py`，用于从周期/非周期 `SZmax(2),Zmin(1)` CSV 曲线计算 `coupling_label_6_24ghz`。
- 新增 `docs/DATASET_SCHEMA.md`，记录五单元 10 维输入特征和标签字段。

English:
- Added `configs/label_config.json` to fix the primary label band as `6-24 GHz`.
- Added `scripts/build_coupling_label.py` to compute `coupling_label_6_24ghz` from paired periodic/nonperiodic `SZmax(2),Zmin(1)` CSV curves.
- Added `docs/DATASET_SCHEMA.md` to document the five-cell 10-dimensional input features and label fields.

验证 / Verification:
- 中文：使用标准模型同一条导出曲线同时作为周期和非周期输入，得到 `coupling_label_6_24ghz = 0.0`，频点数 `1001`，频率范围 `6.0-24.0 GHz`。
- English: Using the same exported standard-model curve as both periodic and nonperiodic input produced `coupling_label_6_24ghz = 0.0`, with `1001` frequency points over `6.0-24.0 GHz`.

## 2026-05-13 M0.1：检查 CST 结果导出入口 / Check CST Result Export Entry

中文：

- 目标：检查 `SZmax(2),Zmin(1)` 的自动导出方式。
- 标准模型只读源：`E:\aris\模型1`。
- 验证工程副本：`E:\aris\meta\cst_coupling_model1\cst_projects\export_probe_ascii\model1.cst`。
- 结论：CST 官方 Python 结果接口 `cst.results.ProjectFile` 可读取 1D 复数结果。
- 目标树路径：`1D Results\S-Parameters\SZmax(2),Zmin(1)`。
- 当前保存结果包含 1001 个频点，实际频率范围为 `6.0-24.0 GHz`。
- 注意：用户已明确标签按可用频段 `6-24 GHz` 计算；当前标准模型已保存结果覆盖 `6.0-24.0 GHz`，后续新仿真需要强制确认导出曲线至少覆盖 `6-24 GHz`。

English:

- Goal: check the automatic export method for `SZmax(2),Zmin(1)`.
- Read-only source standard model: `E:\aris\模型1`.
- Verification project copy: `E:\aris\meta\cst_coupling_model1\cst_projects\export_probe_ascii\model1.cst`.
- Conclusion: the official CST Python result interface `cst.results.ProjectFile` can read 1D complex results.
- Target tree path: `1D Results\S-Parameters\SZmax(2),Zmin(1)`.
- The currently saved result contains 1001 frequency points, with an actual frequency range of `6.0-24.0 GHz`.
- Note: the user has confirmed that labels are computed over the available `6-24 GHz` band. The saved standard-model result covers `6.0-24.0 GHz`, so new simulations must explicitly confirm at least `6-24 GHz` coverage.

产物 / Artifacts:

- `scripts/export_cst_1d_result.py`
- `data/raw/periodic/model1_szmax2_zmin1_export_test.csv`



