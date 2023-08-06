# -*- coding: utf-8 -*-
# Copyright © 2021 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import sys

from contrast.extern.six import PY2

from contrast.extern.wrapt import register_post_import_hook
from contrast.agent.policy import patch_manager
from contrast.utils.patch_utils import patch_cls_or_instance


def noop_intern(orig_func, patch_policy, string):
    """
    Defeat interning by returning the original string

    sys.intern takes no kwargs
    """
    return string


def patch_sys(module):
    if not PY2:
        # sys.intern is PY3 only
        patch_cls_or_instance(module, "intern", noop_intern)


def register_patches():
    register_post_import_hook(patch_sys, "sys")


def reverse_patches():
    # sys is always imported, no need to check
    patch_manager.reverse_patches_by_owner(sys)
