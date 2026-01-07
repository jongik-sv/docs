#!/usr/bin/env python3
"""
Template Migration Script
Migrates templates from old structure to new category-based structure.
"""

import os
import shutil
import yaml
from pathlib import Path
from datetime import datetime

# Paths
OLD_TEMPLATES_DIR = Path("C:/project/docs/.claude/skills/ppt-gen/templates/contents/templates")
OLD_THUMBNAILS_DIR = Path("C:/project/docs/.claude/skills/ppt-gen/templates/contents/thumbnails")
NEW_TEMPLATES_DIR = Path("C:/project/docs/templates/contents/templates")
NEW_THUMBNAILS_DIR = Path("C:/project/docs/templates/contents/thumbnails")

# Migration mapping: old_name -> (category, new_name, original_theme)
MIGRATION_MAP = {
    # Cover
    "deepgreen-cover1": ("cover", "cover-centered1", "deepgreen"),
    "brandnew-cover1": ("cover", "cover-photo1", "brandnew"),
    "cover1": ("cover", "cover-simple1", None),

    # TOC
    "deepgreen-toc1": ("toc", "toc-3col1", "deepgreen"),
    "brandnew-toc1": ("toc", "toc-list-image1", "brandnew"),
    "toc1": ("toc", "toc-simple1", None),

    # Section
    "deepgreen-section1": ("section", "section-number1", "deepgreen"),
    "brandnew-section1": ("section", "section-textured1", "brandnew"),

    # Comparison
    "comparison1": ("comparison", "comparison-2col1", None),
    "brandnew-comparison1": ("comparison", "comparison-2col-image1", "brandnew"),
    "pros-cons1": ("comparison", "pros-cons1", None),

    # Process
    "deepgreen-process1": ("process", "process-circle1", "deepgreen"),
    "brandnew-process1": ("process", "process-3step-result1", "brandnew"),
    "process-flow1": ("process", "process-flow1", None),
    "deepgreen-cylinder1": ("process", "process-cylinder1", "deepgreen"),
    "deepgreen-honeycomb1": ("process", "process-honeycomb1", "deepgreen"),

    # Chart
    "deepgreen-chart1": ("chart", "chart-bar-table1", "deepgreen"),

    # Stats
    "deepgreen-stats1": ("stats", "stats-dotgrid1", "deepgreen"),
    "stat-cards1": ("stats", "stat-cards1", None),

    # Grid
    "deepgreen-grid4col1": ("grid", "grid-4col-icon1", "deepgreen"),
    "brandnew-grid3col1": ("grid", "grid-3col-image1", "brandnew"),
    "feature-grid1": ("grid", "feature-grid1", None),

    # Diagram
    "deepgreen-matrix1": ("diagram", "matrix-2x21", "deepgreen"),
    "deepgreen-cycle1": ("diagram", "cycle-circular1", "deepgreen"),
    "deepgreen-dotmap1": ("diagram", "dotmap-text1", "deepgreen"),
    "brandnew-growth1": ("diagram", "growth-circles1", "brandnew"),
    "brandnew-flow1": ("diagram", "flow-text1", "brandnew"),

    # Timeline
    "timeline1": ("timeline", "timeline1", None),

    # Content
    "deepgreen-imagetext1": ("content", "image-text1", "deepgreen"),

    # Quote
    "brandnew-quote1": ("quote", "quote-centered1", "brandnew"),

    # Closing
    "brandnew-closing1": ("closing", "closing-thankyou1", "brandnew"),
}


def migrate_template(old_name: str, category: str, new_name: str, original_theme: str | None):
    """Migrate a single template file."""
    old_yaml_path = OLD_TEMPLATES_DIR / f"{old_name}.yaml"
    new_yaml_path = NEW_TEMPLATES_DIR / category / f"{new_name}.yaml"

    if not old_yaml_path.exists():
        print(f"  [SKIP] {old_name}.yaml not found")
        return False

    # Read old YAML
    with open(old_yaml_path, 'r', encoding='utf-8') as f:
        content = yaml.safe_load(f)

    # Update metadata
    if 'content_template' in content:
        content['content_template']['id'] = new_name
        content['content_template']['version'] = "3.0"
        content['content_template']['migrated_from'] = old_name
        content['content_template']['migrated_at'] = datetime.now().isoformat()
        if original_theme:
            content['content_template']['original_theme'] = original_theme

    # Update thumbnail path
    if 'thumbnail' in content:
        content['thumbnail'] = f"thumbnails/{category}/{new_name}.png"

    # Write new YAML
    new_yaml_path.parent.mkdir(parents=True, exist_ok=True)
    with open(new_yaml_path, 'w', encoding='utf-8') as f:
        yaml.dump(content, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

    print(f"  [OK] {old_name}.yaml -> {category}/{new_name}.yaml")
    return True


def migrate_thumbnail(old_name: str, category: str, new_name: str):
    """Migrate a single thumbnail file."""
    old_png_path = OLD_THUMBNAILS_DIR / f"{old_name}.png"
    new_png_path = NEW_THUMBNAILS_DIR / category / f"{new_name}.png"

    if not old_png_path.exists():
        print(f"  [SKIP] {old_name}.png not found")
        return False

    new_png_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(old_png_path, new_png_path)

    print(f"  [OK] {old_name}.png -> {category}/{new_name}.png")
    return True


def main():
    print("=" * 60)
    print("Template Migration Script")
    print("=" * 60)

    template_count = 0
    thumbnail_count = 0

    print("\n[1/2] Migrating YAML templates...")
    for old_name, (category, new_name, original_theme) in MIGRATION_MAP.items():
        if migrate_template(old_name, category, new_name, original_theme):
            template_count += 1

    print(f"\n[2/2] Migrating thumbnails...")
    for old_name, (category, new_name, _) in MIGRATION_MAP.items():
        if migrate_thumbnail(old_name, category, new_name):
            thumbnail_count += 1

    print("\n" + "=" * 60)
    print(f"Migration complete!")
    print(f"  Templates migrated: {template_count}/{len(MIGRATION_MAP)}")
    print(f"  Thumbnails migrated: {thumbnail_count}/{len(MIGRATION_MAP)}")
    print("=" * 60)


if __name__ == "__main__":
    main()
