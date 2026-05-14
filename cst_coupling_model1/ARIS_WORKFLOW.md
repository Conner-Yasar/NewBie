# ARIS 工作流规范 / ARIS Workflow Contract

创建日期：2026-05-13  
更新日期：2026-05-14  
Created: 2026-05-13  
Updated: 2026-05-14

## 1. 定位 / Purpose

中文：  
本文档定义本次 CST 耦合效应任务采用的本地 ARIS 工作流规范。ARIS 在这里表示一种研究闭环组织方式：需求清晰、证据留痕、脚本可复现、数据可追溯、模型可验证、结论可审计。

English:  
This document defines the local ARIS workflow contract for the CST coupling-effect task. Here, ARIS means a research-loop organization style: clear requirements, preserved evidence, reproducible scripts, traceable data, verifiable models, and auditable claims.

## 2. 文件边界 / File Boundary

中文：  
本任务所有新建文件必须位于 `E:\aris\meta` 下，主任务目录为：

English:  
All newly created files for this task must stay under `E:\aris\meta`. The main task directory is:

```text
E:\aris\meta\cst_coupling_model1
```

## 3. 双语文档规则 / Bilingual Documentation Rule

中文：  
所有说明性文档必须中英文双语，包括 README、需求、实验计划、数据集说明、训练报告、优化报告和最终总结。

English:  
All explanatory documents must be bilingual in Chinese and English, including README, requirements, experiment plans, dataset descriptions, training reports, optimization reports, and final summaries.

## 4. 当前固定设置 / Current Fixed Settings

- 邻域窗口：`[L2, L1, C, R1, R2]`  
  Neighborhood window: `[L2, L1, C, R1, R2]`
- 输入维度：`5 × (Atheta, Pphi) = 10`  
  Input dimension: `5 × (Atheta, Pphi) = 10`
- `Atheta`：幅度调控几何角，`0` 到 `-45` 度，步长 `0.5` 度  
  `Atheta`: amplitude-control geometry angle, `0` to `-45` deg, step `0.5` deg
- `Pphi`：相位调控几何角，`50` 到 `170` 度，步长 `1` 度  
  `Pphi`: phase-control geometry angle, `50` to `170` deg, step `1` deg
- 周期采样：单元级全网格，`91 × 121 = 11011` 条  
  Periodic sampling: unit-cell full grid, `91 × 121 = 11011` samples
- 非周期采样：每个周期中心参数 `K=5` 条五单元窗口，当前 `11011 × 5 = 55055`  
  Nonperiodic sampling: `K=5` five-cell windows per periodic center pair, currently `11011 × 5 = 55055`
- 邻居唯一性：五个参数对、五个 `Atheta`、五个 `Pphi` 均不能重复  
  Neighbor uniqueness: all five parameter pairs, five `Atheta` values, and five `Pphi` values must be unique
- 扰动分层：`perturbation_tier = low/medium/high`  
  Perturbation tier: `perturbation_tier = low/medium/high`
- 响应通道：`SZmax(2),Zmin(1)`  
  Response channel: `SZmax(2),Zmin(1)`
- 标签频段：`6-24 GHz`  
  Label band: `6-24 GHz`

## 5. 阶段门 / Phase Gates

| 阶段 / Phase | 进入条件 / Entry Condition | 退出条件 / Exit Condition |
| --- | --- | --- |
| Requirements | 用户目标明确 / User goal is stated | 双语需求与研究契约更新 / Bilingual requirements and research contract updated |
| Sampling index | 参数范围与中心匹配规则明确 / Parameter ranges and center-matching rule are clear | 周期全网格和非周期中心匹配 CSV 已生成并校验 / Periodic full-grid and nonperiodic center-matched CSVs generated and verified |
| CST micro loop | 新采样表可用 / New manifests available | 1-3 条中心匹配样本完成 CST 生成、求解、导出、标签 / 1-3 center-matched samples complete CST generation, solving, export, and labeling |
| Batch dataset | 小闭环稳定 / Micro loop is stable | 批量数据集质量报告通过 / Batch dataset quality report passes |
| Predictor | 数据集清洗完成 / Dataset cleaned | 测试误差优于均值基线 / Test error beats mean baseline |
| Optimization | 预测模型可用 / Predictor usable | 候选生成并 CST 复验 / Candidates generated and CST-reverified |
| Claim | 优化前后结果齐全 / Before/after results available | 报告说明证据是否支持耦合减弱 / Report states whether reduced coupling is supported |

## 6. Artifact Contract

| 文件 / Artifact | 用途 / Purpose |
| --- | --- |
| `RESEARCH_CONTRACT.md` | 当前任务真相和恢复入口 / Current source of truth and recovery entry |
| `EXPERIMENT_PLAN.md` | Claim map、实验块和成功标准 / Claim map, experiment blocks, and success criteria |
| `EXPERIMENT_LOG.md` | CST 运行、失败、修复、数据生成记录 / CST runs, failures, fixes, and dataset generation log |
| `docs/PILOT_SAMPLING_PLAN.md` | 采样规则 / Sampling rules |
| `docs/DATASET_SCHEMA.md` | 数据字段和标签定义 / Dataset fields and label definition |
| `DATASET_CARD.md` | 后续批量数据集质量卡 / Future batch dataset quality card |
| `MODEL_REPORT.md` | 后续预测模型报告 / Future predictor report |
| `OPTIMIZATION_REPORT.md` | 后续优化和复验报告 / Future optimization and re-verification report |
| `RESULT_TO_CLAIM.md` | 后续结论支撑审计 / Future claim-support audit |

## 7. 当前执行顺序 / Current Execution Order

1. 更新文档和采样脚本。  
   Update documents and the sampling script.
2. 生成并校验新的采样 CSV。  
   Generate and verify the new sampling CSVs.
3. 停止沿用旧的 `pilot_0024/pilot_0019` 作为当前小闭环。  
   Stop using the old `pilot_0024/pilot_0019` as the current micro-loop samples.
4. 从 `micro_loop_candidates.csv` 中选择新的 1-3 条 `grid_*_np_r01` 样本进入 CST。  
   Select new 1-3 `grid_*_np_r01` samples from `micro_loop_candidates.csv` for CST.
