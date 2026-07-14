#!/usr/bin/env python3
"""HeiGeAi 开源发布前硬检查。

用法:
    python3 preflight.py <repo-path> [--check-links]

检查项:
    1. 必备文件: README.md / LICENSE / .gitignore
    2. LICENSE 类型识别; PolyForm 必须带 Required Notice
    3. git 历史: 邮箱只允许 noreply, commit 信息禁 Co-Authored-By
    4. SKILL.md frontmatter: 顶层键白名单, name 与目录名一致
    5. 外部实体扫描: 域名 / 邮箱 / GitHub 句柄清单, 供人工核查
    6. --check-links: README 外链存活检查

退出码: 有 ERROR 时为 1, 否则 0。WARN 逐条人工判断。
"""

import re
import subprocess
import sys
import urllib.request
from pathlib import Path

ALLOWED_EMAIL_SUFFIX = "@users.noreply.github.com"
ALLOWED_FRONTMATTER_KEYS = {"name", "description", "allowed-tools",
                            "compatibility", "license", "metadata"}
# 无需人工核查的域名: 基础设施、保留 TLD、官方站点
DOMAIN_ALLOWLIST_SUFFIXES = (
    "github.com", "githubusercontent.com", "github.io", "shields.io",
    "example.com", ".example", ".invalid", ".test", "localhost",
    "anthropic.com", "claude.ai", "claude.com", "openai.com",
    "polyformproject.org", "opensource.org", "python.org", "nodejs.org",
)

errors, warns, infos = [], [], []


def rel(path, root):
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def check_required_files(root):
    if not (root / "README.md").exists():
        errors.append("缺 README.md")
    if not (root / "LICENSE").exists():
        errors.append("缺 LICENSE")
    if not (root / ".gitignore").exists():
        warns.append("缺 .gitignore, 确认是否需要")


def check_license(root):
    lic = root / "LICENSE"
    if not lic.exists():
        return
    text = lic.read_text(encoding="utf-8", errors="replace")
    if "PolyForm Noncommercial" in text:
        infos.append("协议: PolyForm Noncommercial 1.0.0")
        if not re.search(r"^Required Notice: Copyright .*HeiGeAi", text, re.M):
            errors.append("PolyForm LICENSE 缺开头的 Required Notice 行"
                          "(Required Notice: Copyright <年> HeiGeAi (Blake Xu) (https://github.com/HeiGeAi))")
    elif "MIT License" in text or "Permission is hereby granted, free of charge" in text:
        infos.append("协议: MIT")
        if "HeiGeAi" not in text:
            warns.append("MIT LICENSE 的 Copyright 行没写 HeiGeAi (Blake Xu)")
    else:
        warns.append("LICENSE 类型识别不出来, 人工确认协议选型")


def check_git_history(root):
    if not (root / ".git").exists():
        infos.append("还没 git init, 跳过历史检查(建仓后记得复跑)")
        return
    try:
        out = subprocess.run(["git", "-C", str(root), "log", "--format=%an|%ae"],
                             capture_output=True, text=True, check=True).stdout
    except subprocess.CalledProcessError:
        infos.append("git 历史为空, 跳过历史检查")
        return
    idents = sorted(set(line for line in out.splitlines() if line.strip()))
    for ident in idents:
        name, _, email = ident.partition("|")
        if not email.endswith(ALLOWED_EMAIL_SUFFIX):
            errors.append(f"提交历史有非 noreply 邮箱: {name} <{email}> "
                          "(私人邮箱进公开历史要 force push 重写才能洗掉, 推送前必须清)")
    bodies = subprocess.run(["git", "-C", str(root), "log", "--format=%B"],
                            capture_output=True, text=True).stdout
    if re.search(r"co-authored-by", bodies, re.I):
        errors.append("commit 信息里有 Co-Authored-By 标记, 公开仓库不允许")


def parse_frontmatter_keys(text):
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    if not m:
        return None, None
    keys, name_val = [], None
    for line in m.group(1).splitlines():
        km = re.match(r"^([A-Za-z][\w-]*):", line)  # 顶层键: 行首无缩进
        if km:
            keys.append(km.group(1))
            if km.group(1) == "name":
                name_val = line.split(":", 1)[1].strip().strip("\"'")
    return keys, name_val


def check_skill_frontmatter(root):
    skill_md = root / "SKILL.md"
    if not skill_md.exists():
        return
    text = skill_md.read_text(encoding="utf-8", errors="replace")
    keys, name_val = parse_frontmatter_keys(text)
    if keys is None:
        errors.append("SKILL.md 缺 frontmatter")
        return
    bad = [k for k in keys if k not in ALLOWED_FRONTMATTER_KEYS]
    if bad:
        errors.append(f"SKILL.md frontmatter 顶层键越界: {bad} "
                      f"(只允许 {sorted(ALLOWED_FRONTMATTER_KEYS)}, 其余放 metadata: 下)")
    if not name_val:
        errors.append("SKILL.md frontmatter 缺 name")
    elif name_val != root.resolve().name:
        errors.append(f"skill 三一致破坏: frontmatter name={name_val} 目录名={root.resolve().name}")


