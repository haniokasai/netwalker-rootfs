# Orca
#
# Copyright 2004-2008 Sun Microsystems Inc.
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

__id__        = "$Id: script_settings.py 4221 2008-09-15 08:11:23Z wwalker $"
__version__   = "$Revision: 4221 $"
__date__      = "$Date: 2008-09-15 04:11:23 -0400 (Mon, 15 Sep 2008) $"
__copyright__ = "Copyright (c) 2004-2008 Sun Microsystems Inc."
__license__   = "LGPL"

# Whether we prefix chat room messages with the name of the chat room.
#
prefixChatMessage = False

# Whether we announce when a buddy is typing.
#
announceBuddyTyping = False

# Whether we provide chat room specific message histories.
#
chatRoomHistories = False

# Possible ways of how Orca should speak pidgin chat messages.
#
SPEAK_ALL_MESSAGES              = 0
SPEAK_CHANNEL_WITH_FOCUS        = 1
SPEAK_ALL_CHANNELS_WHEN_FOCUSED = 2

# Indicates how pidgin chat messages should be spoken.
#
speakMessages = SPEAK_ALL_MESSAGES

