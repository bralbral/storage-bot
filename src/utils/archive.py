from __future__ import annotations

import gzip
import tarfile
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path


@contextmanager
def open_gzip_without_filename(path: Path) -> Iterator[gzip.GzipFile]:
    """Open a gzip stream without leaking a temporary path into its header."""
    with path.open("wb") as output:
        with gzip.GzipFile(
            filename="",
            fileobj=output,
            mode="wb",
        ) as compressed:
            yield compressed


@contextmanager
def open_tar_gz(path: Path) -> Iterator[tarfile.TarFile]:
    """Create a streaming tar.gz without an embedded gzip filename."""
    with open_gzip_without_filename(path) as compressed:
        with tarfile.open(fileobj=compressed, mode="w|") as archive:
            yield archive
