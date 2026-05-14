# 非周期五单元几何构建 / Nonperiodic Five-Cell Geometry Build

创建日期：2026-05-13  
Created: 2026-05-13

## 1. 目标 / Goal

中文：  
将 `pilot_0070` 的 nonperiodic CST 工程从单元模板副本重建为真实包含 `[L2, L1, C, R1, R2]` 的五单元几何。

English:  
Rebuild the `pilot_0070` nonperiodic CST project from a unit-cell template copy into a true five-cell geometry containing `[L2, L1, C, R1, R2]`.

## 2. 已生成组件 / Generated Components

| 单元 / Cell | Component | x 位置 / x position |
| --- | --- | --- |
| `L2` | `np_L2` | `-12 mm` |
| `L1` | `np_L1` | `-6 mm` |
| `C` | `np_C` | `0 mm` |
| `R1` | `np_R1` | `6 mm` |
| `R2` | `np_R2` | `12 mm` |

中文：  
每个 component 使用该单元自己的 `Atheta/Pphi` 数值重建中心臂、延伸环、上下栅格、介质层和空气层。

English:  
Each component uses its own `Atheta/Pphi` values to rebuild the center arm, extension ring, upper/lower gratings, dielectric layers, and air layer.

## 3. 产物 / Artifacts

```text
E:\aris\meta\cst_coupling_model1\scripts\build_nonperiodic_five_cell.py
E:\aris\meta\cst_coupling_model1\cst_projects\nonperiodic\pilot_0070\build_nonperiodic_five_cell.bas
E:\aris\meta\cst_coupling_model1\cst_projects\nonperiodic\pilot_0070\model1.cst
```

## 4. 验证 / Verification

中文：  
`Model.mod` 和 `ModelHistory.json` 中均已出现 `build nonperiodic five-cell geometry` history，并包含 `np_L2`, `np_L1`, `np_C`, `np_R1`, `np_R2` 五个组件的创建记录。

English:  
Both `Model.mod` and `ModelHistory.json` now contain the `build nonperiodic five-cell geometry` history, including creation records for `np_L2`, `np_L1`, `np_C`, `np_R1`, and `np_R2`.

## 5. 仍需注意 / Remaining Caveat

中文：  
当前工程几何已经是五单元非周期结构，但边界和 Floquet 端口仍沿用原 unit-cell 模板。下一步需要验证并改造有限阵列边界/激励设置，然后再运行新的 CST 求解。旧的 `pilot_0070_szmax2_zmin1.csv` 是几何重建前的模板导出，不应作为新几何结果。

English:  
The geometry is now a five-cell nonperiodic structure, but the boundaries and Floquet ports still follow the original unit-cell template. The next step is to validate and convert the finite-array boundary/excitation setup before running a new CST solve. The old `pilot_0070_szmax2_zmin1.csv` was exported before the geometry rebuild and must not be treated as the new-geometry result.
