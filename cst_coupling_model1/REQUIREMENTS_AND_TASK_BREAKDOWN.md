# CST 耦合效应任务需求与拆分 / CST Coupling-Effect Requirements and Task Breakdown

创建日期：2026-05-13  
更新日期：2026-05-14  
Created: 2026-05-13  
Updated: 2026-05-14

## 1. 任务目标 / Goal

中文：  
基于导师提供的标准模型 `E:\aris\模型1`，建立完整研究闭环：周期单元全网格基准、中心匹配非周期五单元数据集、耦合效应预测模型、优化搜索、CST 复验和结论报告。

English:  
Using the advisor-provided standard model `E:\aris\模型1`, build a complete research loop: periodic unit-cell full-grid baseline, center-matched nonperiodic five-cell dataset, coupling-effect predictor, optimization search, CST re-verification, and final reporting.

## 2. 文件边界 / File Boundary

中文：  
本任务创建的所有文件只能放在 `E:\aris\meta` 中。标准模型 `E:\aris\模型1` 只作为源模型和验证对象，不能直接覆盖或破坏。

English:  
All files created for this task must be placed under `E:\aris\meta`. The standard model `E:\aris\模型1` is used only as the source and verification model and must not be overwritten or damaged.

## 3. 双语文档规则 / Bilingual Documentation Rule

中文：  
所有说明文档、README、实验计划、数据集说明、训练说明、优化报告和结论报告都必须使用中英文双语。

English:  
All explanatory documents, READMEs, experiment plans, dataset descriptions, training notes, optimization reports, and conclusion reports must be bilingual in Chinese and English.

## 4. 已确认研究设置 / Confirmed Research Settings

| 项目 / Item | 中文 / Chinese | English |
| --- | --- | --- |
| 标准模型 / Standard model | `E:\aris\模型1` | `E:\aris\模型1` |
| 任务目录 / Task directory | `E:\aris\meta\cst_coupling_model1` | `E:\aris\meta\cst_coupling_model1` |
| 几何变量 / Geometry variables | `Atheta`, `Pphi` | `Atheta`, `Pphi` |
| `Atheta` | 幅度调控几何角；中心结构/中心臂旋转角度 | Amplitude-control geometry angle; center-structure or center-arm rotation angle |
| `Pphi` | 相位调控几何角；圆环/延伸臂圆心角 | Phase-control geometry angle; circular extension-arm central angle |
| `Atheta` 范围 / `Atheta` range | `0` 到 `-45` 度，步长 `0.5` 度 | `0` to `-45` deg, step `0.5` deg |
| `Pphi` 范围 / `Pphi` range | `50` 到 `170` 度，步长 `1` 度 | `50` to `170` deg, step `1` deg |
| 周期采样 / Periodic sampling | 单元级全网格，`11011` 条 | Unit-cell full grid, `11011` samples |
| 非周期采样 / Nonperiodic sampling | 每个周期中心参数 `K=5` 条五单元窗口，当前 `11011 × 5 = 55055` | `K=5` five-cell windows per periodic center pair, currently `11011 × 5 = 55055` |
| 五单元窗口 / Five-cell window | `[L2, L1, C, R1, R2]` | `[L2, L1, C, R1, R2]` |
| 邻居规则 / Neighbor rule | `L2/L1/R1/R2` 随机，五个参数对、五个 `Atheta`、五个 `Pphi` 均不能重复 | `L2/L1/R1/R2` random; all five parameter pairs, five `Atheta` values, and five `Pphi` values unique |
| 扰动分层 / Perturbation tier | `low/medium/high`，按邻居扰动强度分层 | `low/medium/high`, stratified by neighborhood perturbation strength |
| 响应通道 / Response channel | `SZmax(2),Zmin(1)` | `SZmax(2),Zmin(1)` |
| 标签频段 / Label band | `6-24 GHz` | `6-24 GHz` |

## 5. 周期/非周期样本定义 / Periodic and Nonperiodic Sample Definition

中文：  
周期样本只包含一个单元，覆盖所有离散 `Atheta/Pphi` 组合：

English:  
Each periodic sample contains one unit cell and covers every discrete `Atheta/Pphi` combination:

```text
Atheta: 0, -0.5, -1.0, ..., -45.0
Pphi:   50, 51, 52, ..., 170
Total:  91 × 121 = 11011
```

中文：  
非周期样本由五个单元组成：

English:  
Each nonperiodic sample consists of five cells:

```text
[L2_Atheta, L2_Pphi,
 L1_Atheta, L1_Pphi,
 C_Atheta,  C_Pphi,
 R1_Atheta, R1_Pphi,
 R2_Atheta, R2_Pphi]
```

中文：  
每条非周期样本的中心单元 `C` 与对应周期样本参数完全一致。每个中心参数生成 `K=5` 组邻居。两侧四个邻居随机抽取，并且 `L2/L1/C/R1/R2` 的五个 `(Atheta, Pphi)` 参数对、五个 `Atheta`、五个 `Pphi` 均不能重复。每条样本记录 `perturbation_tier`，取值为 `low/medium/high`。

English:  
The center cell `C` in each nonperiodic sample exactly matches the corresponding periodic sample. Each center pair generates `K=5` neighbor groups. The four side neighbors are randomly drawn, and the five `(Atheta, Pphi)` pairs, five `Atheta` values, and five `Pphi` values across `L2/L1/C/R1/R2` must be unique. Each sample records `perturbation_tier` as `low/medium/high`.

## 6. 耦合效应标签 / Coupling-Effect Label

中文：  
主标签按可用频段 `6-24 GHz` 计算，表示非周期五单元超胞响应与同中心参数五单元超胞基准响应在 `SZmax(2),Zmin(1)` 通道上的平均幅值绝对差。

English:  
The primary label is computed over the available `6-24 GHz` band and represents the mean absolute magnitude difference between the nonperiodic five-cell supercell and the same-center five-cell supercell baseline on the `SZmax(2),Zmin(1)` channel.

```text
coupling_label_6_24ghz = mean_f | |S_five_cell_nonperiodic(f)| - |S_five_cell_same_center(f)| |, f in [6, 24] GHz
```

## 7. 当前任务拆分 / Current Task Breakdown

1. 更新文档和采样脚本。  
   Update documents and the sampling script.
2. 生成 `periodic_full_grid.csv` 与 `nonperiodic_center_matched_samples.csv`。  
   Generate `periodic_full_grid.csv` and `nonperiodic_center_matched_samples.csv`.
3. 校验中心匹配和参数对唯一性。  
   Verify center matching and parameter-pair uniqueness.
4. 从新非周期样本中选择 1-3 条进入 CST 小闭环。  
   Select 1-3 samples from the new nonperiodic manifest for the CST micro loop.
5. 生成新的周期、same-center、非周期 CST 工程并导出曲线。  
   Generate new periodic, same-center, and nonperiodic CST projects and export curves.
6. 批量扩展数据集、训练预测模型、优化并 CST 复验。  
   Scale the dataset, train the predictor, optimize, and re-verify in CST.

## 8. 当前暂停项 / Paused Items

中文：  
旧的 `pilot_0024/pilot_0019` 不再继续作为当前采样口径的小闭环样本。它们可以保留为历史尝试记录，但后续应使用新生成的 `grid_*_np_r01` 样本。

English:  
The old `pilot_0024/pilot_0019` runs should not continue as micro-loop samples under the current sampling definition. They can remain as historical attempts, but future work should use the newly generated `grid_*_np_r01` samples.
