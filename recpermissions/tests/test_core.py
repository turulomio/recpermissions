import pytest
import tempfile
import shutil
import os
import pwd
import grp
import stat

# It's good practice to make the test runner find the modules.
# This assumes you run pytest or unittest from the project root.
from recpermissions.core import recpermissions, remove_empty_directories, main_recpermissions, main_remove_empty_directories



@pytest.fixture
def test_fs(monkeypatch):
    """Set up a temporary directory with a file structure for each test."""
    # Suppress print output for all tests using this fixture
    monkeypatch.setattr('builtins.print', lambda *args, **kwargs: None)

    test_dir = tempfile.mkdtemp()
    user = pwd.getpwuid(os.getuid()).pw_name
    group = grp.getgrgid(os.getgid()).gr_name

    # Create a structure inside the temp directory
    # test_dir/
    # ├── file1.txt
    # ├── empty_dir/
    # └── sub_dir/
    #     ├── file2.txt
    #     └── deep_empty_dir/
    fs = {
        "test_dir": test_dir,
        "user": user,
        "group": group,
        "file1": os.path.join(test_dir, "file1.txt"),
        "empty_dir": os.path.join(test_dir, "empty_dir"),
        "sub_dir": os.path.join(test_dir, "sub_dir"),
        "file2": os.path.join(test_dir, "sub_dir", "file2.txt"),
        "deep_empty_dir": os.path.join(test_dir, "sub_dir", "deep_empty_dir"),
    }

    with open(fs["file1"], "w") as f:
        f.write("hello")
    os.makedirs(fs["empty_dir"])
    os.makedirs(fs["sub_dir"])
    with open(fs["file2"], "w") as f:
        f.write("world")
    os.makedirs(fs["deep_empty_dir"])

    yield fs

    # Teardown: remove the temporary directory
    shutil.rmtree(test_dir)

def get_permissions(path):
    """Helper to get octal permissions from a path."""
    return oct(stat.S_IMODE(os.stat(path).st_mode))

def get_ownership(path):
    """Helper to get user/group from a path."""
    file_stat = os.stat(path)
    return (
        pwd.getpwuid(file_stat.st_uid).pw_name,
        grp.getgrgid(file_stat.st_gid).gr_name
    )

def test_recpermissions(test_fs):
    """Test the main recpermissions logic."""
    # Change permissions and ownership
    file_perms = "640"
    dir_perms = "750"

    # The user/group will likely be the same, but this tests the logic.
    recpermissions(
        user=test_fs["user"],
        group=test_fs["group"],
        files=file_perms,
        directories=dir_perms,
        absolute_path=test_fs["test_dir"]
    )

    # Assert permissions on directories
    assert get_permissions(test_fs["test_dir"])[-3:] == dir_perms
    assert get_permissions(test_fs["sub_dir"])[-3:] == dir_perms
    assert get_permissions(test_fs["empty_dir"])[-3:] == dir_perms

    # Assert permissions on files
    assert get_permissions(test_fs["file1"])[-3:] == file_perms
    assert get_permissions(test_fs["file2"])[-3:] == file_perms

    # Assert ownership (user and group)
    assert get_ownership(test_fs["test_dir"]) == (test_fs["user"], test_fs["group"])
    assert get_ownership(test_fs["file1"]) == (test_fs["user"], test_fs["group"])
    assert get_ownership(test_fs["sub_dir"]) == (test_fs["user"], test_fs["group"])
    assert get_ownership(test_fs["file2"]) == (test_fs["user"], test_fs["group"])

def test_remove_empty_directories_pretend(test_fs):
    """Test remove_empty_directories in pretend mode."""
    remove_empty_directories(pretend=True, absolute_path=test_fs["test_dir"])

    # Assert that empty directories still exist
    assert os.path.exists(test_fs["empty_dir"])
    assert os.path.exists(test_fs["deep_empty_dir"])

def test_remove_empty_directories_real(test_fs):
    """Test remove_empty_directories actually removes dirs."""
    # The function walks from top down, so it won't remove nested empty dirs
    # in one pass. We can call it multiple times to simulate real-world usage
    # where a user might run it until no more dirs are deleted.

    # First pass removes deep_empty_dir
    remove_empty_directories(pretend=False, absolute_path=test_fs["test_dir"])
    assert not os.path.exists(test_fs["deep_empty_dir"])
    assert not os.path.exists(test_fs["empty_dir"])
    assert os.path.exists(test_fs["sub_dir"])  # Now empty, but not removed yet


    # Remove file2 and pass again
    os.remove(test_fs["file2"])
    remove_empty_directories(pretend=False, absolute_path=test_fs["test_dir"])
    assert not os.path.exists(test_fs["sub_dir"])



    # Assert that non-empty dirs and files are untouched
    assert os.path.exists(test_fs["test_dir"])
    assert os.path.exists(test_fs["file1"])

def test_main_recpermissions_no_args(monkeypatch):
    """Test that main_recpermissions exits when no arguments are provided."""
    # Prevent sys.argv from being used by argparse
    # monkeypatch.setattr('sys.argv', ['recpermissions'])
    with pytest.raises(SystemExit) as e:
        main_recpermissions()
    assert e.type == SystemExit
    assert e.value.code == 2

def test_main_remove_empty_directories_no_args(monkeypatch):
    """Test that main_remove_empty_directories exits when no arguments are provided."""
    # monkeypatch.setattr('sys.argv', ['remove-empty-dirs'])
    with pytest.raises(SystemExit) as e:
        main_remove_empty_directories()
    assert e.type == SystemExit
    assert e.value.code == 2
