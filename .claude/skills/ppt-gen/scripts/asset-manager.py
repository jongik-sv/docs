#!/usr/bin/env python3
"""
Asset Manager - 에셋 저장/검색/삭제 CLI

PPT 생성에 사용할 아이콘, 이미지 등의 에셋을 관리합니다.

Usage:
    python asset-manager.py add <file> --id <id> --tags "tag1,tag2"
    python asset-manager.py search "chart"
    python asset-manager.py list --type icons
    python asset-manager.py delete <id>
    python asset-manager.py info <id>

Examples:
    # 아이콘 추가
    python asset-manager.py add icon.svg --id chart-line --tags "chart,analytics"

    # URL에서 이미지 추가
    python asset-manager.py add "https://example.com/bg.png" --id hero-bg --tags "background,hero"

    # 검색
    python asset-manager.py search chart
    python asset-manager.py search --tags background

    # 목록
    python asset-manager.py list
    python asset-manager.py list --type icons --format table

    # 삭제
    python asset-manager.py delete chart-line
"""

import argparse
import shutil
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

import yaml

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False


# 기본 경로 설정
SCRIPT_DIR = Path(__file__).parent
TEMPLATES_DIR = SCRIPT_DIR.parent / 'templates'
ASSETS_DIR = TEMPLATES_DIR / 'assets'
REGISTRY_PATH = ASSETS_DIR / 'registry.yaml'


def load_registry() -> dict:
    """registry.yaml 로드"""
    if not REGISTRY_PATH.exists():
        return {'icons': [], 'images': []}

    with open(REGISTRY_PATH, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f) or {}

    return {
        'icons': data.get('icons') or [],
        'images': data.get('images') or []
    }


def save_registry(registry: dict) -> None:
    """registry.yaml 저장"""
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)

    yaml_str = f"""# 공용 에셋 레지스트리
# 마지막 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M')}

"""
    yaml_str += yaml.dump(registry, allow_unicode=True, default_flow_style=False, sort_keys=False)

    with open(REGISTRY_PATH, 'w', encoding='utf-8') as f:
        f.write(yaml_str)


def get_all_assets(registry: dict) -> list:
    """모든 에셋 목록 반환 (type 필드 포함)"""
    assets = []
    for item in registry.get('icons', []):
        item_copy = dict(item)
        item_copy['_type'] = 'icon'
        assets.append(item_copy)
    for item in registry.get('images', []):
        item_copy = dict(item)
        item_copy['_type'] = 'image'
        assets.append(item_copy)
    return assets


def find_asset(registry: dict, asset_id: str) -> tuple:
    """ID로 에셋 찾기 → (asset_dict, asset_type, index)"""
    for idx, item in enumerate(registry.get('icons', [])):
        if item.get('id') == asset_id:
            return item, 'icons', idx
    for idx, item in enumerate(registry.get('images', [])):
        if item.get('id') == asset_id:
            return item, 'images', idx
    return None, None, -1


def detect_asset_type(file_path: str) -> str:
    """파일 확장자로 에셋 타입 감지"""
    path = Path(file_path)
    ext = path.suffix.lower()

    icon_exts = {'.svg', '.ico'}
    if ext in icon_exts:
        return 'icons'
    return 'images'


def is_url(path: str) -> bool:
    """URL인지 확인"""
    parsed = urlparse(path)
    return parsed.scheme in ('http', 'https')


def download_file(url: str, dest_path: Path) -> bool:
    """URL에서 파일 다운로드"""
    if not HAS_REQUESTS:
        print("Error: requests 모듈이 필요합니다. pip install requests")
        return False

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        with open(dest_path, 'wb') as f:
            f.write(response.content)
        return True
    except Exception as e:
        print(f"Error: 다운로드 실패 - {e}")
        return False


