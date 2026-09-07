"""
Materials Synchronization Engine

Synchronizes project-native .FCMat material cards from the repository's `materials/` directory
into FreeCAD's native User Material Library at `~/.local/share/FreeCAD/v1-1/Material/maker/`.

Uses file symlinks so modifications to repo material cards are immediately live in FreeCAD
without requiring manual re-copying or re-exporting.
"""

import os
import sys
import shutil
from pathlib import Path


def get_default_user_material_dir():
    """
    Returns the standard FreeCAD 1.1+ User Material Library path:
    `~/.local/share/FreeCAD/v1-1/Material`
    """
    return os.path.expanduser("~/.local/share/FreeCAD/v1-1/Material")


def get_repo_materials_dir():
    """
    Returns the absolute path to `materials/` in the maker repository.
    """
    curr = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.abspath(os.path.join(curr, "..", "..", "..", ".."))
    mat_dir = os.path.join(repo_root, "materials")
    return mat_dir


def sync_materials(user_mat_dir=None, repo_mat_dir=None, clean=True, verbose=True):
    """
    Synchronizes all .FCMat files from `repo_mat_dir` into `user_mat_dir/maker/`.
    
    Parameters:
      user_mat_dir: Target directory (default: ~/.local/share/FreeCAD/v1-1/Material)
      repo_mat_dir: Source directory (default: maker/materials)
      clean: If True, removes orphaned symlinks in target directory
      verbose: If True, prints status messages
      
    Returns:
      Dictionary with counts and lists of created, existing, and removed links.
    """
    if user_mat_dir is None:
        user_mat_dir = get_default_user_material_dir()
    if repo_mat_dir is None:
        repo_mat_dir = get_repo_materials_dir()

    target_root = os.path.join(user_mat_dir, "maker")
    os.makedirs(target_root, exist_ok=True)

    # Collect source cards: {rel_path: abs_path}
    source_cards = {}
    for root, dirs, files in os.walk(repo_mat_dir):
        for f in files:
            if f.endswith(".FCMat"):
                abs_src = os.path.join(root, f)
                rel_src = os.path.relpath(abs_src, repo_mat_dir)
                source_cards[rel_src] = abs_src

    stats = {
        "created": [],
        "existing": [],
        "updated": [],
        "removed": [],
        "total_source": len(source_cards),
    }

    # Create/update symlinks in target_root
    for rel_path, abs_src in source_cards.items():
        dest_path = os.path.join(target_root, rel_path)
        dest_dir = os.path.dirname(dest_path)
        os.makedirs(dest_dir, exist_ok=True)

        if os.path.islink(dest_path):
            current_target = os.readlink(dest_path)
            if os.path.abspath(current_target) == os.path.abspath(abs_src):
                stats["existing"].append(rel_path)
                continue
            else:
                os.unlink(dest_path)
                stats["updated"].append(rel_path)
        elif os.path.exists(dest_path):
            # If a regular file or dir exists, replace with symlink
            if os.path.isdir(dest_path):
                shutil.rmtree(dest_path)
            else:
                os.remove(dest_path)
            stats["updated"].append(rel_path)
        else:
            stats["created"].append(rel_path)

        os.symlink(abs_src, dest_path)

    # Clean up orphaned symlinks
    if clean and os.path.exists(target_root):
        for root, dirs, files in os.walk(target_root, topdown=False):
            for f in files:
                dest_path = os.path.join(root, f)
                rel_path = os.path.relpath(dest_path, target_root)
                if rel_path not in source_cards:
                    if os.path.islink(dest_path) or os.path.isfile(dest_path):
                        os.remove(dest_path)
                        stats["removed"].append(rel_path)
            # Remove empty subfolders
            if not os.listdir(root) and root != target_root:
                try:
                    os.rmdir(root)
                except OSError:
                    pass

    if verbose:
        print(f"Materials Sync Summary -> {target_root}:")
        print(f"  Source cards: {stats['total_source']}")
        print(f"  Links created: {len(stats['created'])}")
        print(f"  Links up-to-date: {len(stats['existing'])}")
        print(f"  Links updated: {len(stats['updated'])}")
        print(f"  Orphans removed: {len(stats['removed'])}")

    return stats


if __name__ == "__main__":
    sync_materials(verbose=True)
    os._exit(0)

