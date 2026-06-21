#!/usr/bin/env python3
"""
🐭 运财鼠成本追踪器 v1.0
数据来源：OpenClaw 会话日志 + DeepSeek 定价
方法论：从原始日志解析实际 Token 用量，按官方定价计算
"""
import json, os, datetime, sys

# 定价（来源：DeepSeek 官方平台）
PRICING = {
    "deepseek-v4-flash": {
        "input": 0.14,       # $/M tokens
        "output": 0.28,      # $/M tokens
        "cache_read": 0.028, # $/M tokens
        "cache_write": 0.0,  # $/M tokens
    }
}

RATE = 7.3  # USD to CNY 参考汇率

def parse_trajectory(path):
    """从 trajectory 日志解析用量"""
    total_input = 0
    total_output = 0
    tool_calls = []
    timestamps = []
    
    if not os.path.exists(path):
        return {"error": f"文件不存在: {path}"}
    
    with open(path, 'r') as f:
        for line in f:
            try:
                d = json.loads(line)
                usage = d.get('usage', {})
                if isinstance(usage, dict):
                    total_input += usage.get('inputTokens', 0) or 0
                    total_output += usage.get('outputTokens', 0) or 0
                
                if 'invocation' in d:
                    tool_name = d.get('invocation', {}).get('function', {}).get('name', '')
                    tool_calls.append(tool_name)
                
                ts = d.get('timestamp', d.get('ts', ''))
                if ts:
                    timestamps.append(ts)
            except:
                pass
    
    return {
        "total_input_tokens": total_input,
        "total_output_tokens": total_output,
        "total_tool_calls": len(tool_calls),
        "tool_call_breakdown": {
            name: tool_calls.count(name) for name in set(tool_calls)
        } if tool_calls else {},
        "first_ts": timestamps[0] if timestamps else None,
        "last_ts": timestamps[-1] if timestamps else None,
    }

def calculate_cost(model, input_tokens, output_tokens):
    """按定价计算成本"""
    pricing = PRICING.get(model, PRICING["deepseek-v4-flash"])
    input_cost = (input_tokens / 1_000_000) * pricing["input"]
    output_cost = (output_tokens / 1_000_000) * pricing["output"]
    return input_cost + output_cost

def main():
    # 查找最新的 session
    sessions_dir = "/home/dify007/.openclaw/agents/main/sessions"
    latest_traj = None
    latest_time = 0
    
    for f in os.listdir(sessions_dir):
        if f.endswith(".trajectory.jsonl"):
            fp = os.path.join(sessions_dir, f)
            mtime = os.path.getmtime(fp)
            if mtime > latest_time:
                latest_time = mtime
                latest_traj = fp
    
    if not latest_traj:
        print("❌ 未找到 trajectory 文件")
        sys.exit(1)
    
    print(f"📊 分析文件: {os.path.basename(latest_traj)}")
    print(f"   文件修改时间: {datetime.datetime.fromtimestamp(latest_time)}")
    print()
    
    data = parse_trajectory(latest_traj)
    
    if "error" in data:
        print(f"❌ {data['error']}")
        sys.exit(1)
    
    total_tokens = data["total_input_tokens"] + data["total_output_tokens"]
    cost_usd = calculate_cost("deepseek-v4-flash", data["total_input_tokens"], data["total_output_tokens"])
    cost_cny = cost_usd * RATE
    
    print("=" * 60)
    print("🐭 运财鼠成本报告")
    print("  方法论：从原始日志直接解析Token用量")
    print("  数据源：OpenClaw trajectory 日志文件")
    print("  定价源：DeepSeek 官方平台")
    print("  置信度：高（从实际日志解析）")
    print("=" * 60)
    
    print(f"\n📈 Token 用量")
    print(f"  输入: {data['total_input_tokens']:,} tokens")
    print(f"  输出: {data['total_output_tokens']:,} tokens")
    print(f"  合计: {total_tokens:,} tokens")
    
    print(f"\n💰 费用（按官方定价）")
    print(f"  模型: deepseek-v4-flash")
    print(f"  输入: ${data['total_input_tokens']/1_000_000 * 0.14:.4f}")
    print(f"  输出: ${data['total_output_tokens']/1_000_000 * 0.28:.4f}")
    print(f"  API 总计: ${cost_usd:.4f} (¥{cost_cny:.2f})")
    
    print(f"\n🔧 工具调用 ({data['total_tool_calls']} 次)")
    for name, count in sorted(data['tool_call_breakdown'].items(), key=lambda x: -x[1]):
        print(f"  {name}: {count}次")
    
    if data['first_ts'] and data['last_ts']:
        print(f"\n⏱ 时间跨度")
        print(f"  开始: {data['first_ts']}")
        print(f"  结束: {data['last_ts']}")

if __name__ == "__main__":
    main()