def cmd_add(args) -> int:
    """에셋 추가"""
    source = args.source
    asset_id = args.id
    name = args.name or asset_id
    tags = [t.strip() for t in args.tags.split(',')] if args.tags else []

    registry = load_registry()

    # ID 중복 확인
    existing, _, _ = find_asset(registry, asset_id)
    if existing:
        print(f"Error: ID '{asset_id}'가 이미 존재합니다.")
        return 1

    # URL vs 로컬 파일 처리
    if is_url(source):
        # URL에서 파일명 추출
        parsed = urlparse(source)
        filename = Path(parsed.path).name
        if not filename or '.' not in filename:
            filename = f"{asset_id}.png"

        asset_type = args.type or detect_asset_type(filename)
        dest_dir = ASSETS_DIR / asset_type
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest_path = dest_dir / filename

        print(f"[1/3] 다운로드: {source}")
        if not download_file(source, dest_path):
            return 1

        source_type = 'downloaded'
        original_url = source
    else:
        # 로컬 파일
        src_path = Path(source)
        if not src_path.exists():
            print(f"Error: 파일을 찾을 수 없습니다 - {source}")
            return 1

        asset_type = args.type or detect_asset_type(source)
        dest_dir = ASSETS_DIR / asset_type
        dest_dir.mkdir(parents=True, exist_ok=True)

        filename = src_path.name
        dest_path = dest_dir / filename

        print(f"[1/3] 복사: {src_path} → {dest_path}")
        shutil.copy2(src_path, dest_path)

        source_type = 'local'
        original_url = None

    # 레지스트리에 추가
    asset_entry = {
        'id': asset_id,
        'name': name,
        'file': f"{asset_type}/{filename}",
        'source': source_type,
        'tags': tags,
        'created': datetime.now().strftime('%Y-%m-%d'),
    }
    if original_url:
        asset_entry['original_url'] = original_url

    print(f"[2/3] 레지스트리 업데이트...")
    registry[asset_type].append(asset_entry)
    save_registry(registry)

    print(f"[3/3] 완료!")
    print(f"  ID: {asset_id}")
    print(f"  Type: {asset_type}")
    print(f"  File: {dest_path}")
    print(f"  Tags: {', '.join(tags) if tags else '(없음)'}")

    return 0


def cmd_search(args) -> int:
    """에셋 검색"""
    query = args.query.lower() if args.query else ''
    tag_filter = args.tags.lower() if args.tags else ''

    registry = load_registry()
    assets = get_all_assets(registry)

    results = []
    for asset in assets:
        # 이름, ID에서 검색
        name_match = query in asset.get('name', '').lower() or query in asset.get('id', '').lower()

        # 태그에서 검색
        asset_tags = [t.lower() for t in asset.get('tags', [])]
        tag_match = any(query in t for t in asset_tags) if query else True

        # 태그 필터
        if tag_filter:
            tag_match = tag_match and any(tag_filter in t for t in asset_tags)

        if name_match or (query and tag_match) or (not query and tag_filter and tag_match):
            results.append(asset)

    if not results:
        print(f"검색 결과 없음: '{query or tag_filter}'")
        return 0

    print(f"검색 결과: {len(results)}개")
    print("-" * 60)
    for asset in results:
        tags_str = ', '.join(asset.get('tags', []))
        print(f"  [{asset['_type']}] {asset['id']}: {asset['name']}")
        print(f"         File: {asset.get('file', '')}")
        if tags_str:
            print(f"         Tags: {tags_str}")

    return 0


def cmd_list(args) -> int:
    """에셋 목록"""
    registry = load_registry()

    # 타입 필터
    if args.type == 'icons':
        assets = [dict(a, _type='icon') for a in registry.get('icons', [])]
    elif args.type == 'images':
        assets = [dict(a, _type='image') for a in registry.get('images', [])]
    else:
        assets = get_all_assets(registry)

    if not assets:
        print("등록된 에셋이 없습니다.")
        return 0

    # 출력 형식
    if args.format == 'json':
        import json
        output = [dict((k, v) for k, v in a.items() if not k.startswith('_')) for a in assets]
        print(json.dumps(output, ensure_ascii=False, indent=2))
    elif args.format == 'yaml':
        output = [dict((k, v) for k, v in a.items() if not k.startswith('_')) for a in assets]
        print(yaml.dump(output, allow_unicode=True, default_flow_style=False))
    else:
        # table 형식
        print(f"에셋 목록: {len(assets)}개")
        print("-" * 70)
        print(f"{'Type':<8} {'ID':<20} {'Name':<25} {'Tags'}")
        print("-" * 70)
        for asset in assets:
            tags_str = ', '.join(asset.get('tags', [])[:3])
            if len(asset.get('tags', [])) > 3:
                tags_str += '...'
            print(f"{asset['_type']:<8} {asset['id']:<20} {asset['name'][:25]:<25} {tags_str}")

    return 0


