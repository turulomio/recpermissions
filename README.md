# Recpermissions [![PyPI - Downloads](https://img.shields.io/pypi/dm/recpermissions?label=Pypi%20downloads)](https://pypi.org/project/recpermissions/)   [![Tests](https://github.com/turulomio/recpermissions/actions/workflows/ci.yml/badge.svg)](https://github.com/turulomio/recpermissions/actions/workflows/ci.yml)


Recpermissions is a Python script to change Linux permissions and ownership in one step. It can delete empty directories when necessary.

This script doesn't work on Windows.

*   **Github web page**: <https://github.com/turulomio/recpermissions>
*   **Pypi web page**: <https://pypi.org/project/recpermissions/>
*   **Gentoo ebuild**: If you use Gentoo you can find an ebuild in <https://github.com/turulomio/myportage/tree/master/app-admin/recpermissions>


## Usage

### `recpermissions`

Recursively changes the ownership and permissions for all files and directories within a given absolute path.

```bash
recpermissions --user <user> --group <group> --files <PERM> --directories <PERM> <absolute_path>
```

**Arguments:**
*   `--user <user>`: The new owner for the files and directories.
*   `--group <group>`: The new group for the files and directories.
*   `--files <PERM>`: The octal permissions to set for all files (e.g., `644`).
*   `--directories <PERM>`: The octal permissions to set for all directories (e.g., `755`).
*   `<absolute_path>`: The absolute path to the directory to process.

### `remove-empty-dirs`

Recursively finds and deletes empty directories within a given path.

```bash
remove-empty-dirs [--pretend] <absolute_path>
```

**Arguments:**
*   `--pretend`: If used, the script will only list the empty directories that would be deleted, without actually deleting them.
*   `<absolute_path>`: The absolute path to the directory to scan for empty subdirectories.
