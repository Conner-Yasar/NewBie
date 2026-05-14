# CST 小闭环工程准备 / CST Micro-Loop Project Preparation

创建日期：2026-05-13  
Created: 2026-05-13

## 1. 目标 / Goal

中文：  
根据 `data/cst_micro_loop_queue.csv`，为 3 条小闭环候选分别准备周期和非周期 CST 工程副本，并尝试对第一条样本执行 `SZmax(2),Zmin(1)` 导出。

English:  
Prepare periodic and nonperiodic CST project copies for the 3 micro-loop candidates listed in `data/cst_micro_loop_queue.csv`, then attempt `SZmax(2),Zmin(1)` export for the first sample.

## 2. 工程副本边界 / Project-Copy Boundary

中文：  
所有工程副本都放在 `E:\aris\meta\cst_coupling_model1\cst_projects` 下，不修改导师提供的标准模型 `E:\aris\模型1`。当前副本来源是已验证可导出的 ASCII 路径工程：

English:  
All project copies are stored under `E:\aris\meta\cst_coupling_model1\cst_projects`; the advisor-provided standard model `E:\aris\模型1` is not modified. The current copy source is the verified ASCII-path project:

```text
E:\aris\meta\cst_coupling_model1\cst_projects\export_probe_ascii
```

## 3. 当前状态 / Current Status

中文：  
周期工程副本可以作为周期单元模板，并写入中心单元 `C_Atheta/C_Pphi` 参数。非周期工程副本已经写入五单元参数元数据，但还没有完成五单元几何拼接，因此不能把当前 nonperiodic 副本导出的结果当作真实非周期物理结果。

English:  
The periodic project copy can serve as the periodic unit-cell template and stores the center-cell `C_Atheta/C_Pphi` parameters. The nonperiodic project copy stores the five-cell parameter metadata, but the five-cell geometry has not yet been assembled. Therefore, exports from the current nonperiodic copy must not be treated as physically valid nonperiodic results.

## 4. 脚本 / Script

```text
E:\aris\meta\cst_coupling_model1\scripts\prepare_cst_micro_loop_projects.py
```

中文：  
脚本会生成：

English:  
The script generates:

```text
E:\aris\meta\cst_coupling_model1\data\cst_micro_loop_queue_prepared.csv
```

## 5. 第一条导出验证 / First Export Verification

中文：  
`pilot_0070` 的周期模板副本和非周期模板副本都已经成功导出 `SZmax(2),Zmin(1)` 曲线：

English:  
Both the periodic and nonperiodic template copies for `pilot_0070` have successfully exported the `SZmax(2),Zmin(1)` curve:

```text
data/raw/periodic/pilot_0070_szmax2_zmin1.csv
data/raw/nonperiodic/pilot_0070_szmax2_zmin1.csv
data/processed/pilot_0070_label.csv
data/processed/pilot_0070_label.json
```

验证结果 / Verification result:

```text
frequency_points: 1001
frequency_min_ghz: 6.0
frequency_max_ghz: 24.0
coupling_label_6_24ghz: 0.0
```

中文：  
由于当前 nonperiodic 工程仍是标准单元模板副本，`0.0` 只说明“复制工程 -> 导出曲线 -> 计算标签”的流程打通，不说明非周期耦合为零。

English:  
Because the current nonperiodic project is still a standard unit-cell template copy, `0.0` only means that the workflow "copy project -> export curve -> compute label" works. It does not mean that the true nonperiodic coupling is zero.
