# CST 结果导出接口说明 / CST Result Export Interface

创建日期：2026-05-13  
Created: 2026-05-13

## 1. 结论 / Conclusion

中文：  
`SZmax(2),Zmin(1)` 的自动导出入口已确认。最稳妥的方式不是 GUI 宏，也不是直接解析 `.sig` 文件，而是使用 CST 官方 Python 结果接口：

English:  
The automatic export entry for `SZmax(2),Zmin(1)` has been confirmed. The most robust approach is not a GUI macro or direct `.sig` parsing, but the official CST Python result interface:

```python
import cst.results as results
project = results.ProjectFile("path/to/project.cst", allow_interactive=True)
result_3d = project.get_3d()
item = result_3d.get_result_item(r"1D Results\S-Parameters\SZmax(2),Zmin(1)")
data = item.get_data()
```

## 2. Python 环境 / Python Environment

中文：  
CST Python 库支持 Python 3.8/3.9/3.10/3.11/3.12。本机可用环境为：

English:  
The CST Python library supports Python 3.8/3.9/3.10/3.11/3.12. The usable local environment is:

```text
D:\software\anaconda\envs\cst\python.exe
```

需要加入 / Required paths:

```text
PYTHONPATH = D:\software\CST Studio Suite\AMD64\python_cst_libraries
PATH      += D:\software\CST Studio Suite\AMD64
```

## 3. 目标结果路径 / Target Result Path

中文：  
主响应通道的结果树路径为：

English:  
The result-tree path for the primary response channel is:

```text
1D Results\S-Parameters\SZmax(2),Zmin(1)
```

此外，已有工程中还存在多个历史参数扫描节点，例如：

English:
The existing project also contains historical parameter-sweep nodes, for example:

```text
1D Results\Pphi-Atheta=-45\SZmax(2),Zmin(1)_(Pphi=110)
1D Results\Atheta-Pphi=110\SZmax(2),Zmin(1)_(Atheta=-90)
```

## 4. 已验证脚本 / Verified Script

中文：  
已创建并验证如下脚本：

English:  
The following script has been created and verified:

```text
E:\aris\meta\cst_coupling_model1\scripts\export_cst_1d_result.py
```

示例命令 / Example command:

```powershell
D:\software\anaconda\envs\cst\python.exe `
  E:\aris\meta\cst_coupling_model1\scripts\export_cst_1d_result.py `
  --project E:\aris\meta\cst_coupling_model1\cst_projects\export_probe_ascii\model1.cst `
  --output E:\aris\meta\cst_coupling_model1\data\raw\periodic\model1_szmax2_zmin1_export_test.csv
```

## 5. 验证结果 / Verification Result

中文：  
导出的测试 CSV 为：

English:  
The exported test CSV is:

```text
E:\aris\meta\cst_coupling_model1\data\raw\periodic\model1_szmax2_zmin1_export_test.csv
```

结果摘要 / Result summary:

| 项目 / Item | 值 / Value |
| --- | --- |
| 数据点 / Points | 1001 |
| 最小频率 / Minimum frequency | 6.0 GHz |
| 最大频率 / Maximum frequency | 24.0 GHz |
| 最小幅值 / Minimum magnitude | 0.00044380303209089694 |
| 最大幅值 / Maximum magnitude | 0.002010264963941081 |

## 6. 重要发现 / Important Finding

中文：  
当前标准模型中已保存的 `SZmax(2),Zmin(1)` 主结果覆盖 `6.0-24.0 GHz`。用户已确认耦合标签按可用频段 `6-24 GHz` 计算。后续每次新仿真/导出都必须显式检查曲线是否至少覆盖该标签频段；超出该范围的点可以保留，但不参与主标签计算。

English:  
The currently saved primary `SZmax(2),Zmin(1)` result in the standard model covers `6.0-24.0 GHz`. The user has confirmed that the coupling label must be computed over the available `6-24 GHz` band. Every later simulation/export must explicitly verify that the curve at least covers this label band. Points outside this range may be retained, but they are not used in the primary label.

## 7. 不推荐入口 / Non-Preferred Entries

中文：  
本次测试也尝试过 `RunScript`、`RunMacro`、`AddToHistory` 和 CLI `--b Model.run`。这些路径在当前环境下不如 `cst.results.ProjectFile` 稳定，暂不作为数据集导出的主路径。

English:  
`RunScript`, `RunMacro`, `AddToHistory`, and CLI `--b Model.run` were also tested. In the current environment, these paths are less stable than `cst.results.ProjectFile`, so they should not be the primary dataset-export path for now.
