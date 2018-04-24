"""Implementation of core routines for thoth-package-extract."""

import logging
import os
import tempfile
import typing
from shlex import quote

from .handlers import HandlerBase
from .image import construct_rootfs
from .image import download_image
from .image import run_analyzers

_LOGGER = logging.getLogger(__name__)


def extract_buildlog(input_text: str) -> typing.List[dict]:
    """Extract Docker image build log and get all installed packages based on ecosystem."""
    result = []
    for handler in HandlerBase.instantiate_handlers():
        result.append({
            'handler': handler.__class__.__name__.lower(),
            'result': handler.run(input_text)
        })

    return result


def extract_image(image_name: str, timeout: int = None, *, registry_credentials: str = None,
                  tls_verify: bool=True) -> dict:
    """Extract dependencies from an image."""
    image_name = quote(image_name)
    with tempfile.TemporaryDirectory() as dir_path:
        download_image(
            image_name,
            dir_path,
            timeout=timeout or None,
            registry_credentials=registry_credentials or None,
            tls_verify=tls_verify
        )

        rootfs_path = os.path.join(dir_path, 'rootfs')
        construct_rootfs(dir_path, rootfs_path)

        return run_analyzers(rootfs_path)
