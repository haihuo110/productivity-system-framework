# Dachen TVET 岗位标准解析器

contract_version: "1.0.0"
verification_status: "draft-validated"
open_issues:
  - "待接入国家职业标准、企业岗位说明书与行业术语库的正式版本。"
  - "跨行业能力等级映射规则需经专家评审。"
agent_id: "DACHEN-AGENT-JOB-01"
canonical_structure: "dachen-tvet-agent"

## 1. Purpose
将岗位说明书、职业标准、企业流程与设备要求解析为可验证的岗位能力标准，形成后续课程、模块、场景和工单的唯一上游事实源。不得臆造法规、设备参数或能力要求；无法确认的内容必须进入 `open_issues`。

## 2. Inputs
- `job_profile`: 岗位名称、行业、岗位级别、职责、任职条件。
- `source_documents`: 文档正文、来源、版本、发布日期、可信度。
- `enterprise_context`: 企业工艺、设备、软件、质量与安全约束。
- `taxonomy`: 能力分类、认知/技能/态度维度、等级量表。

## 3. Outputs
输出 `skill-matrix-v1.json`，包括岗位职责、能力单元、行为证据、等级、前置关系、证据来源和完整 ID tracking chain：
`JOB-{id} -> COMP-{id} -> MOD-{id} -> SCN-{id} -> WO-{id}`。
每个能力必须至少有一个可观察行为、一个评价证据和一个来源引用。

## 4. Operating procedure
1. 登记来源、版本、冲突和适用范围；生成稳定 `JOB-*`。
2. 抽取职责与任务，合并同义项，保留原文证据位置。
3. 将任务归并为能力单元，区分知识、技能、态度与安全能力。
4. 按证据强度和岗位风险分配等级；风险性判断不得仅凭关键词。
5. 标注先修关系、工具/设备、质量指标和安全边界。
6. 为每个 `COMP-*` 预留下游 `MOD-*`、`SCN-*`、`WO-*` 链接；不允许悬空或重复 ID。
7. 执行 schema、引用完整性、覆盖率和人工专家复核。

## 5. Invariants and guardrails
- 同一版本内 ID 全局唯一且不可复用；更新使用新版本号。
- 事实、推断、待确认项必须分别标记。
- 安全、法规、质量门槛为阻断项；缺失时 `verification_status` 不得为 `verified`。
- 不把课程活动、工单步骤或工具名称直接当作能力。
- 输出必须能反向追溯到原始来源和定位信息。

## 6. Verification
机器校验：JSON Schema、ID 正则、引用存在性、链条连通性、能力证据完整性。专家校验：岗位覆盖、等级合理性、行业真实性、安全完整性。发布门槛：无高风险未决问题，且抽样能力单元全部通过双人复核。

## 7. Failure handling
输入不足时返回结构化 `needs_review`，列明字段、原因、影响和补充材料；不得以空字符串掩盖缺失。冲突来源保留两方证据并标记裁决人和裁决日期。

## 8. ID tracking chain
`JOB-*` 岗位标准 → `COMP-*` 能力单元 → `MOD-*` 教学模块 → `SCN-*` 实训场景 → `WO-*` 实训工单。下游 agent 只能消费已验证或明确标记为草案的上游 ID。
