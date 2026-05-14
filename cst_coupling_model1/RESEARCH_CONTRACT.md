# 研究契约 / Research Contract

更新日期：2026-05-14  
Updated: 2026-05-14

## 当前目标 / Current Goal

中文：  
基于 `E:\aris\模型1` 标准 CST 模型，建立周期单元全网格基准和中心匹配非周期五单元窗口数据集，训练耦合效应预测模型，并通过优化证明耦合效应可以减弱。

English:  
Using the standard CST model at `E:\aris\模型1`, build a periodic unit-cell full-grid baseline and a center-matched nonperiodic five-cell-window dataset, train a coupling-effect predictor, and use optimization to show that the coupling effect can be reduced.

## 固定文件边界 / Fixed File Boundary

中文：  
本任务创建的所有文件只能放在：

English:  
All files created for this task must stay under:

```text
E:\aris\meta
```

主任务目录 / Main task directory:

```text
E:\aris\meta\cst_coupling_model1
```

## 当前采样定义 / Current Sampling Definition

| 项目 / Item | 当前定义 / Current Definition |
| --- | --- |
| `Atheta` | 幅度调控几何角；`0` 到 `-45` 度，步长 `0.5` 度 / Amplitude-control geometry angle; `0` to `-45` deg, step `0.5` deg |
| `Pphi` | 相位调控几何角；`50` 到 `170` 度，步长 `1` 度 / Phase-control geometry angle; `50` to `170` deg, step `1` deg |
| 周期样本 / Periodic samples | 单元级全网格，`91 × 121 = 11011` 条 / Unit-cell full grid, `91 × 121 = 11011` samples |
| 非周期样本 / Nonperiodic samples | 每个周期中心参数 `K=5` 条五单元窗口，当前 `11011 × 5 = 55055` / `K=5` five-cell windows per periodic center pair, currently `11011 × 5 = 55055` |
| 五单元窗口 / Five-cell window | `[L2, L1, C, R1, R2]` |
| 中心匹配 / Center matching | `C_Atheta/C_Pphi` 与对应周期样本完全一致 / `C_Atheta/C_Pphi` exactly match the corresponding periodic sample |
| 邻居规则 / Neighbor rule | `L2/L1/R1/R2` 随机抽取，五个参数对、五个 `Atheta`、五个 `Pphi` 均不能重复 / `L2/L1/R1/R2` are randomly drawn; all five parameter pairs, five `Atheta` values, and five `Pphi` values must be unique |
| 扰动分层 / Perturbation tier | `perturbation_tier = low/medium/high`，按 `neighbor_contrast_mean` 三分位分层 / `perturbation_tier = low/medium/high`, split by tertiles of `neighbor_contrast_mean` |
| 响应通道 / Response channel | `SZmax(2),Zmin(1)` |
| 标签频段 / Label band | `6-24 GHz` |

## 主标签 / Primary Label

中文：  
主标签优先使用非周期五单元超胞相对 same-center 五单元超胞基准的平均幅值绝对差，用于隔离邻居差异导致的耦合效应。

English:  
The primary label should use the mean absolute magnitude difference between the nonperiodic five-cell supercell and the same-center five-cell supercell baseline, so that the measured effect is tied to neighbor differences.

```text
coupling_label_6_24ghz = mean_f | |S_five_cell_nonperiodic(f)| - |S_five_cell_same_center(f)| |, f in [6, 24] GHz
```

## 当前下一步 / Current Next Step

中文：  
不要继续跑旧的 `pilot_0024/pilot_0019`。先使用新脚本和新采样表，选择新的中心匹配小闭环样本，再生成 CST 工程。

English:  
Do not continue the old `pilot_0024/pilot_0019` runs. First use the new script and manifests, select new center-matched micro-loop samples, and then generate CST projects.
