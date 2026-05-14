# grid_05506_np_r04 尖跳复现性记录 / Spike Reproducibility Note

## 中文

样本：`grid_05506_np_r04`

目标通道：`1D Results\S-Parameters\SZmax(2),Zmin(1)`

结论：

- 原始非周期五单元曲线的主要尖跳不是单次导出错误。`repeat01` 完整重跑后，主要尖跳频点大体复现。
- 原始曲线与重复曲线的相邻幅度跳变相关系数为 `0.858689`。
- 原始最大尖跳位于 `8.286-8.304 GHz`，幅度跳变为 `0.330222`；重复运行同一频段跳变为 `0.253345`。
- `7.980-7.998 GHz`、`9.366-9.384 GHz`、`9.384-9.402 GHz`、`9.834-9.852 GHz` 等频段也在重复运行中保持明显跳变。
- 多通道检查显示，目标通道的大幅度尖跳没有在其它所有 S 参数幅度中等幅同步出现；但同输出/同入射相关通道的相位跳变常在相同频点附近同步出现。
- 这说明尖跳更像是该非周期五单元结构在目标通道上的快速频率响应/插值敏感区域，而不是简单的 CSV 导出错误。

本次重复求解耗时较长的原因：

- CST 执行了完整 `DeleteResults()` 后重算。
- 频段为 `6-24 GHz`，最终线性输出 `1001` 点。
- 求解器为 interpolative broadband sweep，实际计算了 `105` 个频率样本。
- 每个频率样本包含 `Zmin/Zmax` 双端口、mode 1/mode 2，共四组激励/模式求解。
- 最终网格约 `79,866` 个单元、`526,686` 个自由度。
- CST 日志记录总求解时间为 `15702 s`，即 `4 h 21 m 42 s`。

后续建议：

- 不建议立刻全带重跑 `same_center_repeat01`，成本较高。
- 建议围绕尖跳频段做窄频段固定采样/更高精度验证，例如 `7.8-8.4 GHz`、`9.2-9.9 GHz`、`20.3-22.4 GHz`。
- 若窄频段高精度结果仍复现尖跳，可把这些频段标记为强耦合/快速响应区域，并在后续模型训练中单独处理。

## English

Sample: `grid_05506_np_r04`

Target channel: `1D Results\S-Parameters\SZmax(2),Zmin(1)`

Conclusion:

- The major spikes in the original nonperiodic five-cell curve are not a one-off export error. After a full `repeat01` rerun, the major spike locations are broadly reproduced.
- The adjacent-point magnitude-jump correlation between the original curve and the repeated curve is `0.858689`.
- The largest original spike is at `8.286-8.304 GHz`, with a magnitude jump of `0.330222`; the repeated run shows a jump of `0.253345` in the same interval.
- The intervals `7.980-7.998 GHz`, `9.366-9.384 GHz`, `9.384-9.402 GHz`, and `9.834-9.852 GHz` also remain strongly jump-like in the repeated run.
- Multi-channel probing shows that the target-channel magnitude spikes do not appear with equal amplitude across all other S-parameter magnitudes. However, phase jumps in related same-output/input channels often occur near the same frequencies.
- This suggests that the spikes are more likely fast target-channel frequency responses or interpolation-sensitive regions of the nonperiodic five-cell structure, rather than a simple CSV export artifact.

Why the repeated CST solve took long:

- CST recomputed from scratch after `DeleteResults()`.
- The sweep band was `6-24 GHz`, with `1001` final linear output points.
- The solver used an interpolative broadband sweep and actually calculated `105` frequency samples.
- Each frequency sample solved both `Zmin/Zmax` ports and mode 1/mode 2, i.e. four excitation/mode solves.
- The final mesh had about `79,866` cells and `526,686` degrees of freedom.
- The CST log reports a total solver time of `15702 s`, i.e. `4 h 21 m 42 s`.

Recommended next steps:

