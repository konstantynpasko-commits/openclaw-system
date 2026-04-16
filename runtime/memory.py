#!/usr/bin/env python3
import json
from pathlib import Path
from typing import List, Dict

WORKSPACE = Path(__file__).resolve().parents[1]
SOURCE_DIR = WORKSPACE / 'openclaw_system'
INDEX_PATH = WORKSPACE / 'memory' / 'memory_index.json'


def _excerpt(text: str, query: str, radius: int = 80) -> str:
    lower = text.lower()
    q = query.lower()
    pos = lower.find(q)
    if pos == -1:
        snippet = text[: radius * 2].strip()
        return snippet.replace('\n', ' ')
    start = max(0, pos - radius)
    end = min(len(text), pos + len(query) + radius)
    snippet = text[start:end].strip().replace('\n', ' ')
    if start > 0:
        snippet = '...' + snippet
    if end < len(text):
        snippet = snippet + '...'
    return snippet


def build_index() -> List[Dict[str, str]]:
    records: List[Dict[str, str]] = []
    for path in sorted(SOURCE_DIR.glob('*.md')):
        text = path.read_text(encoding='utf-8')
        records.append({
            'path': str(path),
            'filename': path.name,
            'content': text,
        })
    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    INDEX_PATH.write_text(json.dumps(records, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return records


def load_index() -> List[Dict[str, str]]:
    if not INDEX_PATH.exists():
        return build_index()
    return json.loads(INDEX_PATH.read_text(encoding='utf-8'))


def search(query: str) -> List[Dict[str, str]]:
    query = query.strip()
    if not query:
        return []
    results: List[Dict[str, str]] = []
    for item in load_index():
        content = item.get('content', '')
        if query.lower() in content.lower() or query.lower() in item.get('filename', '').lower():
            results.append({
                'path': item['path'],
                'snippet': _excerpt(content, query),
            })
    return results


if __name__ == '__main__':
    import sys
    if len(sys.argv) >= 2 and sys.argv[1] == 'build':
        data = build_index()
        print(json.dumps({'indexed_files': len(data), 'index_path': str(INDEX_PATH)}, ensure_ascii=False, indent=2))
    elif len(sys.argv) >= 3 and sys.argv[1] == 'search':
        print(json.dumps(search(' '.join(sys.argv[2:])), ensure_ascii=False, indent=2))
    else:
        print('usage: memory.py build | memory.py search <query>')
