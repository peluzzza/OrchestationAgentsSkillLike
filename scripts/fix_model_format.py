"""
fix_model_format.py
-------------------
Converts `model:` YAML block-sequences in .agent.md frontmatter to the
inline format VS Code's agent linter requires:

  Block (before):           Inline (after):
  model:                    model: "A"           # single value
    - A                     model: ["A", "B"]    # multiple values (deduped)
    - B

Also:
  - Adds quotes to bare inline scalars: model: X  →  model: "X"
  - Removes # comments trapped inside frontmatter (e.g. # PREREQUISITE lines)
"""
import os
import re
import sys


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEARCH_DIRS = [
    os.path.join(ROOT, ".github", "agents"),
    os.path.join(ROOT, "plugins"),
]

# ── helpers ──────────────────────────────────────────────────────────────────

def _block_to_inline(match):
    """Replace a YAML block-sequence under `model:` with an inline form."""
    items_raw = match.group(1)
    items = []
    for line in re.split(r"\r?\n", items_raw):
        stripped = line.strip()
        if stripped.startswith("- "):
            item = stripped[2:].strip()
            if item and item not in items:           # dedup while preserving order
                items.append(item)
    if not items:
        return match.group(0)                        # nothing to do
    if len(items) == 1:
        return f'model: "{items[0]}"\n'              # trailing newline required
    quoted = ", ".join(f'"{i}"' for i in items)
    return f"model: [{quoted}]\n"                    # trailing newline required


def _fixup_frontmatter(content: str) -> str:
    """Apply all frontmatter fixes to a file's content."""

    # ── 1. Convert block-sequence model: ─────────────────────────────────────
    # Matches:  model:\n  - val1\n  - val2\n  (handles CRLF)
    content = re.sub(
        r"^model:\r?\n((?:[ \t]+-[ \t]+[^\r\n]+[\r\n]+)+)",
        _block_to_inline,
        content,
        flags=re.MULTILINE,
    )

    # ── 2. Quote bare inline scalars (model: X  →  model: "X") ───────────────
    # Only fires when the value is not already quoted and not an inline array.
    def _quote_inline(m):
        val = m.group(1).rstrip()
        if val.startswith('"') or val.startswith("'") or val.startswith("["):
            return f"model: {val}"
        return f'model: "{val}"'

    content = re.sub(
        r"^model: (.+?)\r?$",
        _quote_inline,
        content,
        flags=re.MULTILINE,
    )

    # ── 2b. Repair missing newline after model: (can result from prior run) ──
    # Catches: model: "X"nextKey:  or  model: [...]nextKey:
    content = re.sub(
        r'(^model: (?:"[^"\r\n]*"|\[[^\]\r\n]*\]))([^\r\n])',
        r'\1\n\2',
        content,
        flags=re.MULTILINE,
    )

    # ── 3. Remove bare comment lines from inside frontmatter ─────────────────
    # A comment line (starting with #) inside the --- delimiters is invalid
    # for strict YAML parsers used by VS Code's agent linter.
    def _strip_fm_comments(text: str) -> str:
        fm_re = re.compile(r"\A(---\r?\n)(.*?)(^---[ \t]*\r?\n)", re.DOTALL | re.MULTILINE)
        m = fm_re.match(text)
        if not m:
            return text
        open_delim, body, close_delim = m.group(1), m.group(2), m.group(3)
        # Remove lines that are purely a YAML comment (optional leading spaces + #)
        clean_body = re.sub(r"^[ \t]*#[^\r\n]*\r?\n", "", body, flags=re.MULTILINE)
        return open_delim + clean_body + close_delim + text[m.end():]

    content = _strip_fm_comments(content)

    return content


# ── main ─────────────────────────────────────────────────────────────────────

def main():
    changed = 0
    errors = 0
    visited = 0

    for base in SEARCH_DIRS:
        for dirpath, _dirs, files in os.walk(base):
            for fname in files:
                if not fname.endswith(".agent.md"):
                    continue
                fpath = os.path.join(dirpath, fname)
                visited += 1
                try:
                    with open(fpath, "r", encoding="utf-8") as fh:
                        original = fh.read()
                    fixed = _fixup_frontmatter(original)
                    if fixed != original:
                        with open(fpath, "w", encoding="utf-8", newline="") as fh:
                            fh.write(fixed)
                        rel = os.path.relpath(fpath, ROOT)
                        print(f"  fixed: {rel}")
                        changed += 1
                except Exception as exc:
                    print(f"  ERROR {fpath}: {exc}", file=sys.stderr)
                    errors += 1

    print(f"\n{visited} files scanned -> {changed} updated, {errors} errors.")


if __name__ == "__main__":
    main()
