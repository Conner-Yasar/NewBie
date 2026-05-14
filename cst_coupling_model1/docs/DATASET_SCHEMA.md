# 数据集字段规范 / Dataset Schema

创建日期：2026-05-13  
更新日期：2026-05-14  
Created: 2026-05-13  
Updated: 2026-05-14

## 1. 数据集结构 / Dataset Structure

中文：  
数据集分为周期全网格基准和中心匹配非周期五单元窗口。周期样本提供单元级理想响应库；非周期样本在同一个中心参数下引入随机且不重复的左右邻居，用于测量耦合效应。

English:  
The dataset is split into a periodic full-grid baseline and center-matched nonperiodic five-cell windows. Periodic samples provide a unit-cell ideal response library. Nonperiodic samples introduce random, non-duplicated left/right neighbors under the same center parameters to measure coupling effects.

## 2. 周期全网格字段 / Periodic Full-Grid Fields

文件 / File:

```text
data/periodic_full_grid.csv
```

| 字段 / Field | 含义 / Meaning |
| --- | --- |
| `sample_id` | 周期样本编号 / Periodic sample identifier |
| `sampling_stage` | 采样阶段 / Sampling stage |
| `sampling_method` | 固定为 `periodic_full_grid` / Fixed as `periodic_full_grid` |
| `grid_index` | 全网格序号 / Full-grid index |
| `Atheta` | 幅度调控几何角，`0` 到 `-45`，步长 `0.5` / Amplitude-control geometry angle, `0` to `-45`, step `0.5` |
| `Pphi` | 相位调控几何角，`50` 到 `170`，步长 `1` / Phase-control geometry angle, `50` to `170`, step `1` |
| `periodic_Atheta` | 等于 `Atheta` / Equal to `Atheta` |
| `periodic_Pphi` | 等于 `Pphi` / Equal to `Pphi` |

周期样本数 / Periodic sample count:

```text
91 × 121 = 11011
```

## 3. 非周期中心匹配字段 / Nonperiodic Center-Matched Fields

文件 / File:

```text
data/nonperiodic_center_matched_samples.csv
```

中文：  
每条非周期样本使用五单元窗口 `[L2, L1, C, R1, R2]`。中心单元 `C` 与对应周期样本完全一致；`L2/L1/R1/R2` 从同一离散参数网格随机抽取。五个单元的 `(Atheta, Pphi)` 参数对必须全部唯一。

English:  
Each nonperiodic sample uses the five-cell window `[L2, L1, C, R1, R2]`. The center cell `C` exactly matches the corresponding periodic sample. `L2/L1/R1/R2` are randomly drawn from the same discrete parameter grid. The five `(Atheta, Pphi)` pairs must all be unique.

| 字段 / Field | 含义 / Meaning |
| --- | --- |
| `sample_id` | 非周期样本编号 / Nonperiodic sample identifier |
| `center_sample_id` | 对应周期中心样本编号 / Matched periodic center sample identifier |
| `grid_index` | 对应周期全网格序号 / Matched periodic full-grid index |
| `repeat_id` | 同一中心参数下的邻居重复编号 / Neighbor repeat index under the same center |
| `neighbor_seed` | 邻居随机采样种子 / Random seed for neighbor sampling |
| `center_Atheta` | 中心幅度调控几何角 / Center amplitude-control geometry angle |
| `center_Pphi` | 中心相位调控几何角 / Center phase-control geometry angle |
| `L2_Atheta`, `L2_Pphi` | 左二邻居参数 / L2 neighbor parameters |
| `L1_Atheta`, `L1_Pphi` | 左一邻居参数 / L1 neighbor parameters |
| `C_Atheta`, `C_Pphi` | 中心单元参数，等于对应周期样本 / Center-cell parameters, equal to the matched periodic sample |
| `R1_Atheta`, `R1_Pphi` | 右一邻居参数 / R1 neighbor parameters |
| `R2_Atheta`, `R2_Pphi` | 右二邻居参数 / R2 neighbor parameters |
| `periodic_sample_id` | 对应周期样本编号 / Matched periodic sample identifier |
| `periodic_Atheta`, `periodic_Pphi` | 对应周期样本参数 / Matched periodic parameters |
| `neighbor_contrast_mean` | 四个邻居相对中心的平均归一化距离 / Mean normalized distance from four neighbors to the center |
| `neighbor_contrast_max` | 四个邻居相对中心的最大归一化距离 / Maximum normalized distance from four neighbors to the center |
| `center_distance_from_midrange` | 中心参数离范围中值的归一化距离 / Normalized distance from the center parameters to the midrange |
| `perturbation_tier` | 邻居扰动分层，`low/medium/high` / Neighborhood perturbation tier, `low/medium/high` |
| `selected_for_micro_loop` | 是否进入 CST 小闭环 / Whether selected for the CST micro loop |
| `micro_loop_role` | 小闭环代表性角色 / Representative micro-loop role |

中文：  
非周期采样当前使用 `K=5`，因此每个 `center_sample_id` 有 5 条邻居样本。每条样本要求五个 `(Atheta, Pphi)` 参数对唯一、五个 `Atheta` 值唯一、五个 `Pphi` 值唯一。

English:  
The current nonperiodic sampling uses `K=5`, so each `center_sample_id` has five neighbor samples. Each sample requires unique five `(Atheta, Pphi)` pairs, unique five `Atheta` values, and unique five `Pphi` values.

## 4. 标签定义 / Label Definition

中文：  
主标签固定为 `coupling_label_6_24ghz`，按可用频段 `6-24 GHz` 计算。推荐主标签是非周期五单元超胞与同中心参数五单元超胞基准在 `SZmax(2),Zmin(1)` 通道上的平均幅值绝对差：

English:  
The primary label is fixed as `coupling_label_6_24ghz` and is computed over the available `6-24 GHz` band. The recommended primary label is the mean absolute magnitude difference between the nonperiodic five-cell supercell and the same-center five-cell supercell baseline on the `SZmax(2),Zmin(1)` channel:

```text
coupling_label_6_24ghz = mean_f | |S_five_cell_nonperiodic(f)| - |S_five_cell_same_center(f)| |, f in [6, 24] GHz
```

中文：  
周期单元响应仍然保留为单元级基准库，可用于查询同一 `(Atheta, Pphi)` 的理想周期响应和辅助分析，但证明“邻居差异导致耦合”的主比较优先使用 same-center 五单元基准。

English:  
The periodic unit-cell response is still kept as a unit-level baseline library for querying the ideal periodic response under the same `(Atheta, Pphi)` and for auxiliary analysis. However, claims about coupling caused by neighbor differences should primarily use the same-center five-cell baseline.
