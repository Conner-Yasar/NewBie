# 实验计划 / Experiment Plan

创建日期：2026-05-13  
更新日期：2026-05-14  
Created: 2026-05-13  
Updated: 2026-05-14

## 1. 问题 / Problem

中文：  
非周期邻域中，左右邻居单元的 `Atheta/Pphi` 与中心单元不一致，会使中心响应偏离同中心五单元基准。我们需要构建数据集和预测模型，并通过优化寻找低耦合邻域组合。

English:  
In a nonperiodic neighborhood, left/right neighbor cells with `Atheta/Pphi` values different from the center cell can shift the center response away from the same-center five-cell baseline. We need to build a dataset and predictor, then use optimization to find low-coupling neighborhood combinations.

## 2. 数据设计 / Data Design

中文：  
周期数据集是单元级全网格基准，共 `11011` 条。非周期数据集与周期中心参数一一对应；每个中心参数至少生成一条 `[L2, L1, C, R1, R2]` 五单元窗口，其中 `C` 等于周期样本，四个邻居随机且五个参数对不重复。

English:  
The periodic dataset is a unit-cell full-grid baseline with `11011` samples. The nonperiodic dataset is center-matched to the periodic center parameters. Each center pair has `K=5` `[L2, L1, C, R1, R2]` five-cell windows, where `C` equals the periodic sample, four neighbors are random, and all five parameter pairs, five `Atheta` values, and five `Pphi` values are unique. Each row includes a `low/medium/high` perturbation tier.

## 3. Claim Map

| Claim | 中文 / Chinese | English | 最低证据 / Minimum Evidence |
| --- | --- | --- | --- |
| C1 | 数据集能量化非周期邻居导致的耦合标签 | The dataset quantifies coupling labels caused by nonperiodic neighbors | CST 小闭环可导出曲线并计算 `6-24 GHz` 标签 / CST micro loop exports curves and computes `6-24 GHz` labels |
| C2 | 预测模型能从五单元角度输入预测耦合标签 | The predictor can estimate coupling labels from five-cell angle inputs | 测试集 MAE/RMSE/R2 优于均值基线 / Test MAE/RMSE/R2 beats mean baseline |
| C3 | 优化能找到更低耦合的角度组合 | Optimization can find lower-coupling angle combinations | 代理模型和 CST 复验均显示标签下降 / Surrogate and CST re-verification both show label reduction |

## 4. 实验块 / Experiment Blocks

### B0: 采样索引 / Sampling Index

中文：
- 生成 `data/periodic_full_grid.csv`，共 `11011` 条。
- 生成 `data/nonperiodic_center_matched_samples.csv`，当前 `11011 × 5 = 55055` 条。
- 写入 `perturbation_tier` 字段，按邻居扰动强度分为 `low/medium/high`。
- 校验每条非周期样本中心匹配周期样本，且五个参数对不重复。

English:
- Generate `data/periodic_full_grid.csv` with `11011` rows.
- Generate `data/nonperiodic_center_matched_samples.csv`, currently `11011 × 5 = 55055` rows.
- Write `perturbation_tier`, split into `low/medium/high` by neighborhood perturbation strength.
- Verify that each nonperiodic sample center matches its periodic sample and that all five parameter pairs are unique.

### B1: CST 小闭环 / CST Micro Loop

中文：
- 从新非周期样本中选 1-3 条代表性样本。
- 生成周期单元工程、same-center 五单元工程、真实非周期五单元工程。
- 导出 `SZmax(2),Zmin(1)`，计算 `6-24 GHz` 标签并画曲线。

English:
- Select 1-3 representative samples from the new nonperiodic manifest.
- Generate the periodic unit-cell project, same-center five-cell project, and true nonperiodic five-cell project.
- Export `SZmax(2),Zmin(1)`, compute the `6-24 GHz` label, and plot curves.

### B2: 批量数据集 / Batch Dataset

中文：
- 小闭环稳定后，按批次求解周期全网格和非周期中心匹配样本。
- 记录失败样本、异常曲线和剔除规则。

English:
- After the micro loop is stable, solve the periodic full grid and center-matched nonperiodic samples in batches.
- Record failed samples, abnormal curves, and exclusion rules.

### B3: 预测模型与优化 / Predictor and Optimization

中文：
- 输入为 10 维 `[L2, L1, C, R1, R2] × [Atheta, Pphi]`。
- 输出为 `coupling_label_6_24ghz`。
- 用预测模型搜索低耦合邻域组合，并送回 CST 复验。

English:
- Input is the 10-dimensional `[L2, L1, C, R1, R2] × [Atheta, Pphi]`.
- Output is `coupling_label_6_24ghz`.
- Use the predictor to search for low-coupling neighborhoods and send candidates back to CST for re-verification.

## 5. 当前执行顺序 / Current Run Order

1. 更新文档和采样脚本。  
   Update documents and the sampling script.
2. 使用新规则生成采样 CSV。  
   Generate sampling CSVs with the new rules.
3. 选取新的 1-3 条中心匹配样本进入 CST 小闭环。  
   Select new 1-3 center-matched samples for the CST micro loop.
4. 不继续旧的 `pilot_0024/pilot_0019`。  
   Do not continue the old `pilot_0024/pilot_0019` runs.
