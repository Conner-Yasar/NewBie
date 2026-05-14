# 曲线与同参数对照检查 / Curve and Same-Parameter Control Check

创建日期：2026-05-13  
Created: 2026-05-13

## 1. 目的 / Purpose

中文：  
本检查用于判断 `pilot_0070` 的大耦合标签是否来自真实五单元非周期差异，还是来自五单元超胞边界/端口设置。

English:  
This check tests whether the large `pilot_0070` coupling label comes from true five-cell nonperiodic differences or from the five-cell supercell boundary/port setup.

## 2. 曲线对比 / Curve Comparison

中文：  
先绘制周期基准与五单元非周期响应曲线，查看差异是全频段存在还是局部异常。

English:  
First plot the periodic baseline and five-cell nonperiodic response curves to see whether the difference is broadband or localized.

脚本 / Script:

```text
E:\aris\meta\cst_coupling_model1\scripts\plot_response_comparison.py
```

## 3. 同参数对照 / Same-Parameter Control

中文：  
对照样本命名为 `pilot_0070_same_center`。它使用与 `pilot_0070` 中心单元相同的参数，并复制到 `[L2, L1, C, R1, R2]` 五个单元：

English:  
The control sample is named `pilot_0070_same_center`. It uses the same parameters as the `pilot_0070` center cell and copies them to all five cells `[L2, L1, C, R1, R2]`:

```text
Atheta = -42.086534
Pphi   = 110.663698
```

中文：  
如果该对照样本仍然与周期基准差异很大，则说明当前五单元超胞边界/端口设置本身可能引入显著差异。

English:  
If this control sample still differs strongly from the periodic baseline, the current five-cell supercell boundary/port setup may itself be introducing a significant difference.

## 4. 结果 / Result

中文：  
曲线图和统计摘要已经生成：

English:  
The curve plots and summary tables have been generated:

```text
reports/figures/pilot_0070_periodic_vs_five_cell.svg
reports/figures/pilot_0070_periodic_vs_same_center_control.svg
reports/pilot_0070_curve_summary.csv
reports/pilot_0070_same_center_curve_summary.csv
```

标签结果 / Label results:

```text
pilot_0070 five-cell nonperiodic:
  coupling_label_6_24ghz = 0.5229127991565287

pilot_0070_same_center control:
  coupling_label_6_24ghz = 0.8949670486897399
```

中文：  
同参数对照样本的差异比真实非周期样本更大，说明当前比较口径还不能证明“邻域非周期性导致耦合”。更可能的问题是：五单元超胞模型与单元周期基准模型的边界、端口归一化或超胞模式定义不一致。下一步应先建立“五单元同参数超胞基准”或调整有限阵列边界，再计算非周期扰动标签。

English:  
The same-parameter control differs from the periodic baseline even more than the true nonperiodic sample. This means the current comparison cannot yet prove that neighborhood nonperiodicity causes the coupling. The more likely issue is an inconsistency between the five-cell supercell model and the unit-cell periodic baseline in boundary conditions, port normalization, or supercell mode definition. The next step should be to build a five-cell same-parameter supercell baseline or adjust the finite-array boundary before computing the nonperiodic perturbation label.

## 5. 修正标签 / Corrected Label

中文：  
主标签已修正为“非周期五单元超胞”相对于“同中心参数五单元超胞基准”的平均幅值绝对差：

English:  
The primary label has been corrected to the mean absolute magnitude difference between the nonperiodic five-cell supercell and the same-center five-cell supercell baseline:

```text
coupling = mean_f |S_five_cell_nonperiodic(f) - S_five_cell_same_center(f)|, f in [6, 24] GHz
```

`pilot_0070` corrected result:

```text
frequency_points: 1001
frequency_min_ghz: 6.0
frequency_max_ghz: 24.0
coupling_label_6_24ghz: 0.37355874533438677
max_abs_difference: 0.9766716529407773
baseline_mean_magnitude: 0.8965608104437428
comparison_mean_magnitude: 0.5245065609105323
```

产物 / Artifacts:

```text
data/processed/pilot_0070_corrected_label.csv
data/processed/pilot_0070_corrected_label.json
reports/figures/pilot_0070_corrected_same_center_vs_nonperiodic.svg
reports/pilot_0070_corrected_curve_summary.csv
```