def cmd_info(args) -> int:
    """에셋 상세 정보"""
    asset_id = args.id
    registry = load_registry()

    asset, asset_type, _ = find_asset(registry, asset_id)
    if not asset:
        print(f"Error: 에셋을 찾을 수 없습니다 - {asset_id}")
        return 1

    print(f"에셋 정보: {asset_id}")
    print("-" * 40)
    print(f"  ID: {asset.get('id')}")
    print(f"  Name: {asset.get('name')}")
    print(f"  Type: {asset_type}")
    print(f"  File: {asset.get('file')}")
    print(f"  Source: {asset.get('source')}")
    print(f"  Tags: {', '.join(asset.get('tags', [])) or '(없음)'}")
    print(f"  Created: {asset.get('created', '?')}")
    if asset.get('original_url'):
        print(f"  URL: {asset.get('original_url')}")

    # 파일 존재 확인
    file_path = ASSETS_DIR / asset.get('file', '')
    if file_path.exists():
        size_kb = file_path.stat().st_size / 1024
        print(f"  Size: {size_kb:.1f} KB")
    else:
        print(f"  Warning: 파일이 존재하지 않습니다!")

    return 0


def cmd_delete(args) -> int:
    """에셋 삭제"""
    asset_id = args.id
    registry = load_registry()

    asset, asset_type, idx = find_asset(registry, asset_id)
    if not asset:
        print(f"Error: 에셋을 찾을 수 없습니다 - {asset_id}")
        return 1

    # 확인
    if not args.force:
        confirm = input(f"정말 삭제하시겠습니까? [{asset_id}] (y/N): ")
        if confirm.lower() != 'y':
            print("취소됨")
            return 0

    # 파일 삭제
    file_path = ASSETS_DIR / asset.get('file', '')
    if file_path.exists():
        print(f"[1/2] 파일 삭제: {file_path}")
        file_path.unlink()
    else:
        print(f"[1/2] 파일 없음 (skip)")

    # 레지스트리에서 제거
    print(f"[2/2] 레지스트리 업데이트...")
    del registry[asset_type][idx]
    save_registry(registry)

    print(f"삭제 완료: {asset_id}")
    return 0


def main():
    parser = argparse.ArgumentParser(
        description='PPT 에셋 관리 CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # 추가
  python asset-manager.py add icon.svg --id chart-line --tags "chart,data"
  python asset-manager.py add "https://example.com/bg.png" --id hero-bg

  # 검색
  python asset-manager.py search chart
  python asset-manager.py search --tags background

  # 목록
  python asset-manager.py list
  python asset-manager.py list --type icons --format table

  # 정보
  python asset-manager.py info chart-line

  # 삭제
  python asset-manager.py delete chart-line
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='명령')

    # add 명령
    add_parser = subparsers.add_parser('add', help='에셋 추가')
    add_parser.add_argument('source', help='파일 경로 또는 URL')
    add_parser.add_argument('--id', required=True, help='에셋 ID')
    add_parser.add_argument('--name', help='표시 이름 (기본: ID)')
    add_parser.add_argument('--tags', help='태그 (쉼표 구분)')
    add_parser.add_argument('--type', choices=['icons', 'images'],
                            help='에셋 타입 (자동 감지)')
    add_parser.set_defaults(func=cmd_add)

    # search 명령
    search_parser = subparsers.add_parser('search', help='에셋 검색')
    search_parser.add_argument('query', nargs='?', default='', help='검색어')
    search_parser.add_argument('--tags', help='태그 필터')
    search_parser.set_defaults(func=cmd_search)

    # list 명령
    list_parser = subparsers.add_parser('list', help='에셋 목록')
    list_parser.add_argument('--type', choices=['icons', 'images', 'all'],
                             default='all', help='타입 필터')
    list_parser.add_argument('--format', choices=['table', 'json', 'yaml'],
                             default='table', help='출력 형식')
    list_parser.set_defaults(func=cmd_list)

    # info 명령
    info_parser = subparsers.add_parser('info', help='에셋 상세 정보')
    info_parser.add_argument('id', help='에셋 ID')
    info_parser.set_defaults(func=cmd_info)

    # delete 명령
    delete_parser = subparsers.add_parser('delete', help='에셋 삭제')
    delete_parser.add_argument('id', help='에셋 ID')
    delete_parser.add_argument('-f', '--force', action='store_true',
                               help='확인 없이 삭제')
    delete_parser.set_defaults(func=cmd_delete)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    return args.func(args)


if __name__ == '__main__':
    sys.exit(main())
