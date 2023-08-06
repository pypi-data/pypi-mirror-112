#
# Copyright (c) 2015-2020 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_skin.resources module

This module provides a "resources" TALES extension, which can be used to include Fanstatic
resources into an HTML page from a Chameleon template; selected resources are based on an
IResources multi-adapter.
"""

from zope.component import getAdapters
from zope.interface import Interface

from pyams_layer.interfaces import IResources
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config
from pyams_utils.interfaces.tales import ITALESExtension
from pyams_viewlet.manager import get_weight


__docformat__ = 'restructuredtext'


@adapter_config(name='resources',
                required=(Interface, Interface, Interface),
                provides=ITALESExtension)
class ResourcesTalesExtension(ContextRequestViewAdapter):
    """tales:resources TALES extension"""

    def render(self, context=None):
        """Render Fanstatic resources"""
        if context is None:
            context = self.context
        for _name, adapter in sorted(getAdapters((context, self.request, self.view),
                                                 IResources),
                                     key=get_weight):
            for resource in adapter.resources:
                resource.need()