# 实体扫描只认这些真实 TLD, 避免把代码里的 args.action 之类误报成域名
REAL_TLDS = {"com", "net", "org", "io", "ai", "cn", "dev", "app", "me", "co",
             "cc", "xyz", "space", "site", "top", "info", "mom", "run", "sh",
             "cloud", "tech", "online", "store", "vip", "fun", "im", "tv",
             "example", "invalid", "test"}


def scan_doc_files(root):
    # 虚构实体核查针对读者会看到的文档; 代码文件里的标识符误报太多, 交给人工清单
    exts = {".md", ".txt", ".html"}
    for p in root.rglob("*"):
        if p.is_file() and p.suffix in exts and ".git" not in p.parts \
                and "node_modules" not in p.parts and "dist" not in p.parts:
            yield p


def domain_allowed(domain):
    d = domain.lower()
    return any(d == s or d.endswith("." + s.lstrip("."))
               for s in DOMAIN_ALLOWLIST_SUFFIXES)


def check_entities(root):
    domains, emails, handles = {}, {}, {}
    dom_re = re.compile(r"\b((?:[a-z0-9-]+\.)+([a-z]{2,}))(?!\()\b", re.I)
    email_re = re.compile(r"\b([\w.+-]+@(?:[\w-]+\.)+[a-z]{2,})\b", re.I)
    handle_re = re.compile(r"github\.com/([A-Za-z0-9](?:[A-Za-z0-9-]{0,38}))\b")
    for p in scan_doc_files(root):
        text = p.read_text(encoding="utf-8", errors="replace")
        for m in email_re.finditer(text):
            email = m.group(1)
            dom = email.split("@")[1]
            if not domain_allowed(dom):
                emails.setdefault(email, rel(p, root))
        for m in dom_re.finditer(text):
            dom, tld = m.group(1), m.group(2).lower()
            if tld in REAL_TLDS and not domain_allowed(dom) and not re.match(r"^[\d.]+$", dom):
                domains.setdefault(dom, rel(p, root))
        for m in handle_re.finditer(text):
            h = m.group(1)
            if h.lower() not in {"heigeai", "blakexu", "polyformproject", "anthropics"}:
                handles.setdefault(h, rel(p, root))
    for email, loc in sorted(emails.items()):
        warns.append(f"示例邮箱用了真实域: {email} ({loc}), 换成 user@example.com 这类保留域")
    if domains:
        listing = ", ".join(f"{d}({loc})" for d, loc in sorted(domains.items())[:20])
        infos.append(f"需人工核查的域名清单(RDAP 逐一查注册): {listing}")
    if handles:
        listing = ", ".join(f"{h}({loc})" for h, loc in sorted(handles.items())[:20])
        infos.append(f"需人工核查的 GitHub 句柄(gh api users/<句柄> 查存在): {listing}")


def check_links(root):
    readme = root / "README.md"
    if not readme.exists():
        return
    urls = sorted(set(re.findall(r"https?://[^\s)\"'<>\]]+", readme.read_text(encoding="utf-8", errors="replace"))))
    urls = [u.rstrip(".,;:") for u in urls if "img.shields.io" not in u]
    for url in urls:
        try:
            req = urllib.request.Request(url, method="GET",
                                         headers={"User-Agent": "Mozilla/5.0 (preflight-check)"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                if resp.status >= 400:
                    warns.append(f"外链异常 {resp.status}: {url}")
        except Exception as e:  # noqa: BLE001
            warns.append(f"外链打不开: {url} ({e})")
    infos.append(f"外链检查完成, 共 {len(urls)} 条(shields 徽章已跳过)")


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(2)
    root = Path(args[0]).expanduser()
    if not root.is_dir():
        print(f"目录不存在: {root}")
        sys.exit(2)

    check_required_files(root)
    check_license(root)
    check_git_history(root)
    check_skill_frontmatter(root)
    check_entities(root)
    if "--check-links" in args:
        check_links(root)

    print(f"\n=== preflight: {root.resolve().name} ===")
    for msg in errors:
        print(f"[ERROR] {msg}")
    for msg in warns:
        print(f"[WARN]  {msg}")
    for msg in infos:
        print(f"[INFO]  {msg}")
    print(f"\n结果: {len(errors)} ERROR / {len(warns)} WARN / {len(infos)} INFO")
    if errors:
        print("ERROR 清零才能 push。")
        sys.exit(1)
    print("硬检查通过。WARN 逐条人工判断, 再过 references/checklist.md 五项人工清单。")


if __name__ == "__main__":
    main()
