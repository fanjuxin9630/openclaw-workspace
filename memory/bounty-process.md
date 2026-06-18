# 💰 运财鼠 Bounty 接单流程 V1.0

> 虚无大人指导的收款与交付流程，2026-06-18 制定

---

## 🏗️ 核心流程

```
客户发任务 → 评估可行性 → 报价 + 收定金(30-50%) → 开工
     ↓
完工 → 提交成果（邮件/Slack/GitHub）→ 收尾款 → 交付凭证归档
```

---

## 📋 具体操作

### 1. 任务评估
- 阅读需求，评估工作量（简单/中等/困难）
- 确认技术栈是否在能力范围内
- 预估时间成本

### 2. 报价与定金
- 报总价（USD），说明分两期付款
- **定金 30-50%**（通过 Stripe Invoice 收款）
- 收到定金后开始工作

### 3. 工作与交付
- 在 GitHub 上 Fork 或 Clone 任务仓库
- 编写代码、测试、生成交付物
- 定期向客户更新进度

### 4. 完工与尾款
- 提交最终成果（GitHub PR / 邮件附件 / 文档）
- **发送 Stripe Invoice 收取尾款**（50-70%）
- 确认到账后，PR merge / 交付完成

### 5. 凭证归档
- 每个任务在 `memory/bounty-records/` 下存档
- 记录：任务名称、金额、客户、PR链接、支付状态

---

## 💳 收款方式（按优先级）

| 优先级 | 方式 | 说明 |
|---|---|---|
| 🥇 | **Stripe Invoicing** | 标准账单，发邮件给客户付款（信用卡/ACH） |
| 🥈 | 加密货币 (USDT) | Gitcoin 类平台默认用这个 |
| 🥉 | 支付宝/微信 | 国内客户专用 |

---

## 📎 交付凭证存档

每个任务完成后，在本目录下创建记录文件：

```
memory/bounty-records/
├── 2026-06-18_claude-changelog.md        ← 第一单
└── README.md                              ← 本流程文件的索引
```

---

## 📝 邮件交付模板

> **Subject:** [Delivery] Bounty #XXX - [Project Name] - Completed
>
> Hi [Client Name],
>
> I have completed the bounty task #[issue_number].
>
> **Deliverables:**
> - [PR Link / Attachment]
> - [Brief description]
>
> **Invoice:** [Stripe Invoice Link]
> **Amount Due:** $XXX (remaining 50-70%)
>
> Please review and let me know if any changes needed.
>
> Best,
> fanjuxin9630
