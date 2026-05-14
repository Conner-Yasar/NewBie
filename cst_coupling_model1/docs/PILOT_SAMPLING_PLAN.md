# 采样计划 / Sampling Plan

创建日期：2026-05-13  
更新日期：2026-05-14  
Created: 2026-05-13  
Updated: 2026-05-14

## 1. 目标 / Goal

中文：  
当前采样口径改为“周期单元全网格基准 + 中心匹配非周期五单元窗口”。周期数据集覆盖所有离散 `Atheta/Pphi` 参数对；非周期数据集为每一个周期中心参数生成对应的 `[L2, L1, C, R1, R2]` 五单元窗口，用于研究邻居不一致带来的耦合效应。

English:  
The sampling definition is now a periodic unit-cell full-grid baseline plus center-matched nonperiodic five-cell windows. The periodic dataset covers every discrete `Atheta/Pphi` pair. The nonperiodic dataset creates a corresponding `[L2, L1, C, R1, R2]` five-cell window for every periodic center pair to study coupling caused by non-identical neighbors.

## 2. 参数范围 / Parameter Ranges

| 变量 / Variable | 范围与步长 / Range and Step | 点数 / Points | 含义 / Meaning |
| --- | --- | --- | --- |
| `Atheta` | `0` to `-45` deg, step `-0.5` deg | `91` | 幅度调控几何角；中心结构/中心臂旋转角度 / Amplitude-control geometry angle; center-structure or center-arm rotation angle |
| `Pphi` | `50` to `170` deg, step `1` deg | `121` | 相位调控几何角；圆环/延伸臂圆心角 / Phase-control geometry angle; circular extension-arm central angle |

中文：  
除 `Atheta` 与 `Pphi` 外，其他 CST 几何参数固定。

English:  
All CST geometry parameters other than `Atheta` and `Pphi` are fixed.

## 3. 周期采样 / Periodic Sampling

中文：  
周期数据集是单元级全网格基准。每个周期样本只包含一个单元，参数为一个离散网格点：

```text
Atheta in {0, -0.5, -1.0, ..., -45.0}
Pphi   in {50, 51, 52, ..., 170}
```

总样本数：

```text
91 × 121 = 11011
```

English:  
The periodic dataset is a unit-cell full-grid baseline. Each periodic sample contains one unit cell with one discrete grid point:

```text
Atheta in {0, -0.5, -1.0, ..., -45.0}
Pphi   in {50, 51, 52, ..., 170}
```

Total sample count:

```text
91 × 121 = 11011
```

## 4. 非周期采样 / Nonperiodic Sampling

中文：  
非周期数据集不做五单元全组合穷举。每一个周期样本 `(Atheta=a, Pphi=p)` 都对应至少一条非周期五单元窗口样本：

```text
[L2, L1, C, R1, R2]
```

中心单元固定为：

```text
C_Atheta = a
C_Pphi   = p
```

两侧邻居单元 `L2/L1/R1/R2` 从同一个离散参数网格随机抽取，并满足：

```text
(L2_Atheta, L2_Pphi)
(L1_Atheta, L1_Pphi)
(C_Atheta,  C_Pphi)
(R1_Atheta, R1_Pphi)
(R2_Atheta, R2_Pphi)
```

五个参数对全部唯一，不能相同。

English:  
The nonperiodic dataset does not enumerate all five-cell combinations. Every periodic sample `(Atheta=a, Pphi=p)` has `K=5` corresponding nonperiodic five-cell windows:

```text
[L2, L1, C, R1, R2]
```

The center cell is fixed as:

```text
C_Atheta = a
C_Pphi   = p
```

The four neighbor cells `L2/L1/R1/R2` are randomly drawn from the same discrete parameter grid and must satisfy:

```text
(L2_Atheta, L2_Pphi)
(L1_Atheta, L1_Pphi)
(C_Atheta,  C_Pphi)
(R1_Atheta, R1_Pphi)
(R2_Atheta, R2_Pphi)
```

All five parameter pairs must be unique. In addition, all five `Atheta` values must be unique and all five `Pphi` values must be unique. Each nonperiodic row also records `perturbation_tier = low/medium/high` based on neighborhood perturbation strength.

## 5. 输出文件 / Artifacts

| 文件 / File | 说明 / Description |
| --- | --- |
| `configs/sampling_pilot.json` | 新采样配置 / New sampling configuration |
| `scripts/generate_pilot_samples.py` | 采样表生成脚本 / Sampling manifest generator |
| `data/periodic_full_grid.csv` | `11011` 条周期单元全网格样本 / `11011` periodic unit-cell full-grid samples |
| `data/nonperiodic_center_matched_samples.csv` | `55055` 条中心匹配非周期五单元窗口样本 / `55055` center-matched nonperiodic five-cell window samples |
| `data/micro_loop_candidates.csv` | 从新非周期样本中抽取的 CST 小闭环候选 / CST micro-loop candidates selected from the new nonperiodic samples |
| `data/cst_micro_loop_queue.csv` | 小闭环 CST 任务队列 / CST micro-loop task queue |

## 6. 执行命令 / Command

```powershell
D:\software\anaconda\envs\cst\python.exe E:\aris\meta\cst_coupling_model1\scripts\generate_pilot_samples.py
```
