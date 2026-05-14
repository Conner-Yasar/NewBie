# ARIS 工作流差距分析 / ARIS Workflow Gap Analysis

创建日期：2026-05-13  
Created: 2026-05-13

## 1. 结论摘要 / Executive Summary

中文：  
当前 `ARIS_WORKFLOW.md` 的方向是对的：它把本任务约束为证据驱动、可复现、只在 `E:\aris\meta` 下落盘的研究闭环。但它与 GitHub 上的 `Auto-claude-code-research-in-sleep` 原始 ARIS 方法相比，还有几个关键差距：缺少标准 artifact contract、缺少 claim map、缺少独立 reviewer / audit gate、缺少 session recovery 入口、缺少 experiment log 与 result-to-claim 的机器可读接口。

English:  
The current `ARIS_WORKFLOW.md` is directionally correct: it constrains this task as an evidence-driven, reproducible research loop that writes only under `E:\aris\meta`. Compared with the upstream `Auto-claude-code-research-in-sleep` ARIS methodology, however, it still has several important gaps: no standard artifact contract, no claim map, no independent reviewer/audit gate, no session recovery entry point, and no machine-readable interfaces for experiment logs and result-to-claim.

## 2. 上游 ARIS 的核心原则 / Core Principles in Upstream ARIS

中文：  
上游 ARIS 的重点不是“一个目录规范”，而是由 Markdown skills 串起来的科研生命周期。它强调：

English:  
Upstream ARIS is not mainly a directory convention; it is a research lifecycle stitched together by Markdown skills. It emphasizes:

- 方法论而非平台 / Methodology, not platform.
- Markdown-only artifact contracts / Markdown-only artifact contracts.
- 跨模型执行-审查分离 / Cross-model executor-reviewer separation.
- 实验计划、实验日志、结果到结论之间的文件接口 / File interfaces between experiment plan, experiment log, and result-to-claim.
- reviewer independence：审查者直接看文件，不接收执行者摘要 / Reviewer independence: reviewers inspect files directly rather than receiving executor summaries.
- experiment integrity：执行者不能审判自己的实验诚实度 / Experiment integrity: the executor must not judge its own evaluation integrity.

## 3. 当前文档的问题 / Problems in the Current Workflow Document

### 问题 1：缺少标准 Artifact Contract / Missing Standard Artifact Contract

中文：  
当前文档有阶段门，但没有定义固定文件名。例如上游 ARIS 使用 `EXPERIMENT_PLAN.md`、`EXPERIMENT_LOG.md`、`EXPERIMENT_AUDIT.md/.json`、`NARRATIVE_REPORT.md` 等作为技能之间的接口。我们现在只有泛化的 `reports/*.md`，后续 agent 可能不知道哪个文件是权威入口。

English:  
The current document has phase gates but does not define fixed artifact names. Upstream ARIS uses files such as `EXPERIMENT_PLAN.md`, `EXPERIMENT_LOG.md`, `EXPERIMENT_AUDIT.md/.json`, and `NARRATIVE_REPORT.md` as interfaces between skills. Our current workflow only has generic `reports/*.md`, so future agents may not know which file is authoritative.

建议 / Recommendation:

- 增加 `EXPERIMENT_PLAN.md`、`EXPERIMENT_LOG.md`、`DATASET_CARD.md`、`MODEL_REPORT.md`、`OPTIMIZATION_REPORT.md`、`RESULT_TO_CLAIM.md`。
- Add `EXPERIMENT_PLAN.md`, `EXPERIMENT_LOG.md`, `DATASET_CARD.md`, `MODEL_REPORT.md`, `OPTIMIZATION_REPORT.md`, and `RESULT_TO_CLAIM.md`.

### 问题 2：缺少 Claim Map / Missing Claim Map

中文：  
当前目标写了“证明能减弱耦合效应”，但没有把它拆成 claim 与最低证据。ARIS 的实验计划模板要求每个 claim 对应 minimum convincing evidence。没有 claim map，后续很容易只跑出数据，却不知道能支撑什么结论。

English:  
The current goal says “prove the coupling effect can be reduced,” but it does not decompose this into claims and minimum evidence. The ARIS experiment plan template requires each claim to have minimum convincing evidence. Without a claim map, we may produce data without knowing what conclusion it supports.

建议 / Recommendation:

- C1：预测模型能从 5 单元角度输入预测耦合标签。
- C2：优化能找到比原始/随机配置更低耦合的角度组合。
- C3：优化结果经 CST 复验后仍成立。
- C1: The predictor can predict the coupling label from five-cell angle inputs.
- C2: Optimization can find angle combinations with lower coupling than original/random configurations.
- C3: The optimized result remains valid after CST re-verification.

### 问题 3：缺少独立审查门 / Missing Independent Review Gates

中文：  
上游 ARIS 明确强调 executor 与 reviewer 分离，尤其是实验诚实度不能由执行者自己审判。当前文档只写了“证据优先”，但没有强制 `experiment-audit` 或 `result-to-claim` 阶段。

