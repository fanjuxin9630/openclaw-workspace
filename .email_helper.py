#!/usr/bin/env python3
"""运财鼠邮件助手 - QQ邮箱 IMAP/SMTP 封装"""
import imaplib, smtplib, email, ssl, json, os, sys
from email.mime.text import MIMEText
from email.header import decode_header

CFG = {
    "email": "164953949@qq.com",
    "password": "xxnljyufyklxcahe",
    "imap_host": "imap.qq.com",
    "imap_port": 993,
    "smtp_host": "smtp.qq.com",
    "smtp_port": 465
}

def check_inbox(limit=5, mark_read=False):
    """获取最近邮件"""
    mail = imaplib.IMAP4_SSL(CFG["imap_host"], CFG["imap_port"])
    mail.login(CFG["email"], CFG["password"])
    mail.select("INBOX")
    _, ids = mail.search(None, "ALL")
    all_ids = ids[0].split()
    msgs = []
    for uid in all_ids[-limit:]:
        _, data = mail.fetch(uid, '(BODY[HEADER.FIELDS (FROM SUBJECT DATE)])')
        if _ == "OK" and data[0]:
            raw = data[0][1].decode('utf-8', errors='replace')
            h = {}
            for line in raw.split('\r\n'):
                if ':' in line:
                    k, v = line.split(':', 1)
                    h[k.strip().lower()] = v.strip()
            msgs.append(h)
    if mark_read:
        mail.store(",".join(a.decode() for a in all_ids[-limit:]), '+FLAGS', '\\Seen')
    mail.logout()
    return msgs

def send_email(to, subject, body):
    """发送邮件"""
    msg = MIMEText(body, "plain", "utf-8")
    msg["From"] = CFG["email"]
    msg["To"] = to
    msg["Subject"] = subject
    server = smtplib.SMTP_SSL(CFG["smtp_host"], CFG["smtp_port"])
    server.login(CFG["email"], CFG["password"])
    server.sendmail(CFG["email"], [to], msg.as_string())
    server.quit()

if __name__ == "__main__":
    action = sys.argv[1] if len(sys.argv) > 1 else "check"
    if action == "check":
        msgs = check_inbox(limit=5)
        for m in msgs:
            print(f"[{m.get('date','?')}] {m.get('from','?')[:40]} — {m.get('subject','?')[:60]}")
    elif action == "send":
        send_email(sys.argv[2], sys.argv[3], sys.argv[4])
        print(f"Sent to {sys.argv[2]}")
