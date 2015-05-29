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

"""Utilities for obtaining braille strings for objects.  In general,
there probably should be a singleton instance of the BrailleGenerator
class.  For those wishing to override the braille generators, however,
one can create a new instance and replace/extend the braille
generators as they see fit."""

__id__        = "$Id: braillegenerator.py 4446 2009-01-21 19:54:21Z wwalker $"
__version__   = "$Revision: 4446 $"
__date__      = "$Date: 2009-01-21 14:54:21 -0500 (Wed, 21 Jan 2009) $"
__copyright__ = "Copyright (c) 2005-2008 Sun Microsystems Inc."
__license__   = "LGPL"

import pyatspi
import braille
import debug
import orca_state
import rolenames
import settings

from orca_i18n import _                     # for gettext support
from orca_i18n import ngettext              # for ngettext support

class BrailleGenerator:
    """Takes accessible objects and produces a list of braille Regions
    for those objects.  See the getBrailleRegions method, which is the
    primary entry point.  Subclasses can feel free to override/extend
    the brailleGenerators instance field as they see fit."""

    SKIP_CONTEXT_ROLES = (pyatspi.ROLE_MENU,
                          pyatspi.ROLE_MENU_BAR,
                          pyatspi.ROLE_PAGE_TAB_LIST,
                          pyatspi.ROLE_COMBO_BOX)

    def __init__(self, script):

        # The script that created us.  This allows us to ask the
        # script for information if we need it.
        #
        self._script = script

        self.brailleGenerators = {}
        self.brailleGenerators[pyatspi.ROLE_ALERT]               = \
             self._getBrailleRegionsForAlert
        self.brailleGenerators[pyatspi.ROLE_ANIMATION]           = \
             self._getBrailleRegionsForAnimation
        self.brailleGenerators[pyatspi.ROLE_ARROW]               = \
             self._getBrailleRegionsForArrow
        self.brailleGenerators[pyatspi.ROLE_CHECK_BOX]           = \
             self._getBrailleRegionsForCheckBox
        self.brailleGenerators[pyatspi.ROLE_CHECK_MENU_ITEM]     = \
             self._getBrailleRegionsForCheckMenuItem
        self.brailleGenerators[pyatspi.ROLE_COLUMN_HEADER]       = \
             self._getBrailleRegionsForColumnHeader
        self.brailleGenerators[pyatspi.ROLE_COMBO_BOX]           = \
             self._getBrailleRegionsForComboBox
        self.brailleGenerators[pyatspi.ROLE_DESKTOP_ICON]        = \
             self._getBrailleRegionsForDesktopIcon
        self.brailleGenerators[pyatspi.ROLE_DIAL]                = \
             self._getBrailleRegionsForDial
        self.brailleGenerators[pyatspi.ROLE_DIALOG]              = \
             self._getBrailleRegionsForDialog
        self.brailleGenerators[pyatspi.ROLE_DIRECTORY_PANE]      = \
             self._getBrailleRegionsForDirectoryPane
        self.brailleGenerators[pyatspi.ROLE_EMBEDDED]            = \
             self._getBrailleRegionsForEmbedded
        self.brailleGenerators[pyatspi.ROLE_FRAME]               = \
             self._getBrailleRegionsForFrame
        self.brailleGenerators[pyatspi.ROLE_HTML_CONTAINER]      = \
             self._getBrailleRegionsForHtmlContainer
        self.brailleGenerators[pyatspi.ROLE_ICON]                = \
             self._getBrailleRegionsForIcon
        self.brailleGenerators[pyatspi.ROLE_IMAGE]               = \
             self._getBrailleRegionsForImage
        self.brailleGenerators[pyatspi.ROLE_LABEL]               = \
             self._getBrailleRegionsForLabel
        self.brailleGenerators[pyatspi.ROLE_LIST]                = \
             self._getBrailleRegionsForList
        self.brailleGenerators[pyatspi.ROLE_MENU]                = \
             self._getBrailleRegionsForMenu
        self.brailleGenerators[pyatspi.ROLE_MENU_BAR]            = \
             self._getBrailleRegionsForMenuBar
        self.brailleGenerators[pyatspi.ROLE_MENU_ITEM]           = \
             self._getBrailleRegionsForMenuItem
        self.brailleGenerators[pyatspi.ROLE_OPTION_PANE]         = \
             self._getBrailleRegionsForOptionPane
        self.brailleGenerators[pyatspi.ROLE_PAGE_TAB]            = \
             self._getBrailleRegionsForPageTab
        self.brailleGenerators[pyatspi.ROLE_PAGE_TAB_LIST]       = \
             self._getBrailleRegionsForPageTabList
        self.brailleGenerators[pyatspi.ROLE_PANEL]               = \
             self._getBrailleRegionsForPanel
        self.brailleGenerators[pyatspi.ROLE_PARAGRAPH]           = \
             self._getBrailleRegionsForText
        self.brailleGenerators[pyatspi.ROLE_PASSWORD_TEXT]       = \
             self._getBrailleRegionsForText
        self.brailleGenerators[pyatspi.ROLE_PROGRESS_BAR]        = \
             self._getBrailleRegionsForProgressBar
        self.brailleGenerators[pyatspi.ROLE_PUSH_BUTTON]         = \
             self._getBrailleRegionsForPushButton
        self.brailleGenerators[pyatspi.ROLE_RADIO_BUTTON]        = \
             self._getBrailleRegionsForRadioButton
        self.brailleGenerators[pyatspi.ROLE_RADIO_MENU_ITEM]     = \
             self._getBrailleRegionsForRadioMenuItem
        self.brailleGenerators[pyatspi.ROLE_ROW_HEADER]          = \
             self._getBrailleRegionsForRowHeader
        self.brailleGenerators[pyatspi.ROLE_SCROLL_BAR]          = \
             self._getBrailleRegionsForScrollBar
        self.brailleGenerators[pyatspi.ROLE_SCROLL_PANE]         = \
             self._getBrailleRegionsForScrollPane
        self.brailleGenerators[pyatspi.ROLE_SLIDER]              = \
             self._getBrailleRegionsForSlider
        self.brailleGenerators[pyatspi.ROLE_SPIN_BUTTON]         = \
             self._getBrailleRegionsForSpinButton
        self.brailleGenerators[pyatspi.ROLE_SPLIT_PANE]          = \
             self._getBrailleRegionsForSplitPane
        self.brailleGenerators[pyatspi.ROLE_TABLE]               = \
             self._getBrailleRegionsForTable
        self.brailleGenerators[pyatspi.ROLE_TABLE_CELL]          = \
             self._getBrailleRegionsForTableCellRow
        self.brailleGenerators[pyatspi.ROLE_TABLE_COLUMN_HEADER] = \
             self._getBrailleRegionsForTableColumnHeader
        self.brailleGenerators[pyatspi.ROLE_TABLE_ROW_HEADER]    = \
             self._getBrailleRegionsForTableRowHeader
        self.brailleGenerators[pyatspi.ROLE_TEAROFF_MENU_ITEM]  = \
             self._getBrailleRegionsForMenu
        self.brailleGenerators[pyatspi.ROLE_TERMINAL]            = \
             self._getBrailleRegionsForTerminal
        self.brailleGenerators[pyatspi.ROLE_TEXT]                = \
             self._getBrailleRegionsForText
        self.brailleGenerators[pyatspi.ROLE_TOGGLE_BUTTON]       = \
             self._getBrailleRegionsForToggleButton
        self.brailleGenerators[pyatspi.ROLE_TOOL_BAR]            = \
             self._getBrailleRegionsForToolBar
        self.brailleGenerators[pyatspi.ROLE_TREE]                = \
             self._getBrailleRegionsForTable
        self.brailleGenerators[pyatspi.ROLE_TREE_TABLE]          = \
             self._getBrailleRegionsForTable
        self.brailleGenerators[pyatspi.ROLE_WINDOW]              = \
             self._getBrailleRegionsForWindow

    def _getTextForAccelerator(self, obj):
        """Returns a string to be displayed that describes the keyboard
        accelerator (and possibly shortcut) for the given object.

        Arguments:
        - obj: the Accessible object

        Returns a string to be displayed.
        """

        if settings.brailleVerbosityLevel == settings.VERBOSITY_LEVEL_VERBOSE:
            text = ""
            result = self._script.getKeyBinding(obj)
            accelerator = result[2]
            if len(accelerator) > 0:
                text += "(" + accelerator + ")"
            return text
        else:
            return None

    def _getTextForAvailability(self, obj):
        """Returns a string to be displayed that describes the availability
        of the given object.

        Arguments:
        - obj: the Accessible object

        Returns a string to be displayed.
        """

        state = obj.getState()
        if not state.contains(pyatspi.STATE_SENSITIVE):
            # Translators: this represents an item on the screen that has
            # been set insensitive (or grayed out).
            #
            return _("grayed")
        else:
            return None

    def _getTextForRequiredObject(self, obj):
        """Returns a string to be displayed that describes the required
        state of the given object.

        Arguments:
        - obj: the Accessible object

        Returns a string to be displayed.
        """

        if not settings.presentRequiredState:
            return None

        state = obj.getState()
        if state.contains(pyatspi.STATE_REQUIRED):
            return settings.brailleRequiredStateString
        else:
            return None

    def _getTextForRole(self, obj, role=None):
        if (settings.brailleVerbosityLevel \
            == settings.VERBOSITY_LEVEL_VERBOSE)\
           and (obj.getRole() != pyatspi.ROLE_UNKNOWN):
            return rolenames.getBrailleForRoleName(obj, role)
        else:
            return None

    def _debugGenerator(self, generatorName, obj):
        """Prints debug.LEVEL_FINER information regarding the braille
        generator.

        Arguments:
        - generatorName: the name of the generator
        - obj: the object being presented
        """

        debug.println(debug.LEVEL_FINER,
                      "GENERATOR: %s" % generatorName)
        debug.println(debug.LEVEL_FINER,
                      "           obj             = %s" % obj.name)
        debug.println(debug.LEVEL_FINER,
                      "           role            = %s" % obj.getRoleName())

    def _getDefaultBrailleRegions(self, obj, role=None):
        """Gets text to be displayed for the current object's name,
        role, and any accelerators.  This is usually the fallback
        braille generator should no other specialized braille
        generator exist for this object.

        Arguments:
        - obj: an Accessible
        - role: Role to use as an override.

        Returns a list where the first element is a list of Regions to
        display and the second element is the Region which should get
        focus.
        """

        self._debugGenerator("_getDefaultBrailleRegions", obj)

        regions = []

        text = ""
        text = self._script.appendString(
            text, self._script.getDisplayedLabel(obj))
        text = self._script.appendString(
            text, self._script.getDisplayedText(obj))
        text = self._script.appendString(text, 
                                         self._script.getTextForValue(obj))
        text = self._script.appendString(text, self._getTextForRole(obj, role))
        text = self._script.appendString(text,
                                         self._getTextForRequiredObject(obj))

        regions = []
        componentRegion = braille.Component(obj, text)
        regions.append(componentRegion)

        return [regions, componentRegion]

    def _getBrailleRegionsForAlert(self, obj):
        """Gets the title of the dialog and the contents of labels inside the
        dialog that are not associated with any other objects.

        Arguments:
        - obj: the Accessible dialog

        Returns a list where the first element is a list of Regions to display
        and the second element is the Region which should get focus.
        """

        self._debugGenerator("_getBrailleRegionsForAlert", obj)
        return self._getDefaultBrailleRegions(obj)

    def _getBrailleRegionsForAnimation(self, obj):
        """Gets the title of the dialog and the contents of labels inside the
        dialog that are not associated with any other objects.

        Arguments:
        - obj: the Accessible dialog

        Returns a list where the first element is a list of Regions to display
        and the second element is the Region which should get focus.
        """

        self._debugGenerator("_getBrailleRegionsForAnimation", obj)

        text = ""
        text = self._script.appendString(
            text, self._script.getDisplayedLabel(obj))
        text = self._script.appendString(
            text, self._script.getDisplayedText(obj))
        text = self._script.appendString(text, self._getTextForRole(obj))
        text = self._script.appendString(text, obj.description, ": ")

        regions = []
        componentRegion = braille.Component(obj, text)
        regions.append(componentRegion)

        return [regions, componentRegion]

    def _getBrailleRegionsForArrow(self, obj):
        """Gets text to be displayed for an arrow.

        Arguments:
        - obj: the arrow

        Returns a list where the first element is a list of Regions to display
        and the second element is the Region which should get focus.
        """

        self._debugGenerator("_getBrailleRegionsForArrow", obj)

        # [[[TODO: determine orientation of arrow. Logged as bugzilla bug
        # 319744.]]]
        # text = arrow direction (left, right, up, down)
        #
        return self._getDefaultBrailleRegions(obj)

    def _getBrailleRegionsForCheckBox(self, obj):
        """Get the braille for a check box.  If the check box already had
        focus, then only the state is displayed.

        Arguments:
        - obj: the check box

        Returns a list where the first element is a list of Regions to display
        and the second element is the Region which should get focus.
        """

        self._debugGenerator("_getBrailleRegionsForCheckBox", obj)

        state = obj.getState()
        if state.contains(pyatspi.STATE_INDETERMINATE):
            indicatorindex = 2
        elif state.contains(pyatspi.STATE_CHECKED):
            indicatorindex = 1
        else:
            indicatorindex = 0

        text = ""
        state = obj.getState()

        text = self._script.appendString(
            text, self._script.getDisplayedLabel(obj))
        text = self._script.appendString(
            text, self._script.getDisplayedText(obj))

        text = self._script.appendString(
            text, self._getTextForRole(obj, pyatspi.ROLE_CHECK_BOX))
        text = self._script.appendString(text,
                                         self._getTextForRequiredObject(obj))

        regions = []
        componentRegion = braille.Component(
            obj, text,
            indicator=settings.brailleCheckBoxIndicators[indicatorindex])
        regions.append(componentRegion)

        return [regions, componentRegion]

    def _getBrailleRegionsForCheckMenuItem(self, obj):
        """Get the braille for a check menu item.  If the check menu item
        already had focus, then only the state is displayed.

        Arguments:
        - obj: the check menu item

        Returns a list where the first element is a list of Regions to display
        and the second element is the Region which should get focus.
        """

        self._debugGenerator("_getBrailleRegionsForCheckMenuItem", obj)

        state = obj.getState()
        if state.contains(pyatspi.STATE_INDETERMINATE):
            indicatorindex = 2
        elif state.contains(pyatspi.STATE_CHECKED):
            indicatorindex = 1
        else:
            indicatorindex = 0

        text = ""
        state = obj.getState()

        text = self._script.appendString(
            text, self._script.getDisplayedLabel(obj))
        text = self._script.appendString(
            text, self._script.getDisplayedText(obj))

        if obj == orca_state.locusOfFocus:
            text = self._script.appendString(text, self._getTextForRole(obj))
            text = self._script.appendString(
                text, self._getTextForAvailability(obj))
            text = self._script.appendString(text,
                                      self._getTextForAccelerator(obj),
                                      "")

        regions = []
        componentRegion = braille.Component(
            obj, text,
            indicator=settings.brailleCheckBoxIndicators[indicatorindex])
        regions.append(componentRegion)

        return [regions, componentRegion]

    def _getBrailleRegionsForColumnHeader(self, obj):
        """Get the braille for a column header.

        Arguments:
        - obj: the column header

        Returns a list where the first element is a list of Regions to display
        and the second element is the Region which should get focus.
        """

        self._debugGenerator("_getBrailleRegionsForColumnHeader", obj)

        return self._getDefaultBrailleRegions(obj)

    def _getBrailleRegionsForComboBox(self, obj):
        """Get the braille for a combo box.  If the combo box already has
        focus, then only the selection is displayed.

        Arguments:
        - obj: the combo box

        Returns a list where the first element is a list of Regions to display
        and the second element is the Region which should get focus.
        """

        self._debugGenerator("_getBrailleRegionsForComboBox", obj)

        regions = []

        focusedRegionIndex = 0
        label = self._script.getDisplayedLabel(obj)
        if label and (len(label) > 0):
            regions.append(braille.Region(label + " "))
            focusedRegionIndex = 1

        # Check to see if the text is editable. If so, then we want
        # to show the text attributes (such as selection -- see bug
        # 496846 for more details).
        #
        textObj = None
        for child in obj:
            if child and child.getRole() == pyatspi.ROLE_TEXT:
                textObj = child
        if textObj and textObj.getState().contains(pyatspi.STATE_EDITABLE):
            textRegion = braille.Text(textObj)
            regions.append(textRegion)
        else:
            displayedText = self._script.getDisplayedText(obj)
            if displayedText:
                regions.append(braille.Region(displayedText))

        regions.append(braille.Region(
            " " + rolenames.getBrailleForRoleName(obj)))

        # Things may not have gone as expected above, so we'll do some
        # defensive programming to make sure we don't get an index out
        # of bounds.
        #
        if focusedRegionIndex >= len(regions):
            focusedRegionIndex = 0
        if len(regions) == 0:
            focusedRegion = None
        else:
            focusedRegion = regions[focusedRegionIndex]

        # [[[TODO: WDW - perhaps if a text area was created, we should
        # give focus to it.]]]
        #
        return [regions, focusedRegion]

    def _getBrailleRegionsForDesktopIcon(self, obj):
        """Get the braille for a desktop icon.

        Arguments:
        - obj: the desktop icon

        Returns a list where the first element is a list of Regions to display
        and the second element is the Region which should get focus.
        """

        self._debugGenerator("_getBrailleRegionsForDesktopIcon", obj)

        return self._getDefaultBrailleRegions(obj)

    def _getBrailleRegionsForDial(self, obj):
        """Get the braille for a dial.

        Arguments:
        - obj: the dial

        Returns a list where the first element is a list of Regions to display
        and the second element is the Region which should get focus.
        """

        # [[[TODO: WDW - might need to include the value here?  Logged as
        # bugzilla bug 319746.]]]
        #
        self._debugGenerator("_getBrailleRegionsForDial", obj)

        return self._getDefaultBrailleRegions(obj)

    def _getBrailleRegionsForDialog(self, obj):
        """Get the braille for a dialog box.

        Arguments:
        - obj: the dialog box

        Returns a list where the first element is a list of Regions to display
        and the second element is the Region which should get focus.
        """

        self._debugGenerator("_getBrailleRegionsForDialog", obj)

        return self._getBrailleRegionsForAlert(obj)

    def _getBrailleRegionsForDirectoryPane(self, obj):
        """Get the braille for a directory pane.

        Arguments:
        - obj: the dial

        Returns a list where the first element is a list of Regions to display
        and the second element is the Region which should get focus.
        """

        self._debugGenerator("_getBrailleRegionsForDirectoryPane", obj)

        return self._getDefaultBrailleRegions(obj)

    def _getBrailleRegionsForEmbedded(self, obj, role=None):
        """Gets text to be displayed for the current embedded object.

        Arguments:
        - obj: an Accessible
        - role: Role to use as an override.

        Returns a list where the first element is a list of Regions to
        display and the second element is the Region which should get
        focus.
        """

        self._debugGenerator("_getBrailleRegionsForEmbedded", obj)

        regions = []

        text = ""
        text = self._script.appendString(
            text, self._script.getDisplayedLabel(obj))
        text = self._script.appendString(
            text, self._script.getDisplayedText(obj))
        if not text:
            try:
                text = obj.getApplication().name
            except:
                pass

        regions = []
        componentRegion = braille.Component(obj, text)
        regions.append(componentRegion)

        return [regions, componentRegion]

    def _getBrailleRegionsForFrame(self, obj):
        """Get the braille for a frame.

        Arguments:
        - obj: the frame

        Returns a list where the first element is a list of Regions to display
        and the second element is the Region which should get focus.
        """

        self._debugGenerator("_getBrailleRegionsForFrame", obj)

        regions = []

        text = ""
        text = self._script.appendString(
            text, self._script.getDisplayedLabel(obj))
        text = self._script.appendString(
            text, self._script.getDisplayedText(obj))
        text = self._script.appendString(text,
                                         self._script.getTextForValue(obj))
        text = self._script.appendString(text, self._getTextForRole(obj))

        # If this application has more than one unfocused alert or
        # dialog window, then add '(<m> dialogs)' to the braille context,
        # to let the user know.
        #
        alertAndDialogCount = \
                    self._script.getUnfocusedAlertAndDialogCount(obj)
        if alertAndDialogCount > 0:
            # Translators: this tells the user how many unfocused
            # alert and dialog windows plus the total number of
            # windows that this application has.
            #
            line = ngettext("(%d dialog)",
                            "(%d dialogs)",
                            alertAndDialogCount) % alertAndDialogCount
            text = self._script.appendString(text, line)

        regions = []
        componentRegion = braille.Component(obj, text)
        regions.append(componentRegion)

        return [regions, componentRegion]

    def _getBrailleRegionsForHtmlContainer(self, obj):
        """Get the braille for an HTML container.

        Arguments:
        - obj: the dial

        Returns a list where the first element is a list of Regions to display
        and the second element is the Region which should get focus.
        """

        self._debugGenerator("_getBrailleRegionsForHtmlContainer", obj)

        return self._getDefaultBrailleRegions(obj)

    def _getBrailleRegionsForIcon(self, obj):
        """Get the braille for an icon.

        Arguments:
        - obj: the icon

        Returns a list where the first element is a list of Regions to display
        and the second element is the Region which should get focus.
        """

        self._debugGenerator("_getBrailleRegionsForIcon", obj)

        text = ""
        text = self._script.appendString(
            text, self._script.getDisplayedLabel(obj))
        text = self._script.appendString(
            text, self._script.getDisplayedText(obj))
        try:
            image = obj.queryImage()
        except NotImplementedError:
            pass
        else:
            description = image.imageDescription
            if len(description):
                text = self._script.appendString(text, description)

        text = self._script.appendString(text, self._getTextForRole(obj))

        regions = []
        componentRegion = braille.Component(obj, text)
        regions.append(componentRegion)

        return [regions, componentRegion]

    def _getBrailleRegionsForImage(self, obj):
        """Get the braille for an image.

        Arguments:
        - obj: the image

        Returns a list where the first element is a list of Regions to display
        and the second element is the Region which should get focus.
        """

        self._debugGenerator("_getBrailleRegionsForImage", obj)

        return self._getDefaultBrailleRegions(obj, pyatspi.ROLE_IMAGE)

    def _getBrailleRegionsForLabel(self, obj):
        """Get the braille for a label.

        Arguments:
        - obj: the label

        Returns a list where the first element is a list of Regions to display
        and the second element is the Region which should get focus.
        """

        self._debugGenerator("_getBrailleRegionsForLabel", obj)

        regions = []

        textRegion = braille.Text(obj,
                                  self._script.getDisplayedLabel(obj),
                                  settings.brailleEOLIndicator)
        regions.append(textRegion)

        # We do not want the role at the end of text areas.

        return [regions, textRegion]

    def _getBrailleRegionsForList(self, obj):
        """Get the braille for a list.

        Arguments:
        - obj: the list

        Returns a list where the first element is a list of Regions to display
        and the second element is the Region which should get focus.
        """

        # [[[TODO: WDW - include how many items in the list?
        # Perhaps should also include current list item in here?
        # Logged as bugzilla bug 319749.]]]
        #
        self._debugGenerator("_getBrailleRegionsForList", obj)

        return self._getDefaultBrailleRegions(obj)

    def _getBrailleRegionsForListItem(self, obj):
        """Get the braille for a listitem.

        Arguments:
        - obj: the listitem

        """

        self._debugGenerator("_getBrailleRegionsForListItem", obj)

        text = ""
        text = self._script.appendString(
            text, self._script.getDisplayedLabel(obj))
        text = self._script.appendString(
            text, self._script.getDisplayedText(obj))

        state = obj.getState()
        if state.contains(pyatspi.STATE_EXPANDABLE):
            if state.contains(pyatspi.STATE_EXPANDED):
                # Translators: this represents the state of a node in a tree.
                # 'expanded' means the children are showing.
                # 'collapsed' means the children are not showing.
                #
                text = self._script.appendString(text, _('expanded'))
            else:
                # Translators: this represents the state of a node in a tree.
                # 'expanded' means the children are showing.
                # 'collapsed' means the children are not showing.
                #
                text = self._script.appendString(text, _('collapsed'))

        if obj == orca_state.locusOfFocus:
            text = self._script.appendString(
                text, self._getTextForRole(obj))
            text = self._script.appendString(
                text, self._getTextForAvailability(obj))
            text = self._script.appendString(
                text, self._getTextForAccelerator(obj), "")

        level = self._script.getNodeLevel(obj)
        if level >= 0:
            # Translators: this represents the depth of a node in a tree
            # view (i.e., how many ancestors a node has).
            #
            text = self._script.appendString(text, _("LEVEL %d") \
                                             % (level + 1))

        regions = []
        componentRegion = braille.Component(obj, text)
        regions.append(componentRegion)

        return [regions, componentRegion]

    def _getBrailleRegionsForMenu(self, obj):
        """Get the braille for a menu.

        Arguments:
        - obj: the menu

        Returns a list where the first element is a list of Regions to display
        and the second element is the Region which should get focus.
        """

        self._debugGenerator("_getBrailleRegionsForMenu", obj)

        text = ""
        text = self._script.appendString(
            text, self._script.getDisplayedLabel(obj))
        text = self._script.appendString(
            text, self._script.getDisplayedText(obj))
        text = self._script.appendString(
            text, rolenames.getBrailleForRoleName(obj))

        if obj == orca_state.locusOfFocus:
            text = self._script.appendString(
                text, self._getTextForAvailability(obj))
            text = self._script.appendString(text,
                                      self._getTextForAccelerator(obj),
                                      "")

        regions = []
        componentRegion = braille.Component(obj, text)
        regions.append(componentRegion)

        return [regions, componentRegion]

    def _getBrailleRegionsForMenuBar(self, obj):
        """Get the braille for a menu bar.

        Arguments:
        - obj: the menu bar

        Returns a list where the first element is a list of Regions to display
        and the second element is the Region which should get focus.
        """

        self._debugGenerator("_getBrailleRegionsForMenuBar", obj)

        return self._getDefaultBrailleRegions(obj)

    def _getBrailleRegionsForMenuItem(self, obj):
        """Get the braille for a menu item.

        Arguments:
        - obj: the menu item

        Returns a list where the first element is a list of Regions to display
        and the second element is the Region which should get focus.
        """

        self._debugGenerator("_getBrailleRegionsForMenuItem", obj)

        text = ""

        # OpenOffice check menu items currently have a role of "menu item"
        # rather then "check menu item", so we need to test if one of the
        # states is CHECKED. If it is, then add that in to the braille
        # display output. Note that we can't tell if this is a "check
        # menu item" that is currently unchecked and braille that state.
        # See Orca bug #433398 for more details.
        #
        state = obj.getState()
        if state.contains(pyatspi.STATE_CHECKED):
            indicator = settings.brailleCheckBoxIndicators[1]
        else:
            indicator = ''

        text = self._script.appendString(
            text, self._script.getDisplayedLabel(obj))
        text = self._script.appendString(
            text, self._script.getDisplayedText(obj))

        if obj == orca_state.locusOfFocus:
            text = self._script.appendString(
                text, self._getTextForAvailability(obj))
            text = self._script.appendString(text,
                                      self._getTextForAccelerator(obj),
                                      "")

        regions = []
        componentRegion = braille.Component(obj, text, indicator=indicator)
        regions.append(componentRegion)

        return [regions, componentRegion]

    def _getBrailleRegionsForText(self, obj):
        """Get the braille for a text component.

        Arguments:
        - obj: the text component

        Returns a list where the first element is a list of Regions to display
        and the second element is the Region which should get focus.
        """

        self._debugGenerator("_getBrailleRegionsForText", obj)

        regions = []

        textRegion = braille.Text(obj,
                                  self._script.getDisplayedLabel(obj),
                                  settings.brailleEOLIndicator)
        regions.append(textRegion)
        text = self._getTextForRequiredObject(obj)
        if text:
            regions.append(braille.Region(" " + text))

        if settings.presentReadOnlyText \
           and self._script.isReadOnlyTextArea(obj):
            regions.append(braille.Region(" " \
                                          + settings.brailleReadOnlyString))

        # We do not want the role at the end of text areas.

        return [regions, textRegion]

    def _getBrailleRegionsForOptionPane(self, obj):
        """Get the braille for an option pane.

        Arguments:
        - obj: the option pane

        Returns a list where the first element is a list of Regions to display
        and the second element is the Region which should get focus.
        """

        self._debugGenerator("_getBrailleRegionsForOptionPane", obj)

        return self._getDefaultBrailleRegions(obj)

    def _getBrailleRegionsForPageTab(self, obj):
        """Get the braille for a page tab.

        Arguments:
        - obj: the page tab

        Returns a list where the first element is a list of Regions to display
        and the second element is the Region which should get focus.
        """

        self._debugGenerator("_getBrailleRegionsForPageTab", obj)

        text = ""
        text = self._script.appendString(
            text, self._script.getDisplayedLabel(obj))
        text = self._script.appendString(
            text, self._script.getDisplayedText(obj))
        text = self._script.appendString(text, self._getTextForRole(obj))

        if obj == orca_state.locusOfFocus:
            text = self._script.appendString(
                text, self._getTextForAvailability(obj))
            text = self._script.appendString(text,
                                      self._getTextForAccelerator(obj),
                                      "")

        regions = []
        componentRegion = braille.Component(obj, text)
        regions.append(componentRegion)

        return [regions, componentRegion]

    def _getBrailleRegionsForPageTabList(self, obj):
        """Get the braille for a page tab list.

        Arguments:
        - obj: the page tab list

        Returns a list where the first element is a list of Regions to display
        and the second element is the Region which should get focus.
        """

        self._debugGenerator("_getBrailleRegionsForPageTabList", obj)

        return self._getDefaultBrailleRegions(obj)

    def _getBrailleRegionsForPanel(self, obj):
        """Gets text to be displayed for a panel.

        Arguments:
        - obj: an Accessible

        Returns a list where the first element is a list of Regions to
        display and the second element is the Region which should get
        focus.
        """

        self._debugGenerator("_getBrailleRegionsForPanel", obj)

        regions = []

        text = ""
        text = self._script.appendString(
            text, self._script.getDisplayedLabel(obj))

        # If there was no label for the panel, but it has a name, we'll
        # use the name.
        #
        if len(text) == 0:
            text = self._script.appendString(
                text, self._script.getDisplayedText(obj))

        text = self._script.appendString(text, self._getTextForRole(obj))

        regions = []
        componentRegion = braille.Component(obj, text)
        regions.append(componentRegion)

        return [regions, componentRegion]

    def _getBrailleRegionsForProgressBar(self, obj):
        """Get the braille for a progress bar.  If the object already
        had focus, just the new value is displayed.

        Arguments:
        - obj: the progress bar

        Returns a list where the first element is a list of Regions to display
        and the second element is the Region which should get focus.
        """

        self._debugGenerator("_getBrailleRegionsForProgressBar", obj)

        return self._getDefaultBrailleRegions(obj)

    def _getBrailleRegionsForPushButton(self, obj):
        """Get the braille for a push button

        Arguments:
        - obj: the push button

        Returns a list where the first element is a list of Regions to display
        and the second element is the Region which should get focus.
        """

        self._debugGenerator("_getBrailleRegionsForPushButton", obj)

        regions = []

        text = ""
        text = self._script.appendString(
            text, self._script.getDisplayedLabel(obj))
        text = self._script.appendString(
            text, self._script.getDisplayedText(obj))

        # In Java, some push buttons don't have label and text.
        # In this case, we'll add to presentation the object description,
        # if exists.
        #
        if (not text) and (obj.description):
            text = self._script.appendString(text, obj.description)

        text = self._script.appendString(text, self._getTextForRole(obj))

        regions = []
        componentRegion = braille.Component(obj, text)
        regions.append(componentRegion)

        return [regions, componentRegion]

    def _getBrailleRegionsForRadioButton(self, obj):
        """Get the braille for a radio button.  If the button already had
        focus, then only the state is displayed.

        Arguments:
        - obj: the check box

        Returns a list where the first element is a list of Regions to display
        and the second element is the Region which should get focus.
        """

        self._debugGenerator("_getBrailleRegionsForRadioButton", obj)

        text = ""
        state = obj.getState()

        text = self._script.appendString(
            text, self._script.getDisplayedLabel(obj))
        text = self._script.appendString(
            text, self._script.getDisplayedText(obj))

        # In Java, some toggle buttons don't have label and text.
        # In this case, we'll add to presentation the object description,
        # if exists.
        #
        if (not text) and (obj.description):
            text = self._script.appendString(text, obj.description)

        text = self._script.appendString(text, self._getTextForRole(obj))

        regions = []
        componentRegion = braille.Component(
            obj, text,
            indicator=settings.brailleRadioButtonIndicators[ \
            int(state.contains(pyatspi.STATE_CHECKED) \
                or state.contains(pyatspi.STATE_PRESSED))])
        regions.append(componentRegion)

        return [regions, componentRegion]

    def _getBrailleRegionsForRadioMenuItem(self, obj):
        """Get the braille for a radio menu item.  If the menu item
        already had focus, then only the state is displayed.

        Arguments:
        - obj: the check menu item

        Returns a list where the first element is a list of Regions to display
        and the second element is the Region which should get focus.
        """

        self._debugGenerator("_getBrailleRegionsForRadioMenuItem", obj)

        text = ""

        state = obj.getState()

        text = self._script.appendString(
            text, self._script.getDisplayedLabel(obj))
        text = self._script.appendString(
            text, self._script.getDisplayedText(obj))

        if obj == orca_state.locusOfFocus:
            text = self._script.appendString(text, self._getTextForRole(obj))
            text = self._script.appendString(
                text, self._getTextForAvailability(obj))
            text = self._script.appendString(text,
                                      self._getTextForAccelerator(obj),
                                      "")

        regions = []
        componentRegion = braille.Component(
            obj, text,
            indicator=settings.brailleRadioButtonIndicators[ \
            int(state.contains(pyatspi.STATE_CHECKED))])
        regions.append(componentRegion)

        return [regions, componentRegion]

    def _getBrailleRegionsForRowHeader(self, obj):
        """Get the braille for a row header.

        Arguments:
        - obj: the column header

        Returns a list where the first element is a list of Regions to display
        and the second element is the Region which should get focus.
        """

        self._debugGenerator("_getBrailleRegionsForRowHeader", obj)

        return self._getDefaultBrailleRegions(obj)

    def _getBrailleRegionsForScrollBar(self, obj):
        """Get the braille for a scroll bar.

        Arguments:
        - obj: the scroll bar

        Returns a list where the first element is a list of Regions to display
        and the second element is the Region which should get focus.
        """

        # [[[TODO: WDW - want to get orientation.  Logged as bugzilla bug
        # 319744.]]]
        #
        self._debugGenerator("_getBrailleRegionsForScrollBar", obj)

        return self._getDefaultBrailleRegions(obj)

    def _getBrailleRegionsForScrollPane(self, obj):
        """Get the braille for a scroll pane.

        Arguments:
        - obj: the scroll pane

        Returns a list where the first element is a list of Regions to display
        and the second element is the Region which should get focus.
        """

        self._debugGenerator("_getBrailleRegionsForScrollPane", obj)

        # If this scroll pane is labelled by a page tab, then return the
        # page tab information for the braille context instead. Thunderbird
        # folder properties is such a case. See bug #507922 for more details.
        #
        relations = obj.getRelationSet()
        for relation in relations:
            if relation.getRelationType() ==  pyatspi.RELATION_LABELLED_BY:
                labelledBy = relation.getTarget(0)
                return self._getBrailleRegionsForPageTab(labelledBy)

        return self._getDefaultBrailleRegions(obj)

    def _getBrailleRegionsForSlider(self, obj):
        """Get the braille for a slider.  If the object already
        had focus, just the value is displayed.

        Arguments:
        - obj: the slider

        Returns a list where the first element is a list of Regions to display
        and the second element is the Region which should get focus.
        """

        self._debugGenerator("_getBrailleRegionsForSlider", obj)

        regions = []

        text = ""
        text = self._script.appendString(
            text, self._script.getDisplayedLabel(obj))
        # Ignore the text on the slider.
        #text = self._script.appendString(
        #    text, self._script.getDisplayedText(obj))
        text = self._script.appendString(text,
                                         self._script.getTextForValue(obj))
        text = self._script.appendString(text, self._getTextForRole(obj))
        text = self._script.appendString(text,
                                         self._getTextForRequiredObject(obj))

        regions = []
        componentRegion = braille.Component(obj, text)
        regions.append(componentRegion)

        return [regions, componentRegion]

    def _getBrailleRegionsForSpinButton(self, obj):
        """Get the braille for a spin button.  If the object already has
        focus, then only the new value is displayed.

        Arguments:
        - obj: the spin button

        Returns a list where the first element is a list of Regions to display
        and the second element is the Region which should get focus.
        """

        self._debugGenerator("_getBrailleRegionsForSpinButton", obj)

        return self._getBrailleRegionsForText(obj)

    def _getBrailleRegionsForSplitPane(self, obj):
        """Get the braille for a split pane.

        Arguments:
        - obj: the split pane

        Returns a list where the first element is a list of Regions to display
        and the second element is the Region which should get focus.
        """

        self._debugGenerator("_getBrailleRegionsForSplitPane", obj)

        return self._getDefaultBrailleRegions(obj)

    def _getBrailleRegionsForTable(self, obj):
        """Get the braille for a table

        Arguments:
        - obj: the table

        Returns a list where the first element is a list of Regions to display
        and the second element is the Region which should get focus.
        """

        self._debugGenerator("_getBrailleRegionsForTable", obj)

        return self._getDefaultBrailleRegions(obj)

    def _getBrailleRegionsForTableCell(self, obj):
        """Get the braille for a single table cell

        Arguments:
        - obj: the table

        Returns a list where the first element is a list of Regions to display
        and the second element is the Region which should get focus.
        """

        self._debugGenerator("_getBrailleRegionsForTableCell", obj)

        regions = []

        # If this table cell has 2 children and one of them has a
        # 'toggle' action and the other does not, then present this
        # as a checkbox where:
        # 1) we get the checked state from the cell with the 'toggle' action
        # 2) we get the label from the other cell.
        # See Orca bug #376015 for more details.
        #
        if obj.childCount == 2:
            cellOrder = []
            hasToggle = [ False, False ]
            for i, child in enumerate(obj):
                try:
                    action = child.queryAction()
                except:
                    continue
                else:
                    for j in range(0, action.nActions):
                        # Translators: this is the action name for
                        # the 'toggle' action. It must be the same
                        # string used in the *.po file for gail.
                        #
                        if action.getName(j) in ["toggle", _("toggle")]:
                            hasToggle[i] = True
                            break

            if hasToggle[0] and not hasToggle[1]:
                cellOrder = [ 0, 1 ]
            elif not hasToggle[0] and hasToggle[1]:
                cellOrder = [ 1, 0 ]
            if cellOrder:
                for i in cellOrder:
                    [cellRegions, focusRegion] = \
                            self._getBrailleRegionsForTableCell(obj[i])
                    if len(regions):
                        regions.append(braille.Region(" "))
                    else:
                        cellFocusedRegion = focusRegion
                    regions.append(cellRegions[0])
                regions = [regions, cellFocusedRegion]
                return regions

        label = None

        # [[[TODO: WDW - Attempt to infer the cell type.  There's a
        # bunch of stuff we can do here, such as check the EXPANDABLE
        # state, check the NODE_CHILD_OF relation, etc.  Logged as
        # bugzilla bug 319750.]]]
        #
        try:
            action = obj.queryAction()
        except NotImplementedError:
            pass
        else:
            for i in range(0, action.nActions):
                debug.println(debug.LEVEL_FINEST,
                    "braillegenerator._getBrailleRegionsForTableCell " \
                    + "looking at action %d" % i)

                # Translators: this is the action name for
                # the 'toggle' action. It must be the same
                # string used in the *.po file for gail.
                #
                if action.getName(i) in ["toggle", _("toggle")]:
                    regions = self._getBrailleRegionsForCheckBox(obj)

                    # If this table cell doesn't have any label associated
                    # with it then also braille the table column header.
                    # See Orca bug #455230 for more details.
                    #
                    label = self._script.getDisplayedText( \
                        self._script.getRealActiveDescendant(obj))

                    if label == None or len(label) == 0:
                        try:
                            table = obj.parent.queryTable()
                            index = self._script.getCellIndex(obj)
                            n = table.getColumnAtIndex(index)
                            accHeader = table.getColumnHeader(n)
                            regions[0].append(braille.Region(" "))
                            label = accHeader.name
                            regions[0].append(braille.Region(label))
                        except:
                            pass

                    break

        descendant = self._script.getRealActiveDescendant(obj)
        if len(regions) == 0:
            regions = self._getDefaultBrailleRegions(descendant)
        else:
            cellText = self._script.getDisplayedText(descendant)
            if not cellText or (cellText and label != cellText):
                [cellRegions, focusRegion] = \
                    self._getDefaultBrailleRegions(descendant)
                regions[0].extend(cellRegions)

        # Check to see if this table cell contains an icon (image).
        # If yes:
        #   1/ Try to get a description for it and speak that.
        #   2/ Treat the object of role type ROLE_IMAGE and speak
        #      the role name.
        # See bug #465989 for more details.
        #
        displayedText = self._script.getDisplayedText( \
                          self._script.getRealActiveDescendant(obj))
        try:
            image = obj.queryImage()
        except:
            image = None
        if (not displayedText or len(displayedText) == 0) and image:
            if image.imageDescription:
                regions[0].append(braille.Component(obj,
                                  image.imageDescription))
            [cellRegions, focusRegion] = self._getBrailleRegionsForImage(obj)
            regions[0].extend(cellRegions)

        # [[[TODO: WDW - HACK attempt to determine if this is a node;
        # if so, describe its state.]]]
        #
        state = obj.getState()
        if state.contains(pyatspi.STATE_EXPANDABLE):
            if state.contains(pyatspi.STATE_EXPANDED):
                # Translators: this represents the state of a node in a tree.
                # 'expanded' means the children are showing.
                # 'collapsed' means the children are not showing.
                #
                regions[0].append(braille.Region(" " + _("expanded")))
            else:
                # Translators: this represents the state of a node in a tree.
                # 'expanded' means the children are showing.
                # 'collapsed' means the children are not showing.
                #
                regions[0].append(braille.Region(" " + _("collapsed")))

        return regions

    def _getBrailleRegionsForTableCellRow(self, obj):
        """Get the braille for a table cell row or a single table cell
        if settings.readTableCellRow is False.

        Arguments:
        - obj: the table

        Returns a list where the first element is a list of Regions to display
        and the second element is the Region which should get focus.
        """

        self._debugGenerator("_getBrailleRegionsForTableColumnHeader", obj)

        regions = []

        # Adding in a check here to make sure that the parent is a
        # valid table. It's possible that the parent could be a
        # table cell too (see bug #351501).
        #
        try:
            table = obj.parent.queryTable()
        except NotImplementedError:
            table = None
        if settings.readTableCellRow and table \
            and (not self._script.isLayoutOnly(obj.parent)):
            rowRegions = []
            savedBrailleVerbosityLevel = settings.brailleVerbosityLevel
            settings.brailleVerbosityLevel = \
                                         settings.VERBOSITY_LEVEL_BRIEF
            index = self._script.getCellIndex(obj)
            row = table.getRowAtIndex(index)
            column = table.getColumnAtIndex(index)

            # This is an indication of whether we should speak all the
            # table cells (the user has moved focus up or down a row),
            # or just the current one (focus has moved left or right in
            # the same row).
            #
            speakAll = True
            if "lastRow" in self._script.pointOfReference and \
                "lastColumn" in self._script.pointOfReference:
                pointOfReference = self._script.pointOfReference
                speakAll = (pointOfReference["lastRow"] != row) or \
                       ((row == 0 or row == table.nRows-1) and \
                        pointOfReference["lastColumn"] == column)

            if speakAll:
                focusRowRegion = None
                for i in range(0, table.nColumns):
                    cell = table.getAccessibleAt(row, i)
                    if not cell:
                        debug.println(debug.LEVEL_WARNING,
                             "ERROR: braillegenerator." \
                             + "_getBrailleRegionsForTableCellRow" \
                             + " no accessible at (%d, %d)" % (row, i))
                        continue
                    state = cell.getState()
                    showing = state.contains(pyatspi.STATE_SHOWING)
                    if showing:
                        [cellRegions, focusRegion] = \
                            self._getBrailleRegionsForTableCell(cell)
                        if len(rowRegions):
                            rowRegions.append(braille.Region(" "))
                        rowRegions.extend(cellRegions)
                        if i == column:
                            focusRowRegion = cellRegions[0]
                regions = [rowRegions, focusRowRegion]
            else:
                regions = self._getBrailleRegionsForTableCell(obj)
            settings.brailleVerbosityLevel = savedBrailleVerbosityLevel
        else:
            regions = self._getBrailleRegionsForTableCell(obj)

        level = self._script.getNodeLevel(obj)
        if level >= 0:
            # Translators: this represents the depth of a node in a tree
            # view (i.e., how many ancestors a node has).
            #
            regions[0].append(braille.Region(" " + _("TREE LEVEL %d") \
                                             % (level + 1)))

        return regions

    def _getBrailleRegionsForTableColumnHeader(self, obj):
        """Get the braille for a table column header

        Arguments:
        - obj: the table column header

        Returns a list where the first element is a list of Regions to display
        and the second element is the Region which should get focus.
        """

        self._debugGenerator("_getBrailleRegionsForTableColumnHeader", obj)

        return self._getBrailleRegionsForColumnHeader(obj)

    def _getBrailleRegionsForTableRowHeader(self, obj):
        """Get the braille for a table row header

        Arguments:
        - obj: the table row header

        Returns a list where the first element is a list of Regions to display
        and the second element is the Region which should get focus.
        """

        self._debugGenerator("_getBrailleRegionsForTableRowHeader", obj)

        return self._getBrailleRegionsForRowHeader(obj)

    def _getBrailleRegionsForTearOffMenuItem(self, obj):
        """Get the braille for a tear off menu item

        Arguments:
        - obj: the tear off menu item

        Returns a list where the first element is a list of Regions to display
        and the second element is the Region which should get focus.
        """

        self._debugGenerator("_getBrailleRegionsForTearOffMenuItem", obj)

        componentRegion = braille.Component(
            obj,
            rolenames.getBrailleForRoleName(obj))
        return [[componentRegion], componentRegion]

    def _getBrailleRegionsForTerminal(self, obj):
        """Get the braille for a terminal

        Arguments:
        - obj: the terminal

        Returns a list where the first element is a list of Regions to display
        and the second element is the Region which should get focus.
        """

        self._debugGenerator("_getBrailleRegionsForTerminal", obj)

        regions = []
        textRegion = braille.Text(obj)
        regions.append(textRegion)
        return [regions, textRegion]

    def _getBrailleRegionsForToggleButton(self, obj):
        """Get the braille for a toggle button.  If the toggle button already
        had focus, then only the state is displayed.

        Arguments:
        - obj: the check box

        Returns a list where the first element is a list of Regions to display
        and the second element is the Region which should get focus.
        """

        self._debugGenerator("_getBrailleRegionsForToggleButton", obj)

        return self._getBrailleRegionsForRadioButton(obj)

    def _getBrailleRegionsForToolBar(self, obj):
        """Get the braille for a tool bar

        Arguments:
        - obj: the tool bar

        Returns a list where the first element is a list of Regions to display
        and the second element is the Region which should get focus.
        """

        self._debugGenerator("_getBrailleRegionsForToolBar", obj)

        return self._getDefaultBrailleRegions(obj)

    def _getBrailleRegionsForTree(self, obj):
        """Get the braille for a tree

        Arguments:
        - obj: the tree

        Returns a list where the first element is a list of Regions to display
        and the second element is the Region which should get focus.
        """

        self._debugGenerator("_getBrailleRegionsForTreeTable", obj)

        return self._getDefaultBrailleRegions(obj)

    def _getBrailleRegionsForTreeTable(self, obj):
        """Get the braille for a tree table

        Arguments:
        - obj: the tree table

        Returns a list where the first element is a list of Regions to display
        and the second element is the Region which should get focus.
        """

        self._debugGenerator("_getBrailleRegionsForTreeTable", obj)

        return self._getDefaultBrailleRegions(obj)

    def _getBrailleRegionsForWindow(self, obj):
        """Get the braille for a window

        Arguments:
        - obj: the window

        Returns a list where the first element is a list of Regions to display
        and the second element is the Region which should get focus.
        """

        self._debugGenerator("_getBrailleRegionsForWindow", obj)

        return self._getDefaultBrailleRegions(obj)

    def getBrailleRegions(self, obj, groupChildren=True):
        """Get the braille regions for an Accessible object.  This
        will look first to the specific braille generators and then to
        the default braille generator.  This method is the primary
        method that external callers of this class should use.

        Arguments:
        - obj: the object
        - groupChildren: if True, children of an object should be displayed
                         together with their parent, where each child is
                         separated by _ and the selected child is the Region
                         that should get focus.  The default here is True,
                         but this also is used in conjunction with
                         settings.enableBrailleGrouping.

        Returns a list where the first element is a list of Regions to
        display and the second element is the Region which should get
        focus.
        """

        # If we want to group the children, first see if obj is a child of
        # something we like to group.  If so, then reset the obj to the obj's
        # parent.  If not, see if the obj is the container of things we like
        # to group.  If all fails, we don't try grouping.
        #
        reallyGroupChildren = False
        if settings.enableBrailleGrouping and groupChildren:
            parent = obj.parent
            isChild = parent \
                      and ((parent.getRole() == pyatspi.ROLE_MENU) \
                           or (parent.getRole() == pyatspi.ROLE_MENU_BAR) \
                           or (parent.getRole() == pyatspi.ROLE_PAGE_TAB_LIST))
            if isChild:
                obj = parent
                reallyGroupChildren = True
            else:
                reallyGroupChildren = \
                    (obj.getRole() == pyatspi.ROLE_MENU) \
                    or (obj.getRole() == pyatspi.ROLE_MENU_BAR) \
                    or (obj.getRole() == pyatspi.ROLE_PAGE_TAB_LIST)

        role = obj.getRole()
        if role in self.brailleGenerators:
            generator = self.brailleGenerators[role]
        else:
            generator = self._getDefaultBrailleRegions

        result = generator(obj)
        regions = result[0]
        selectedRegion = result[1]

        if reallyGroupChildren:
            regions.append(braille.Region(" "))
            try:
                selection = obj.querySelection()
            except NotImplementedError:
                selection = None
            i = 0
            for child in obj:
                debug.println(debug.LEVEL_FINEST,
                    "braillegenerator.getBrailleRegions " \
                    + "looking at child %d" % i)

                # [[[TODO: richb - Need to investigate further.
                # Sometimes, for some unknown reason, the child is None.
                # We now test for this, rather than cause a traceback.
                #
                if child and (child.getRole() != pyatspi.ROLE_SEPARATOR):

                # the following line has been removed because insensitive
                # menu items can get focus in StarOffice.
                #
                # and child.getState().contains(pyatspi.STATE_SENSITIVE):

                    if (i > 0) and (i < (self, obj.childCount - 1)):
                        regions.append(braille.Region(" _ "))

                    result = self.getBrailleRegions(child, False)
                    regions.extend(result[0])

                    # This helps us determine which child is the selected
                    # child.  Tracking the SELECTED state is not always
                    # useful (it seems to be inconsistently handled by
                    # toolkits), so we look at the parent's selection model.
                    # In addition, we add a STATE_ARMED check here as a
                    # workaround to the way OOo handles its menu items.
                    #
                    if (selection and selection.isChildSelected(i)) \
                       or child.getState().contains(pyatspi.STATE_ARMED):
                        selectedRegion = result[1]
                i += 1

        return [regions, selectedRegion]

    def getBrailleContext(self, obj):
        """Get the braille regions that describe the context (i.e.,
        names/roles of the container hierarchy) of the object.

        Arguments:
        - obj: the object

        Returns a list of Regions to display.
        """

        brailleRolenameStyle = settings.brailleRolenameStyle

        regions = []
        if not settings.enableBrailleContext:
            return regions

        parent = obj.parent
        if parent and (parent.getRole() in self.SKIP_CONTEXT_ROLES):
            parent = parent.parent
        while parent and (parent.parent != parent):
            # [[[TODO: WDW - we might want to include more things here
            # besides just those things that have labels.  For example,
            # page tab lists might be a nice thing to include. Logged
            # as bugzilla bug 319751.]]]
            #
            if (parent.getRole() != pyatspi.ROLE_FILLER) \
                and (parent.getRole() != pyatspi.ROLE_SECTION) \
                and (parent.getRole() != pyatspi.ROLE_SPLIT_PANE) \
                and (not self._script.isLayoutOnly(parent)):

                # Announce the label and text of the object in the hierarchy.
                #
                label = self._script.getDisplayedLabel(parent)
                text = self._script.getDisplayedText(parent)
                regions.append(braille.Region(" "))
                result = self.getBrailleRegions(parent, False)
                regions.extend(result[0])

            # [[[TODO: HACK - we've discovered oddness in hierarchies
            # such as the gedit Edit->Preferences dialog.  In this
            # dialog, we have labeled groupings of objects.  The
            # grouping is done via a FILLER with two children - one
            # child is the overall label, and the other is the
            # container for the grouped objects.  When we detect this,
            # we add the label to the overall context.]]]
            #
            if parent.getRole() == pyatspi.ROLE_FILLER:
                label = self._script.getDisplayedLabel(parent)
                if label and len(label) and not label.isspace():
                    regions.append(braille.Region(" "))
                    result = self.getBrailleRegions(parent, False)
                    regions.extend(result[0])

            parent = parent.parent

        regions.reverse()

        # Now, we'll treat table row and column headers as context as
        # well.  This requires special handling because we're making
        # headers seem hierarchical in the context, but they are not
        # hierarchical in the containment hierarchicy.  If both exist,
        # we first show the row header then the column header.
        #
        parent = obj.parent
        try:
            table = parent.queryTable()
        except (NotImplementedError, AttributeError):
            table = None
        if parent and table:
            index = self._script.getCellIndex(obj)
            row = table.getRowAtIndex(index)
            if (row >= 0) \
                and (not obj.getRole() in [pyatspi.ROLE_ROW_HEADER,
                                           pyatspi.ROLE_TABLE_ROW_HEADER]):
                # Get the header information.  In Java Swing, the
                # information is not exposed via the description
                # but is instead a header object, so we fall back
                # to that if it exists.
                #
                # [[[TODO: WDW - the more correct thing to do, I 
                # think, is to look at the row header object.
                # We've been looking at the description for so 
                # long, though, that we'll give the description 
                # preference for now.]]]
                #
                desc = table.getRowDescription(row)
                if not desc:
                    header = table.getRowHeader(row)
                    if header:
                        desc = self._script.getDisplayedText(header)
            else:
                desc = None
            if desc and len(desc):
                if settings.brailleRolenameStyle \
                       == settings.VERBOSITY_LEVEL_VERBOSE:
                    if brailleRolenameStyle \
                           == settings.BRAILLE_ROLENAME_STYLE_LONG:
                        text = desc + " " + rolenames.rolenames[\
                            pyatspi.ROLE_ROW_HEADER].brailleLong + " "
                    else:
                        text = desc + " " + rolenames.rolenames[\
                            pyatspi.ROLE_ROW_HEADER].brailleShort + " "
                else:
                    text = desc
                regions.append(braille.Region(text))

            col = table.getColumnAtIndex(index)
            if (col >= 0) \
                and (not obj.getRole() in [pyatspi.ROLE_COLUMN_HEADER,
                                           pyatspi.ROLE_TABLE_COLUMN_HEADER]):
                # Get the header information.  In Java Swing, the
                # information is not exposed via the description
                # but is instead a header object, so we fall back
                # to that if it exists.
                #
                # [[[TODO: WDW - the more correct thing to do, I 
                # think, is to look at the row header object.
                # We've been looking at the description for so 
                # long, though, that we'll give the description 
                # preference for now.]]]
                #
                desc = table.getColumnDescription(col)
                if not desc:
                    header = table.getColumnHeader(col)
                    if header:
                        desc = self._script.getDisplayedText(header)
            else:
                desc = None
            if desc and len(desc):
                if settings.brailleVerbosityLevel \
                       == settings.VERBOSITY_LEVEL_VERBOSE:
                    if brailleRolenameStyle \
                           == settings.BRAILLE_ROLENAME_STYLE_LONG:
                        text = desc + " " + rolenames.rolenames[\
                            pyatspi.ROLE_COLUMN_HEADER].brailleLong + " "
                    else:
                        text = desc + " " + rolenames.rolenames[\
                            pyatspi.ROLE_COLUMN_HEADER].brailleShort + " "
                else:
                    text = desc
                regions.append(braille.Region(text))

        return regions
