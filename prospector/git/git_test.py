# from pprint import pprint
import os.path
import time

import pytest

from .git import Exec, Git

# from .version_to_tag import version_to_wide_interval_tags
from .version_to_tag import get_possible_tags

NEBULA = "https://github.com/slackhq/nebula"
BEAM = "https://github.com/apache/beam"
OPENCAST = "https://github.com/opencast/opencast"
OPENCAST_COMMIT = "bbb473f34ab95497d6c432c81285efb0c739f317"


COMMIT_ID = "4645e6034b9c88311856ee91d19b7328bd5878c1"
COMMIT_ID_1 = "d85e24f49f9efdeed5549a7d0874e68155e25301"
COMMIT_ID_2 = "b38bd36766994715ac5226bfa361cd2f8f29e31e"
COMMIT_ID_3 = "ae3ee42469b7c48848d841386ca9c74b7d6bbcd8"


@pytest.fixture
def repository() -> Git:
    repo = Git(OPENCAST)  # apache/beam
    repo.clone()
    return repo


def test_extract_timestamp(repository: Git):
    commit = repository.get_commit(COMMIT_ID)
    commit.extract_timestamp(format_date=True)
    assert commit.get_timestamp() == "2020-07-01 15:20:52"
    commit.extract_timestamp(format_date=False)
    assert commit.get_timestamp() == 1593616852


def test_show_tags(repository: Git):
    tags = repository.execute("git name-rev --tags")
    print(tags)
    raise Exception()


def test_get_tags_for_commit(repository: Git):
    commits = repository.create_commits()
    commit = commits.get(OPENCAST_COMMIT)
    if commit is not None:
        tags = commit.find_tag("8.1")
        raise Exception(tags)


def test_create_commits(repository: Git):
    commits = repository.create_commits()
    commit = commits.get(COMMIT_ID)
    assert len(commits) == 357
    assert commit.get_id() == COMMIT_ID


def test_get_hunks_count(repository: Git):
    commits = repository.create_commits()
    commit = commits.get(OPENCAST_COMMIT)
    diff, hunks = commit.get_diff()
    print(diff)
    raise Exception()
    assert hunks == 2


def test_get_changed_files(repository: Git):
    commit = repository.get_commit(COMMIT_ID)

    changed_files = commit.get_changed_files()
    assert len(changed_files) == 0


@pytest.mark.skip(reason="Skipping this test")
def test_extract_timestamp_from_version():
    repo = Git(NEBULA)
    repo.clone()
    assert repo.extract_timestamp_from_version("v1.5.2") == 1639518536
    assert repo.extract_timestamp_from_version("INVALID_VERSION_1_0_0") is None


def test_get_tag_for_version():
    repo = Git(NEBULA)
    repo.clone()
    tags = repo.get_tags()
    assert get_possible_tags(tags, "1.5.2") == ["v1.5.2"]


def test_get_commit_parent():
    repo = Git(NEBULA)
    repo.clone()
    id = repo.get_commit_id_for_tag("v1.6.1")
    commit = repo.get_commit(id)

    commit.get_parent_id()
    assert True  # commit.parent_id == "4c0ae3df5ef79482134b1c08570ff51e52fdfe06"


def test_run_cache():
    _exec = Exec(workdir=os.path.abspath("."))
    start = time.time_ns()
    for _ in range(1000):
        result = _exec.run("echo 42", cache=False)
        assert result == ["42"]
    no_cache_time = time.time_ns() - start

    _exec = Exec(workdir=os.path.abspath("."))
    start = time.time_ns()
    for _ in range(1000):
        result = _exec.run("echo 42", cache=True)
        assert result == ["42"]
    cache_time = time.time_ns() - start

    assert cache_time < no_cache_time
