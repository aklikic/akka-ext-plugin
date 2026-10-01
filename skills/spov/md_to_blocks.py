#!/usr/bin/env python3
"""Convert a SCOPE_OF_WORK.md into blocks.json + rendered Mermaid PNGs for build_docx.py.

    python skills/spov/md_to_blocks.py <scope.md> <blocks.json> [--img-dir <dir>]

Blocks follow the format expected by build_docx.py from gdoc-restyle:
  {"k": "h",     "lvl": 1|2|3, "text": "..."}
  {"k": "p",     "runs": [{"t": "...", "b": bool, "i": bool}], "hl": bool}
  {"k": "list",  "ordered": bool, "items": [{"runs": [...], "lvl": 0}]}
  {"k": "table", "rows": [{"kind": "head"|"body", "cells": [{"paras": [[runs]]}]}]}
  {"k": "image", "path": "diagrams/diagram-1.png", "alt": "..."}

Mermaid code blocks are extracted, rendered to PNG via mmdc, and replaced with
image blocks. build_docx.py needs a small extension to handle "image" blocks.
"""
import argparse
import json
import os
import re
import subprocess
import sys
import tempfile

if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')


def parse_inline(text):
    """Parse inline markdown (bold, italic, bold+italic, code) into runs."""
    runs = []
    # Pattern: ***bold+italic***, **bold**, *italic*, `code`
    pattern = re.compile(r'(\*\*\*(.+?)\*\*\*|\*\*(.+?)\*\*|\*(.+?)\*|`(.+?)`)')
    pos = 0
    for m in pattern.finditer(text):
        # Text before this match
        if m.start() > pos:
            runs.append({'t': text[pos:m.start()], 'b': False, 'i': False})
        if m.group(2):  # ***bold+italic***
            runs.append({'t': m.group(2), 'b': True, 'i': True})
        elif m.group(3):  # **bold**
            runs.append({'t': m.group(3), 'b': True, 'i': False})
        elif m.group(4):  # *italic*
            runs.append({'t': m.group(4), 'b': False, 'i': True})
        elif m.group(5):  # `code`
            runs.append({'t': m.group(5), 'b': False, 'i': False})
        pos = m.end()
    if pos < len(text):
        runs.append({'t': text[pos:], 'b': False, 'i': False})
    # Merge adjacent runs with same formatting
    merged = []
    for r in runs:
        if not r['t']:
            continue
        if merged and merged[-1]['b'] == r['b'] and merged[-1]['i'] == r['i']:
            merged[-1]['t'] += r['t']
        else:
            merged.append(r)
    return merged if merged else [{'t': '', 'b': False, 'i': False}]


def parse_table(lines):
    """Parse markdown table lines into a table block."""
    rows = []
    for i, line in enumerate(lines):
        line = line.strip()
        if not line.startswith('|'):
            continue
        cells_text = [c.strip() for c in line.split('|')[1:-1]]
        # Skip separator row (e.g., |---|---|)
        if all(re.match(r'^[-:]+$', c) for c in cells_text):
            continue
        kind = 'head' if i == 0 else 'body'
        cells = []
        for ct in cells_text:
            cells.append({'paras': [parse_inline(ct)]})
        rows.append({'kind': kind, 'cells': cells})
    return {'k': 'table', 'rows': rows}


