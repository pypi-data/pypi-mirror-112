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

"""PyAMS_zmi.controlpanel module

This module defines views and content providers which are used to get access to the local
site manager contents view.
"""

from zope.interface import implementer

from pyams_layer.interfaces import IPyAMSLayer
from pyams_pagelet.pagelet import pagelet_config
from pyams_security.interfaces.base import VIEW_SYSTEM_PERMISSION
from pyams_site.interfaces import ISiteRoot
from pyams_table.interfaces import IColumn, IValues
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config
from pyams_viewlet.manager import viewletmanager_config
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.table import ITableWithActions
from pyams_zmi.interfaces.viewlet import IControlPanelMenu, IUtilitiesMenu
from pyams_zmi.table import NameColumn, Table, TableAdminView
from pyams_zmi.zmi.viewlet.menu import NavigationMenuItem


__docformat__ = 'restructuredtext'

from pyams_zmi import _


@viewletmanager_config(name='utilities.menu', context=ISiteRoot, layer=IAdminLayer,
                       manager=IControlPanelMenu, weight=10,
                       permission=VIEW_SYSTEM_PERMISSION, provides=IUtilitiesMenu)
class UtilitiesMenuItem(NavigationMenuItem):
    """Utilities menu item"""

    label = _("Utilities")
    icon_class = 'fab fa-codepen'
    href = '#utilities.html'


@implementer(ITableWithActions)
class UtilitiesTable(Table):
    """Utilities table list"""


@adapter_config(required=(ISiteRoot, IAdminLayer, UtilitiesTable),
                provides=IValues)
class UtilitiesTableValues(ContextRequestViewAdapter):
    """Utilities tables values adapter"""

    @property
    def values(self):
        """Utilities table values"""
        sm = self.context.getSiteManager()  # pylint: disable=invalid-name
        yield from sm.values()


@adapter_config(name='name',
                required=(ISiteRoot, IAdminLayer, UtilitiesTable),
                provides=IColumn)
class UtilityNameColumn(NameColumn):
    """Utility name column"""


@pagelet_config(name='utilities.html', context=ISiteRoot, layer=IPyAMSLayer,
                permission=VIEW_SYSTEM_PERMISSION)
class UtilitiesView(TableAdminView):
    """Utilities view"""

    title = _("Control panel")
    table_class = UtilitiesTable
    table_label = _("Site utilities")
