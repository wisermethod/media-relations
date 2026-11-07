"""Caller-path screening shared by Campaign Plan's two entry scripts."""

from pathlib import Path
import re


def protected(path):
    return any(part.casefold() == "memory" or
               re.match(r"^\.env(?:\.|$)", part, re.I) for part in path.parts)


def canonical_path(value):
    path = Path(value)
    if not path.is_absolute():
        raise ValueError("Path must be absolute; see --help")
    if protected(path):
        raise ValueError("Protected path; supply a work-product path")
    # Resolve the deepest existing ancestor strictly. A dangling link or an
    # inaccessible ancestor is not a cleared path, even for a new destination.
    ancestor, tail = path, []
    try:
        while True:
            try:
                ancestor.lstat()
                break
            except FileNotFoundError:
                if ancestor == ancestor.parent:
                    raise
                tail.append(ancestor.name)
                ancestor = ancestor.parent
        resolved = ancestor.resolve(strict=True).joinpath(*reversed(tail)).resolve(strict=False)
    except (OSError, RuntimeError) as error:
        raise ValueError("Path cannot be canonicalized; repair missing ancestors, links or permissions") from error
    if protected(resolved):
        raise ValueError("Protected path; supply a work-product path")
    return resolved


def inside_directory(path, directory, stat=None):
    """Compare filesystem identities, including aliases spelling no common path."""
    stat = stat or (lambda item: item.stat())
    own = stat(directory)
    identity = (own.st_dev, own.st_ino)
    for ancestor in (path, *path.parents):
        try:
            info = stat(ancestor)
        except FileNotFoundError:
            continue
        if (info.st_dev, info.st_ino) == identity:
            return True
    return False


def screen_path(value, *, file=False, directory=False, destination=None):
    path = canonical_path(value)
    if destination is not None:
        if inside_directory(path, destination):
            raise ValueError("PDF output resolves inside this skill; use the owning root's work directory")
        if path.exists() or path.is_symlink():
            raise ValueError("PDF destination already exists; choose a fresh HTML/PDF version")
    if file and not path.is_file():
        raise ValueError("Input is not a regular file; supply a readable source; see --help")
    if directory and not path.is_dir():
        raise ValueError("Input is not a directory; supply the composed base plugin; see --help")
    return path


def self_test():
    from types import SimpleNamespace
    from unittest.mock import patch

    for spelling in ['relative.txt', '/example/memory/text.txt', '/example/.env.local']:
        try:
            canonical_path(spelling)
        except ValueError:
            pass
        else:
            raise AssertionError("Uncleared path accepted")
    # Synthetic inode aliases exercise the actual ancestry predicate without
    # creating files, hard links or platform-specific directory aliases.
    own, alias = Path('/primitive'), Path('/alias/new/output.pdf')
    def stat(item):
        if item == own or item == Path('/alias'):
            return SimpleNamespace(st_dev=7, st_ino=11)
        if item in {alias, alias.parent}:
            raise FileNotFoundError
        return SimpleNamespace(st_dev=8, st_ino=11)
    assert inside_directory(alias, own, stat)
    assert not inside_directory(Path('/elsewhere/output.pdf'), own, stat)
    with patch.object(Path, 'lstat', side_effect=PermissionError):
        try:
            canonical_path('/unreadable/new.pdf')
        except ValueError:
            pass
        else:
            raise AssertionError("Inaccessible ancestor accepted")
    with patch.object(Path, 'resolve', return_value=Path('/example/memory/hidden.txt')):
        try:
            canonical_path(__file__)
        except ValueError:
            pass
        else:
            raise AssertionError("Protected resolved alias accepted")
    return 'absolute and canonical protected paths; device/inode destination ancestry'
