# pilot_0070 五单元求解结果 / pilot_0070 Five-Cell Solve Result

创建日期：2026-05-13  
Created: 2026-05-13

## 1. 设置 / Setup

中文：  
`pilot_0070` 的 nonperiodic 工程已经改造成五单元超胞 Floquet 设置：`x/y` 为 `unit cell`，`z` 为 `expanded open`，并启用 `Zmin/Zmax` 双向 Floquet 激励，以保留目标通道 `SZmax(2),Zmin(1)`。

English:  
The `pilot_0070` nonperiodic project was configured as a five-cell Floquet supercell: `x/y` are `unit cell`, `z` is `expanded open`, and both `Zmin/Zmax` Floquet excitations are enabled to preserve the target channel `SZmax(2),Zmin(1)`.

## 2. 新结果 / New Results

```text
E:\aris\meta\cst_coupling_model1\data\raw\nonperiodic\pilot_0070_five_cell_szmax2_zmin1.csv
E:\aris\meta\cst_coupling_model1\data\processed\pilot_0070_five_cell_label.csv
E:\aris\meta\cst_coupling_model1\data\processed\pilot_0070_five_cell_label.json
```

验证结果 / Verification result:

```text
response_channel: SZmax(2),Zmin(1)
frequency_points: 1001
frequency_min_ghz: 6.0
frequency_max_ghz: 24.0
coupling_label_6_24ghz: 0.5229127991565287
max_abs_difference: 0.9987223167471379
periodic_mean_magnitude: 0.0015937617540040562
nonperiodic_mean_magnitude: 0.5245065609105323
```

## 3. 旧结果不可用 / Old Result Is Not Valid

中文：  
旧文件 `data/raw/nonperiodic/pilot_0070_szmax2_zmin1.csv` 是五单元几何重建前的模板副本导出，不代表真实非周期五单元结果。后续应使用 `pilot_0070_five_cell_szmax2_zmin1.csv`。

English:  
The old file `data/raw/nonperiodic/pilot_0070_szmax2_zmin1.csv` was exported from the template copy before the five-cell geometry rebuild. It does not represent the true nonperiodic five-cell result. Use `pilot_0070_five_cell_szmax2_zmin1.csv` going forward.

## 4. 进程状态 / Process Status

中文：  
结果已经成功导出并计算标签，但 CST 仍报告 solver 进程在后台响应/收尾。已尝试通过 CST 官方接口优雅停止，但调用未及时返回。不要重复启动同一工程的新求解，直到该进程结束或手动确认关闭。

English:  
The result was exported and labeled successfully, but CST still reports a responsive solver process in the background. A graceful stop through the CST interface was attempted, but the call did not return in time. Do not start another solve for the same project until this process exits or is manually confirmed closed.