def render_mermaid(code, output_path):
    """Render Mermaid code to PNG using mmdc."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.mmd', delete=False) as f:
        f.write(code)
        mmd_path = f.name
    try:
        result = subprocess.run(
            ['npx', '--yes', '@mermaid-js/mermaid-cli',
             '-i', mmd_path, '-o', output_path,
             '-b', 'white', '--scale', '2',
             '-t', 'default'],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode != 0:
            print(f'  mmdc warning: {result.stderr.strip()}', file=sys.stderr)
        return os.path.exists(output_path)
    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        print(f'  mmdc error: {e}', file=sys.stderr)
        return False
    finally:
        os.unlink(mmd_path)


def parse_md(md_text, img_dir):
    """Parse markdown text into blocks list, rendering Mermaid diagrams."""
    blocks = []
    lines = md_text.split('\n')
    i = 0
    mermaid_count = 0
    list_buffer = None  # accumulate list items

    def flush_list():
        nonlocal list_buffer
        if list_buffer:
            blocks.append(list_buffer)
            list_buffer = None

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Mermaid code block
        if stripped.startswith('```mermaid'):
            flush_list()
            i += 1
            code_lines = []
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code_lines.append(lines[i])
                i += 1
            i += 1  # skip closing ```
            mermaid_count += 1
            png_name = f'diagram-{mermaid_count}.png'
            png_path = os.path.join(img_dir, png_name)
            code = '\n'.join(code_lines)
            print(f'  Rendering Mermaid diagram {mermaid_count}...')
            if render_mermaid(code, png_path):
                blocks.append({'k': 'image', 'path': png_path, 'alt': f'Diagram {mermaid_count}'})
            else:
                # Fallback: insert as italic note
                blocks.append({'k': 'p', 'runs': [{'t': f'[Diagram {mermaid_count} — see markdown version]', 'b': False, 'i': True}], 'hl': False})
            continue

        # Other code blocks — skip
        if stripped.startswith('```'):
            flush_list()
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('```'):
                i += 1
            i += 1
            continue

        # Headings
        hm = re.match(r'^(#{1,3})\s+(.+)$', stripped)
        if hm:
            flush_list()
            lvl = len(hm.group(1))
            text = hm.group(2).strip()
            # Strip bold markers from heading text
            text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
            blocks.append({'k': 'h', 'lvl': lvl, 'text': text})
            i += 1
            continue

        # Table — collect consecutive lines starting with |
        if stripped.startswith('|'):
            flush_list()
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                table_lines.append(lines[i])
                i += 1
            blocks.append(parse_table(table_lines))
            continue

        # Ordered list item
        olm = re.match(r'^\d+\.\s+(.+)$', stripped)
        if olm:
            runs = parse_inline(olm.group(1))
            if list_buffer and list_buffer['ordered']:
                list_buffer['items'].append({'runs': runs, 'lvl': 0})
            else:
                flush_list()
                list_buffer = {'k': 'list', 'ordered': True, 'items': [{'runs': runs, 'lvl': 0}]}
            i += 1
            continue

        # Unordered list item
        ulm = re.match(r'^[-*]\s+(.+)$', stripped)
        if ulm:
            runs = parse_inline(ulm.group(1))
            if list_buffer and not list_buffer['ordered']:
                list_buffer['items'].append({'runs': runs, 'lvl': 0})
            else:
                flush_list()
                list_buffer = {'k': 'list', 'ordered': False, 'items': [{'runs': runs, 'lvl': 0}]}
            i += 1
            continue

        # Horizontal rule — skip
        if re.match(r'^---+$', stripped):
            flush_list()
            i += 1
            continue

        # Empty line
        if not stripped:
            flush_list()
            i += 1
            continue

        # Header metadata lines (Date:, Version:, etc.) — skip if at top
        if re.match(r'^\*\*(Date|Version|Prepared for|Prepared by)\*\*:', stripped):
            i += 1
            continue

        # Paragraph — collect continuation lines
        flush_list()
        para_lines = [stripped]
        i += 1
        while i < len(lines):
            next_stripped = lines[i].strip()
            # Stop at: empty line, heading, list, table, code block, hr
            if (not next_stripped or next_stripped.startswith('#') or
                next_stripped.startswith('|') or next_stripped.startswith('```') or
                re.match(r'^[-*]\s+', next_stripped) or
                re.match(r'^\d+\.\s+', next_stripped) or
                re.match(r'^---+$', next_stripped)):
                break
            para_lines.append(next_stripped)
            i += 1

        full_text = ' '.join(para_lines)
        # Check if highlighted (contains bold markers throughout — heuristic)
        hl = full_text.endswith(':') and '**' in full_text
        # Check if entirely italic
        all_italic = full_text.startswith('*') and full_text.endswith('*') and not full_text.startswith('**')
        runs = parse_inline(full_text)
        if all_italic and len(runs) == 1:
            runs[0]['i'] = True
        blocks.append({'k': 'p', 'runs': runs, 'hl': hl})

    flush_list()
    return blocks


def summary(blocks):
    """Print a summary of parsed blocks."""
    for b in blocks:
        if b['k'] == 'h':
            print(f"H{b['lvl']}  {b['text']}")
        elif b['k'] == 'p':
            t = ''.join(r['t'] for r in b['runs'])
            tag = '*' if b['hl'] else ' '
            print(f"  P{tag} {t[:80]}{'...' if len(t) > 80 else ''}")
        elif b['k'] == 'list':
            print(f"  {'OL' if b['ordered'] else 'UL'} {len(b['items'])} items")
        elif b['k'] == 'table':
            kinds = ''.join(r['kind'][0] for r in b['rows'])
            cells = [(''.join(r['t'] for r in c['paras'][0])) for c in b['rows'][0]['cells']]
            print(f"  T  {len(b['rows'])} rows [{kinds}]  {cells}")
        elif b['k'] == 'image':
            print(f"  IMG {b['path']}")


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('md', help='Path to SCOPE_OF_WORK.md')
    ap.add_argument('out', help='Output blocks.json path')
    ap.add_argument('--img-dir', default=None,
                    help='Directory for rendered Mermaid PNGs (default: same dir as output)')
    args = ap.parse_args()

    img_dir = args.img_dir or os.path.join(os.path.dirname(args.out) or '.', 'diagrams')
    os.makedirs(img_dir, exist_ok=True)

    md_text = open(args.md, encoding='utf-8').read()

    # Extract title and meta from header
    title_match = re.search(r'^#\s+(.+)', md_text, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else 'Untitled'

    print(f'Parsing {args.md}...')
    blocks = parse_md(md_text, img_dir)

    # Remove the top-level H1 (it becomes the cover title)
    if blocks and blocks[0]['k'] == 'h' and blocks[0]['lvl'] == 1:
        blocks = blocks[1:]

    # Also skip "Scope of Work" H2 if present
    if blocks and blocks[0]['k'] == 'h' and 'scope of work' in blocks[0]['text'].lower():
        blocks = blocks[1:]

    json.dump(blocks, open(args.out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'\nBlocks summary:')
    summary(blocks)
    print(f'\nWrote {args.out} ({len(blocks)} blocks)')
    print(f'Title for build_docx.py: --title "{title}"')
