#!/usr/bin/env python3
"""
🐭 运财鼠邮件助手 v2.0 — 多账户支持

用法:
  .email_helper.py check [账户名]      # 查看最近邮件
  .email_helper.py list              # 列出所有账户
  .email_helper.py send <to> <sub> <body> [账户名]

账户:
  main    — QQ邮箱 164953949@qq.com (主号, IMAP)
  sub     — 163邮箱 shixumei080@163.com (副号, POP3)
  留空    — 默认主号
"""
import imaplib, smtplib, poplib, email, ssl, json, os, sys
from email.mime.text import MIMEText
from email.header import decode_header

# ===== 账户配置 =====
ACCOUNTS = {
    "main": {
        "label": "主号 QQ",
        "email": "164953949@qq.com",
        "password": "xxnljyufyklxcahe",
        "type": "imap",
        "imap_host": "imap.qq.com", "imap_port": 993,
        "smtp_host": "smtp.qq.com", "smtp_port": 465
    },
    "sub": {
        "label": "副号 163",
        "email": "shixumei080@163.com",
        "password": "JZjT5LKk4vw5JTW5",
        "type": "pop3",
        "pop3_host": "pop.163.com", "pop3_port": 995,
        "smtp_host": "smtp.163.com", "smtp_port": 465
    }
}

def _parse_header(raw):
    """解析邮件头部行"""
    h = {}
    for line in raw.split('\r\n'):
        if ':' in line:
            k, v = line.split(':', 1)
            h[k.strip().lower()] = v.strip()
    return h

def check_inbox_imap(cfg, limit=5):
    """通过 IMAP 检查收件箱"""
    mail = imaplib.IMAP4_SSL(cfg["imap_host"], cfg["imap_port"])
    mail.login(cfg["email"], cfg["password"])
    mail.select("INBOX")
    _, ids = mail.search(None, "ALL")
    all_ids = ids[0].split()
    msgs = []
    for uid in all_ids[-limit:]:
        _, data = mail.fetch(uid, '(BODY[HEADER.FIELDS (FROM SUBJECT DATE)])')
        if _ == "OK" and data[0]:
            raw = data[0][1].decode('utf-8', errors='replace')
            msgs.append(_parse_header(raw))
    mail.logout()
    return msgs

def check_inbox_pop3(cfg, limit=5):
    """通过 POP3 检查收件箱"""
    M = poplib.POP3_SSL(cfg["pop3_host"], cfg["pop3_port"])
    M.user(cfg["email"])
    M.pass_(cfg["password"])
    count, _ = M.stat()
    msgs = []
    for num in range(max(1, count - limit + 1), count + 1):
        resp, lines, octets = M.top(num, 5)
        raw = b'\r\n'.join(lines).decode('utf-8', errors='replace')
        msgs.append(_parse_header(raw))
    M.quit()
    return msgs

def check_inbox(acct="main", limit=5):
    """获取最近邮件"""
    cfg = ACCOUNTS.get(acct)
    if not cfg:
        return [{"error": f"未知账户: {acct}"}]
    if cfg.get("type") == "pop3":
        return check_inbox_pop3(cfg, limit)
    else:
        return check_inbox_imap(cfg, limit)

def send_email(to, subject, body, acct="main"):
    """发送邮件"""
    cfg = ACCOUNTS.get(acct)
    if not cfg:
        print(f"❌ 未知账户: {acct}")
        return
    msg = MIMEText(body, "plain", "utf-8")
    msg["From"] = cfg["email"]
    msg["To"] = to
    msg["Subject"] = subject
    server = smtplib.SMTP_SSL(cfg["smtp_host"], cfg["smtp_port"])
    server.login(cfg["email"], cfg["password"])
    server.sendmail(cfg["email"], [to], msg.as_string())
    server.quit()
    print(f"✅ 已从 {cfg['label']} 发送至 {to}")

def list_accounts():
    """列出所有账户"""
    for key, cfg in ACCOUNTS.items():
        print(f"  {key}: {cfg['label']} — {cfg['email']} ({cfg.get('type','imap').upper()})")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法:")
        print("  .email_helper.py check [main|sub]")
        print("  .email_helper.py list")
        print("  .email_helper.py send <to> <subject> <body> [main|sub]")
        sys.exit(1)

    action = sys.argv[1]
    if action == "list":
        list_accounts()
    elif action == "check":
        acct = sys.argv[2] if len(sys.argv) > 2 else "main"
        msgs = check_inbox(acct, limit=5)
        for m in msgs:
            if "error" in m:
                print(f"  ❌ {m['error']}")
            else:
                print(f"  [{m.get('date','?')}] {m.get('from','?')[:40]}")
                print(f"    └─ {m.get('subject','?')[:60]}")
    elif action == "send":
        if len(sys.argv) < 5:
            print("用法: .email_helper.py send <to> <subject> <body> [main|sub]")
            sys.exit(1)
        acct = sys.argv[5] if len(sys.argv) > 5 else "main"
        send_email(sys.argv[2], sys.argv[3], sys.argv[4], acct)
    else:
        print(f"❌ 未知操作: {action}")
