# Orca
#
# Copyright 2005-2008 Sun Microsystems Inc.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., Franklin Street, Fifth Floor,
# Boston MA  02110-1301 USA.

"""Custom script for StarOffice and OpenOffice."""

__id__        = "$Id: braille_generator.py 4294 2008-10-15 17:29:05Z joanied $"
__version__   = "$Revision: 4294 $"
__date__      = "$Date: 2008-10-15 13:29:05 -0400 (Wed, 15 Oct 2008) $"
__copyright__ = "Copyright (c) 2005-2008 Sun Microsystems Inc."
__license__   = "LGPL"

import pyatspi

import orca.braille as braille
import orca.braillegenerator as braillegenerator
import orca.settings as settings

class BrailleGenerator(braillegenerator.BrailleGenerator):
    """Overrides _getBrailleRegionsForTableCellRow so that , when we are
    in a spread sheet, we can braille the dynamic row and column headers
    (assuming they are set).
    Overrides _getBrailleRegionsForTableCell so that, when we are in
    a spread sheet, we can braille the location of the table cell as well
    as the contents.
    """

    def __init__(self, script):
        braillegenerator.BrailleGenerator.__init__(self, script)

    def _getTextForRole(self, obj, role=None):
        if obj.getRole() == pyatspi.ROLE_DOCUMENT_FRAME \
           or role == pyatspi.ROLE_DOCUMENT_FRAME:
            return None

        return braillegenerator.BrailleGenerator.\
            _getTextForRole(self, obj, role)

    def _getBrailleRegionsForList(self, obj):
        """Get the braille for a focused list.

        Arguments:
        - obj: the list

        Returns a list where the first element is a list of Regions to
        display and the second element is the Region which should get
        focus.
        """

        self._debugGenerator("soffice: _getBrailleRegionsForList", obj)

        if not obj.getState().contains(pyatspi.STATE_FOCUSABLE):
            return braillegenerator.BrailleGenerator.\
                       _getBrailleRegionsForList(self, obj)

        text = ""
        label = self._script.getDisplayedLabel(obj)
        if not label:
            label = obj.name
        if label and len(label):
            text = self._script.appendString(text, label)

        text = self._script.appendString(text, self._getTextForRole(obj))
        text = self._script.appendString(text,
                                         self._getTextForRequiredObject(obj))
        regions = []
        componentRegion = braille.Component(obj, text)
        regions.append(componentRegion)

        return [regions, componentRegion]

    def _getBrailleRegionsForTableCellRow(self, obj):
        """Get the braille for a table cell row or a single table cell
        if settings.readTableCellRow is False.

        Arguments:
        - obj: the table cell

        Returns a list where the first element is a list of Regions to display
        and the second element is the Region which should get focus.
        """

        focusRegion = None
        regions = []

        # Check to see if this spread sheet cell has either a dynamic
        # column heading or row heading (or both) associated with it.
        # If it does, then braille those first before brailling the
        # cell contents.
        #
        table = self._script.getTable(obj)
        parent = obj.parent
        try:
            parentTable = parent.queryTable()
        except NotImplementedError:
            parentTable = None

        index = self._script.getCellIndex(obj)
        if "lastColumn" in self._script.pointOfReference and \
              self._script.pointOfReference["lastColumn"] != \
              parentTable.getColumnAtIndex(index):
            if table in self._script.dynamicColumnHeaders:
                row = self._script.dynamicColumnHeaders[table]
                header = self._script.getDynamicRowHeaderCell(obj, row)
                try:
                    headerText = header.queryText()
                except:
                    headerText = None

                if header.childCount > 0:
                    for child in header:
                        text = self._script.getText(child, 0, -1)
                        if text:
                            regions.append(braille.Region(" " + text + " "))
                elif headerText:
                    text = self._script.getText(header, 0, -1)
                    if text:
                        regions.append(braille.Region(" " + text + " "))

        if "lastRow" in self._script.pointOfReference and \
              self._script.pointOfReference['lastRow'] != \
              parentTable.getRowAtIndex(index):
            if table in self._script.dynamicRowHeaders:
                column = self._script.dynamicRowHeaders[table]
                header = self._script.getDynamicColumnHeaderCell(obj, column)
                try:
                    headerText = header.queryText()
                except:
                    headerText = None

                if header.childCount > 0:
                    for child in header:
                        text = self._script.getText(child, 0, -1)
                        if text:
                            regions.append(braille.Region(" " + text + " "))
                elif headerText:
                    text = self._script.getText(header, 0, -1)
                    if text:
                        regions.append(braille.Region(" " + text + " "))

        if self._script.isSpreadSheetCell(obj):

            # Adding in a check here to make sure that the parent is a
            # valid table. It's possible that the parent could be a
            # table cell too (see bug #351501).
            #
            if settings.readTableCellRow and parentTable:
                rowRegions = []
                savedBrailleVerbosityLevel = settings.brailleVerbosityLevel
                settings.brailleVerbosityLevel = \
                                             settings.VERBOSITY_LEVEL_BRIEF

                parent = obj.parent
                index = self._script.getCellIndex(obj)
                row = parentTable.getRowAtIndex(index)
                column = parentTable.getColumnAtIndex(index)

                # This is an indication of whether we should speak all the
                # table cells (the user has moved focus up or down a row),
                # or just the current one (focus has moved left or right in
                # the same row).
                #
                speakAll = True
                if "lastRow" in self._script.pointOfReference and \
                    "lastColumn" in self._script.pointOfReference:
                    pointOfReference = self._script.pointOfReference
                    speakAll = \
                        (pointOfReference["lastRow"] != row) or \
                           ((row == 0 or row == parentTable.nRows-1) and \
                            pointOfReference["lastColumn"] == column)

                if speakAll:
                    [startIndex, endIndex] = \
                        self._script.getSpreadSheetRowRange(obj)
                    for i in range(startIndex, endIndex+1):
                        cell = parentTable.getAccessibleAt(row, i)
                        showing = cell.getState().contains( \
                                        pyatspi.STATE_SHOWING)
                        if showing:
                            [cellRegions, focusRegion] = \
                                self._getBrailleRegionsForTableCell(cell)
                            if len(rowRegions):
                                rowRegions.append(braille.Region(" "))
                            rowRegions.append(cellRegions[0])
                    regions.extend(rowRegions)
                    settings.brailleVerbosityLevel = savedBrailleVerbosityLevel
                else:
                    [cellRegions, focusRegion] = \
                                self._getBrailleRegionsForTableCell(obj)
                    regions.extend(cellRegions)
            else:
                [cellRegions, focusRegion] = \
                                self._getBrailleRegionsForTableCell(obj)
                regions.extend(cellRegions)
            regions = [regions, focusRegion]
        else:
            [cellRegions, focusRegion] = \
                braillegenerator.BrailleGenerator.\
                    _getBrailleRegionsForTableCellRow(self, obj)
            regions.extend(cellRegions)
            regions = [regions, focusRegion]

        return regions

    def _getBrailleRegionsForTableCell(self, obj):
        """Get the braille for a table cell. If this isn't inside a
        spread sheet, just return the regions returned by the default
        table cell braille handler.

        Arguments:
        - obj: the table cell

        Returns a list where the first element is a list of Regions to display
        and the second element is the Region which should get focus.
        """

        if self._script.isSpreadSheetCell(obj):
            if self._script.inputLineForCell == None:
                self._script.inputLineForCell = \
                            self._script.locateInputLine(obj)

            regions = []
            text = self._script.getDisplayedText(obj)
            componentRegion = braille.Component(obj, text)
            regions.append(componentRegion)

            # If the spread sheet table cell has something in it, then we
            # want to append the name of the cell (which will be its location).
            # Note that if the cell was empty, then
            # self._script.getDisplayedText will have already done this for us.
            #
            try:
                if obj.queryText():
                    objectText = self._script.getText(obj, 0, -1)
                    if objectText and len(objectText) != 0:
                        regions.append(braille.Region(" " + obj.name))
            except NotImplementedError:
                pass

            return [regions, componentRegion]

        else:
            # Check to see how many children this table cell has. If it's
            # just one (or none), then pass it on to the superclass to be
            # processed.
            #
            # If it's more than one, then get the braille regions for each
            # child, and call this method again.
            #
            if obj.childCount <= 1:
                regions = braillegenerator.BrailleGenerator.\
                              _getBrailleRegionsForTableCell(self, obj)
            else:
                regions = []
                for child in obj:
                    [cellRegions, focusRegion] = \
                                self._getBrailleRegionsForTableCell(child)
                    regions.extend(cellRegions)
                return [regions, focusRegion]

        return regions

    def _getBrailleRegionsForScrollPane(self, obj):
        """Get the braille for a scroll pane.

        Arguments:
        - obj: the scroll pane

        Returns a list where the first element is a list of Regions to display
        and the second element is the Region which should get focus.
        """

        self._debugGenerator("soffice: _getBrailleRegionsForScrollPane", obj)

        scrollRegions = braillegenerator.BrailleGenerator.\
                               _getBrailleRegionsForScrollPane(self, obj)

        # If we are in the slide presentation scroll pane, also announce
        # the current page tab. See bug #538056 for more details.
        #
        rolesList = [pyatspi.ROLE_SCROLL_PANE, \
                     pyatspi.ROLE_PANEL, \
                     pyatspi.ROLE_PANEL, \
                     pyatspi.ROLE_ROOT_PANE, \
                     pyatspi.ROLE_FRAME, \
                     pyatspi.ROLE_APPLICATION]
        if self._script.isDesiredFocusedItem(obj, rolesList):
            for child in obj.parent:
                if child.getRole() == pyatspi.ROLE_PAGE_TAB_LIST:
                    for tab in child:
                        eventState = tab.getState()
                        if eventState.contains(pyatspi.STATE_SELECTED):
                            tabRegions = self.getBrailleRegions(tab)
                            tabRegions[0].append(braille.Region(" ")) 
                            tabRegions[0].extend(scrollRegions[0])
                            return tabRegions

        return scrollRegions