- Do not immediately rerun the full-band `same_center_repeat01`; it is expensive.
- Run narrow-band fixed-sampling or higher-accuracy verification around spike regions, for example `7.8-8.4 GHz`, `9.2-9.9 GHz`, and `20.3-22.4 GHz`.
- If the narrow-band high-accuracy runs still reproduce the spikes, mark those bands as strong-coupling/fast-response regions and handle them separately in later model training.

## Artifacts

- `reports/grid_05506_np_r04_sparam_spike_analysis.csv`
- `reports/grid_05506_np_r04_repeat01_reproducibility.csv`
- `data/processed/grid_05506_np_r04_target_phase.csv`
- `data/raw/nonperiodic/grid_05506_np_r04_repeat01_five_cell_szmax2_zmin1.csv`

## 窄频段固定采样验证 / Narrow-Band Fixed-Sampling Verification

中文：

- 已完成三段窄频段固定采样 CST 验证：`7.8-8.4 GHz`、`9.2-9.9 GHz`、`20.3-22.4 GHz`。
- 每段使用 `81` 个固定单频采样点，并导出目标通道 `SZmax(2),Zmin(1)`。
- `7.8-8.4 GHz`：窄频段最大跳变为 `0.215021`，位置约 `8.1225-8.1300 GHz`；原全带最大跳变 `8.295 GHz` 附近在窄频固定采样中变平滑，附近跳变仅 `0.001859`。
- `9.2-9.9 GHz`：窄频段在 `9.366-9.384 GHz` 附近仍有明显跳变，靠近原全带 `9.375 GHz` 尖跳，窄频附近跳变为 `0.136810`。
- `20.3-22.4 GHz`：窄频段存在明显跳变，最大跳变为 `0.261610`，位置约 `20.5363-20.5625 GHz`；原 `20.427 GHz` 附近仍有中等跳变 `0.135692`。
- 初步解释：尖跳不是简单 CSV 导出错误；但部分全带尖跳位置受 CST 自动插值/宽带采样策略影响。后续建模时应把这些频段作为快速响应区域单独标记，而不是把所有相邻点尖跳都直接当作同一类真实物理突变。

English:

- Completed three narrow-band fixed-sampling CST verification runs: `7.8-8.4 GHz`, `9.2-9.9 GHz`, and `20.3-22.4 GHz`.
- Each band used `81` fixed single-frequency samples and exported the target channel `SZmax(2),Zmin(1)`.
- `7.8-8.4 GHz`: the largest narrow-band jump is `0.215021` at about `8.1225-8.1300 GHz`; the original full-band top spike near `8.295 GHz` becomes smooth under narrow fixed sampling, with a nearby jump of only `0.001859`.
- `9.2-9.9 GHz`: a strong jump remains near `9.366-9.384 GHz`, close to the original full-band `9.375 GHz` spike, with a nearby narrow-band jump of `0.136810`.
- `20.3-22.4 GHz`: strong narrow-band jumps are present. The largest jump is `0.261610` at about `20.5363-20.5625 GHz`; the original `20.427 GHz` neighborhood still has a moderate jump of `0.135692`.
- Initial interpretation: the spikes are not simple CSV export errors, but some full-band spike locations are affected by CST automatic interpolation/broadband sampling. These regions should be flagged as fast-response bands for later modeling rather than treating every adjacent-point spike as the same kind of physical discontinuity.

Additional artifacts:

- `reports/grid_05506_np_r04_narrowband_verification_summary.csv`
- `reports/grid_05506_np_r04_narrowband_verification_points.csv`
- `reports/figures/grid_05506_np_r04_narrowband_verification.pdf`
- `data/raw/nonperiodic/grid_05506_np_r04_nb_7p8_8p4_szmax2_zmin1.csv`
- `data/raw/nonperiodic/grid_05506_np_r04_nb_9p2_9p9_szmax2_zmin1.csv`
- `data/raw/nonperiodic/grid_05506_np_r04_nb_20p3_22p4_szmax2_zmin1.csv`
