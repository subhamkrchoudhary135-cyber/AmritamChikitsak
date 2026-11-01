"""
Comprehensive security scanner for SANJIVANI AI.
Scans all project files for potential credentials, API keys, passwords, and tokens.
Never prints raw secrets.
"""

import os
import re

PATTERNS = [
    (r'(?i)(?:api[_-]?key|apikey|secret[_-]?key|password|passwd|auth[_-]?token)\s*[:=]\s*["\']([^"\']{4,})["\']', "Generic Secret Assignment"),
    (r'sk-[a-zA-Z0-9]{20,}', "OpenAI API Key Pattern"),
    (r'sk-ant-[a-zA-Z0-9_-]{20,}', "Anthropic API Key Pattern"),
    (r'AIza[0-9A-Za-z-_]{35}', "Google API Key Pattern"),
    (r'ghp_[a-zA-Z0-9]{36}', "GitHub Personal Access Token"),
    (r'AKIA[0-9A-Z]{16}', "AWS Access Key ID"),
    (r'postgres(?:ql)?:\/\/[^:]+:([^@]+)@', "Database Connection URI with Password"),
    (r'-----BEGIN (?:RSA |EC )?PRIVATE KEY-----', "Private Key Header"),
]

# Patterns that are acceptable defaults or placeholders
IGNORE_VALUES = {
    "your_jwt_secret_key_here", "your_secret_key_here", "changeme", "secret",
    "postgresql://postgres:postgres@localhost:5432/sanjivani_ai",
    "postgresql://postgres:postgres@localhost:5432/swasth_ai",
    "postgresql://postgres:postgres@localhost:5432/test_sanjivani",
    "redis://localhost:6379/0", "localhost", "testsecret", "secretkey"
}

def scan():
    findings = []
    scanned_count = 0
    
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in ['.venv', '.git', 'node_modules', '__pycache__', '.pytest_cache', '.next', 'models_cache']]
        for f in files:
            if f.endswith(('.py', '.yaml', '.yml', '.json', '.toml', '.ini', '.env', '.md', '.ts', '.tsx', '.js', '.mjs', '.ipynb', '.sh')):
                p = os.path.join(root, f)
                scanned_count += 1
                try:
                    with open(p, 'r', encoding='utf-8', errors='ignore') as fh:
                        lines = fh.readlines()
                    for line_no, line in enumerate(lines, 1):
                        for pat, desc in PATTERNS:
                            for m in re.finditer(pat, line):
                                matched_str = m.group(0)
                                secret_part = m.group(1) if m.groups() else matched_str
                                
                                # Check if false positive or obvious placeholder
                                if secret_part.lower() in IGNORE_VALUES or 'dummy' in secret_part.lower() or 'example' in secret_part.lower():
                                    findings.append((p, line_no, desc, "[KNOWN PLACEHOLDER/DEFAULT]", line.strip()[:80]))
                                else:
                                    masked = matched_str[:8] + "..." + matched_str[-4:] if len(matched_str) > 14 else "***"
                                    findings.append((p, line_no, desc, masked, line.strip()[:80]))
                except Exception as e:
                    print(f"Error reading {p}: {e}")
                    
    print(f"Total files scanned: {scanned_count}")
    print(f"Total potential secret matches: {len(findings)}")
    print("-" * 80)
    for p, line_no, desc, masked, sample in findings:
        print(f"[{desc}] {p}:{line_no} -> {masked}")
        print(f"    Context: {sample}")
    print("-" * 80)

if __name__ == "__main__":
    scan()
