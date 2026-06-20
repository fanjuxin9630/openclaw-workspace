#!/bin/bash
# =============================================
# 🐭 运财鼠 回滚脚本
# 用途：安全回滚到指定版本（自动创建备份点）
# 用法：./scripts/git-rollback.sh <commit-hash|tag-name>
# =============================================

set -e

cd "$(dirname "$0")/.."

TARGET="${1:-}"
if [[ -z "$TARGET" ]]; then
    echo "❌ 用法: $0 <commit-hash|tag-name>"
    echo ""
    echo "📋 可用的 tag："
    git tag | sort -r | head -10
    echo ""
    echo "📋 最近 10 条提交："
    git log --oneline -10
    exit 1
fi

# 检查目标是否存在
if ! git rev-parse --verify "$TARGET" >/dev/null 2>&1; then
    echo "❌ 错误：找不到 '$TARGET'"
    exit 1
fi

echo "🐭 准备回滚..."
echo ""

# 创建备份 tag
BACKUP_TAG="pre-rollback-$(date '+%Y%m%d-%H%M%S')"
git tag "$BACKUP_TAG"
echo "📦 已创建备份点: $BACKUP_TAG"

echo "🎯 回滚目标: $TARGET ($(git rev-parse --short "$TARGET"))"
echo ""

# 显示变更内容
echo "📋 即将被撤销的提交："
git log --oneline "$TARGET"..HEAD 2>/dev/null || true
echo ""

# 执行安全回滚（revert 而非 reset，保留历史）
echo "🔄 正在执行安全回滚 (revert)..."
if git revert --no-edit "$TARGET"..HEAD 2>/dev/null; then
    echo "✅ 回滚成功！"
    git push origin master --tags
    echo "🚀 已推送到远程仓库"
else
    echo "⚠️  自动回滚有冲突，手动处理："
    echo "  git revert --continue   # 解决冲突后继续"
    echo "  或放弃回滚："
    echo "  git revert --abort"
fi

echo ""
echo "🔄 如果错误回滚，可恢复到备份点："
echo "  git revert --no-edit $BACKUP_TAG..HEAD"
