# CST 耦合效应研究任务 / CST Coupling-Effect Research Task

创建日期：2026-05-13  
更新日期：2026-05-14  
Created: 2026-05-13  
Updated: 2026-05-14

## 目标 / Goal

中文：  
基于导师提供的标准模型 `E:\aris\模型1`，构建完整研究闭环：周期/非周期数据集、耦合效应预测模型、优化搜索、CST 复验，并证明优化可以减弱耦合效应。

English:  
Based on the advisor-provided standard model `E:\aris\模型1`, build a complete research loop: periodic/nonperiodic datasets, a coupling-effect predictor, optimization search, CST re-verification, and evidence that optimization can reduce coupling.

## 当前采样规则 / Current Sampling Rule

- `Atheta`：幅度调控几何角，`0` 到 `-45` 度，步长 `0.5` 度。  
  `Atheta`: amplitude-control geometry angle, `0` to `-45` deg, step `0.5` deg.
- `Pphi`：相位调控几何角，`50` 到 `170` 度，步长 `1` 度。  
  `Pphi`: phase-control geometry angle, `50` to `170` deg, step `1` deg.
- 周期样本：单元级全网格，`91 × 121 = 11011` 条。  
  Periodic samples: unit-cell full grid, `91 × 121 = 11011` samples.
- 非周期样本：每个周期中心参数对应 `K=5` 条五单元窗口 `[L2, L1, C, R1, R2]`，共 `55055` 条。  
  Nonperiodic samples: `K=5` five-cell windows `[L2, L1, C, R1, R2]` per periodic center pair, `55055` rows in total.
- 中心单元 `C` 与对应周期样本完全一致；`L2/L1/R1/R2` 随机，五个参数对、五个 `Atheta`、五个 `Pphi` 都不能重复。  
  The center cell `C` exactly matches the corresponding periodic sample; `L2/L1/R1/R2` are random, and the five parameter pairs, five `Atheta` values, and five `Pphi` values must all be unique.
- 非周期样本包含 `perturbation_tier` 字段，按邻居扰动强度分为 `low/medium/high`。  
  Nonperiodic samples include `perturbation_tier`, split into `low/medium/high` by neighborhood perturbation strength.

## 关键文件 / Key Files

| 文件 / File | 说明 / Description |
| --- | --- |
| `RESEARCH_CONTRACT.md` | 当前任务真相和恢复入口 / Current source of truth and recovery entry |
| `docs/PILOT_SAMPLING_PLAN.md` | 新采样计划 / New sampling plan |
| `docs/DATASET_SCHEMA.md` | 数据字段规范 / Dataset schema |
| `configs/sampling_pilot.json` | 采样配置 / Sampling configuration |
| `scripts/generate_pilot_samples.py` | 采样表生成脚本 / Sampling manifest generator |
| `data/periodic_full_grid.csv` | 周期单元全网格 / Periodic unit-cell full grid |
| `data/nonperiodic_center_matched_samples.csv` | 中心匹配非周期样本 / Center-matched nonperiodic samples |

## 运行采样脚本 / Run Sampling Script

```powershell
D:\software\anaconda\envs\cst\python.exe E:\aris\meta\cst_coupling_model1\scripts\generate_pilot_samples.py
```
