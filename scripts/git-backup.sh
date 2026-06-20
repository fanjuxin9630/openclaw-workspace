#!/bin/bash
# =============================================
# 🐭 运财鼠 Git 备份 & 回滚脚本
# 用途：自动备份 + 创建可回滚的 git tag
# 用法：./scripts/git-backup.sh [message]
# =============================================

set -e

cd "$(dirname "$0")/.."

MESSAGE="${1:-自动备份 $(date '+%Y-%m-%d %H:%M')}"
TAG_NAME="backup-$(date '+%Y%m%d-%H%M%S')"

echo "🐭 运财鼠备份中..."
echo "📝 提交信息: $MESSAGE"

# 检查是否有变更
if [[ -z $(git status --porcelain) ]]; then
    echo "✅ 工作区干净，无变更需提交。"
    # 仍然打 tag 标记时间点
    git tag -f "$TAG_NAME" HEAD 2>/dev/null || true
    echo "🏷️  已标记时间戳: $TAG_NAME"
    exit 0
fi

# 添加所有变更
git add -A

# 提交
git commit -m "$MESSAGE"

# 打时间戳 tag
git tag "$TAG_NAME"

# 推送到远程
git push origin master --tags

echo "✅ 备份完成！"
echo "  提交: $(git rev-parse --short HEAD)"
echo "  Tag:  $TAG_NAME"
echo ""
echo "🔄 如需回滚到该版本："
echo "  git checkout tags/$TAG_NAME"
echo "  或恢复到某个 tag："
echo "  git revert <commit-hash> --no-edit"
