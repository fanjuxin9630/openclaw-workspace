#!/bin/bash
# Bounty监控脚本 - 运财鼠
# 每小时检查GitHub上新的bounty标签issue
# 输出到 workspace/data/bounty-alerts.md

WORKSPACE="/home/dify007/.openclaw/workspace"
ALERT_FILE="$WORKSPACE/data/bounty-alerts.md"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M EDT')

mkdir -p "$WORKSPACE/data"

# 当前时间戳用于标记
echo "## 🔍 Bounty扫描报告 - $TIMESTAMP" >> "$ALERT_FILE"
echo "" >> "$ALERT_FILE"

# 搜索1: 最新带bounty标签的TypeScript/Python issues
for lang in "typescript" "python" "javascript" "shell" "go"; do
    RESULT=$(curl -s "https://api.github.com/search/issues?q=label:bounty+is:issue+is:open+language:${lang}+no:assignee&sort=created&order=desc&per_page=5" 2>/dev/null)
    COUNT=$(echo "$RESULT" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['total_count'])" 2>/dev/null)
    
    if [ "$COUNT" != "" ] && [ "$COUNT" -gt 0 ]; then
        echo "### $lang ($COUNT 个可用)" >> "$ALERT_FILE"
        echo "$RESULT" | python3 -c "
import json, sys
d = json.load(sys.stdin)
for i in d.get('items', [])[:5]:
    repo = i['repository_url'].split('/')[-1]
    owner = i['repository_url'].split('/')[-2]
    title = i['title'][:60]
    created = i['created_at'][:10]
    comments = i['comments']
    url = i['html_url']
    print(f'- [{owner}/{repo} #{i[\"number\"]}] {title}')
    print(f'  📅 {created} | 💬 {comments}条评论')
    print(f'  🔗 {url}')
    print()
" 2>/dev/null >> "$ALERT_FILE"
    fi
done

echo "---" >> "$ALERT_FILE"
echo "" >> "$ALERT_FILE"

# 只保留最近50条记录
tail -200 "$ALERT_FILE" > "${ALERT_FILE}.tmp" && mv "${ALERT_FILE}.tmp" "$ALERT_FILE"

echo "✅ 扫描完成 - $TIMESTAMP"