English:  
Upstream ARIS explicitly separates executor and reviewer, especially for experiment integrity. The current document says “evidence first” but does not require `experiment-audit` or `result-to-claim` gates.

建议 / Recommendation:

- Pilot 后运行实验审计 / Run experiment audit after the pilot.
- Full 数据集后运行数据集审计 / Run dataset audit after the full dataset.
- 优化后运行 result-to-claim / Run result-to-claim after optimization.

### 问题 4：没有 Session Recovery 入口 / No Session Recovery Entry Point

中文：  
上游模板有 focused contract 的思想：新会话不要读所有历史，而是读一个聚焦的研究契约。当前任务没有 `RESEARCH_CONTRACT.md`，长任务压缩后容易丢失目标、范围和当前阶段。

English:  
Upstream templates use the idea of a focused contract: new sessions should not read all history, but a focused research contract. This task currently lacks `RESEARCH_CONTRACT.md`, so long sessions may lose goal, scope, and current phase after compaction.

建议 / Recommendation:

- 新建 `RESEARCH_CONTRACT.md`，作为恢复入口。
- Create `RESEARCH_CONTRACT.md` as the recovery entry point.

### 问题 5：CST 仿真不是典型 ML 实验，需要专门适配 / CST Simulation Needs Domain-Specific Adaptation

中文：  
上游 ARIS 很多默认假设来自 ML/GPU 实验，例如 seed、训练曲线、GPU queue。CST 任务的瓶颈是商业软件自动化、许可证、参数化几何、结果导出和失败恢复。因此不能照搬 `/run-experiment` 或 `/experiment-queue` 的 GPU 语义。

English:  
Many upstream ARIS defaults come from ML/GPU experiments, such as seeds, training curves, and GPU queues. The bottlenecks in this CST task are commercial software automation, licensing, parametric geometry, result export, and failure recovery. Therefore, `/run-experiment` or `/experiment-queue` GPU semantics should not be copied blindly.

建议 / Recommendation:

- 把 CST batch 视为 domain-specific experiment runner。
- Treat CST batch execution as a domain-specific experiment runner.
- 保留 ARIS artifact contract，但执行器用 CST COM/CLI 脚本实现。
- Preserve the ARIS artifact contract, but implement the runner through CST COM/CLI scripts.

### 问题 6：成功标准还不够可审计 / Success Criteria Are Not Auditable Enough

中文：  
当前成功标准说“优于均值预测基线”和“至少一组显示下降”，但没有定义具体阈值、对照组、统计方式和失败样本处理。

English:  
The current success criteria say “beats mean baseline” and “shows reduced coupling in at least one group,” but do not define thresholds, controls, statistics, or failed-sample handling.

建议 / Recommendation:

- 预测模型：报告 MAE/RMSE/R2，并与 mean baseline 比较。
- 优化：至少 `N` 个代表性邻域中，CST 复验后中位耦合下降。
- 失败：明确 CST 求解失败、导出失败、异常曲线的剔除规则。
- Predictor: report MAE/RMSE/R2 and compare with mean baseline.
- Optimization: show median coupling reduction after CST re-verification across at least `N` representative neighborhoods.
- Failures: define exclusion rules for CST solve failures, export failures, and abnormal curves.

## 4. 修正优先级 / Fix Priority

| 优先级 / Priority | 修正 / Fix |
| --- | --- |
| P0 | 添加 `RESEARCH_CONTRACT.md`，作为会话恢复与唯一当前真相入口 / Add `RESEARCH_CONTRACT.md` as session recovery and source-of-truth entry |
| P0 | 添加 `EXPERIMENT_PLAN.md`，包含 claim map 与实验块 / Add `EXPERIMENT_PLAN.md` with claim map and experiment blocks |
| P1 | 添加 `EXPERIMENT_LOG.md` 模板 / Add `EXPERIMENT_LOG.md` template |
| P1 | 添加 `DATASET_CARD.md` 模板 / Add `DATASET_CARD.md` template |
| P1 | 在 `ARIS_WORKFLOW.md` 中加入 reviewer independence 与 audit gates / Add reviewer independence and audit gates to `ARIS_WORKFLOW.md` |
| P2 | 后续再接入 `analyze-results`、`experiment-audit`、`result-to-claim` / Later integrate `analyze-results`, `experiment-audit`, and `result-to-claim` |

## 5. 总体判断 / Overall Verdict

中文：  
当前工作流文档可以作为项目说明，但还不能算严格 ARIS workflow。它缺的是 ARIS 最关键的“文件合约 + 独立审查 + claim-driven 实验”三件事。补齐后，它就能很好地适配 CST 耦合效应任务。

English:  
The current workflow document is usable as a project description, but it is not yet a strict ARIS workflow. It lacks the three most important ARIS elements: file contracts, independent review, and claim-driven experiments. Once these are added, it will fit the CST coupling-effect task well.
