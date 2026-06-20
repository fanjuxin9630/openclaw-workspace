# 🧠 记忆系统说明

## 结构

```
memory/
├── README.md           ← 本文件，记忆使用说明
├── YYYY-MM-DD.md       ← 每日工作日志（原始）
├── bounty-records/     ← Bounty任务存档
├── communications/     ← 客户沟通记录
└── reviews/            ← 复盘/总结
```

## 读取顺序（每次session启动）

1. `MEMORY.md` — 长期记忆，核心事实
2. `memory/YYYY-MM-DD.md` — 最近几天日志
3. `strategy/current.md` — 当前策略和待办

## 规则

- 每次重要事件立即写入当日日志
- 每周清理一次老旧daily log，精华提炼入MEMORY.md
- 所有PR/操作记录必须可回溯
