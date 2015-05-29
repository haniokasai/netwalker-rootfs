#!/usr/bin/python
# coding=UTF-8
#
# Copyright (C) 2008 Tim-Philipp Müller <tim.muller@collabora.co.uk>
# Copyright (C) 2008 Canonical Ltd.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA.
#
# The Totem project hereby grant permission for non-gpl compatible GStreamer
# plugins to be used and distributed together with GStreamer and Totem. This
# permission are above and beyond the permissions granted by the GPL license
# Totem is covered by.
#
# See license_change file for details.

import gobject
gobject.threads_init()
import pygst
pygst.require ("0.10")
import gst

shortref_to_label_map = {
  "childrens": _("Children's"),
  "childrens/activities": _("Activities"),
  "childrens/drama": _("Drama"),
  "childrens/entertainmentandcomedy": _("Entertainment & Comedy"),
  "childrens/factual": _("Factual"),
  "childrens/music": _("Music"),
  "childrens/news": _("News"),
  "childrens/sport": _("Sport"),
  "drama": _("Drama"),
  "drama/actionandadventure": _("Action & Adventure"),
  "drama/biographical": _("Biographical"),
  "drama/classicandperiod": _("Classic & Period"),
  "drama/crime": _("Crime"),
  "drama/historical": _("Historical"),
  "drama/horrorandsupernatural": _("Horror & Supernatural"),
  "drama/legalandcourtroom": _("Legal & Courtroom"),
  "drama/medical": _("Medical"),
  "drama/musical": _("Musical"),
  "drama/political": _("Political"),
  "drama/psychological": _("Psychological"),
  "drama/relationshipsandromance": _("Relationships & Romance"),
  "drama/scifiandfantasy": _("SciFi & Fantasy"),
  "drama/soaps": _("Soaps"),
  "drama/spiritual": _("Spiritual"),
  "drama/thriller": _("Thriller"),
  "drama/waranddisaster": _("War & Disaster"),
  "drama/western": _("Western"),
  "entertainmentandcomedy": _("Entertainment & Comedy"),
  "entertainmentandcomedy/impressionists": _("Impressionists"),
  "entertainmentandcomedy/satire": _("Satire"),
  "entertainmentandcomedy/sitcoms": _("Sitcoms"),
  "entertainmentandcomedy/sketch": _("Sketch"),
  "entertainmentandcomedy/spoof": _("Spoof"),
  "entertainmentandcomedy/standup": _("Standup"),
  "entertainmentandcomedy/varietyshows": _("Variety Shows"),
  "factual": _("Factual"),
  "factual/antiques": _("Antiques"),
  "factual/artscultureandthemedia": _("Arts, Culture & the Media"),
  "factual/beautyandstyle": _("Beauty & Style"),
  "factual/carsandmotors": _("Cars & Motors"),
  "factual/cinema": _("Cinema"),
  "factual/consumer": _("Consumer"),
  "factual/crimeandjustice": _("Crime & Justice"),
  "factual/disability": _("Disability"),
  "factual/familiesandrelationships": _("Families & Relationships"),
  "factual/foodanddrink": _("Food & Drink"),
  "factual/healthandwellbeing": _("Health & Wellbeing"),
  "factual/history": _("History"),
  "factual/homesandgardens": _("Homes & Gardens"),
  "factual/lifestories": _("Life Stories"),
  "factual/money": _("Money"),
  "factual/petsandanimals": _("Pets & Animals"),
  "factual/politics": _("Politics"),
  "factual/sciencenatureandenvironment": _("Science, Nature & Environment"),
  "factual/travel": _("Travel"),
  "learning": _("Learning"),
  "learning/1119": _("Age 11-19"),
  "learning/511": _("Age 5-11"),
  "learning/adults": _("Adults"),
  "learning/preschool": _("Pre-School"),
  "music": _("Music"),
  "music/classicpopandrock": _("Classic Pop & Rock"),
  "music/classical": _("Classical"),
  "music/country": _("Country"),
  "music/danceandelectronica": _("Dance & Electronica"),
  "music/desi": _("Desi"),
  "music/easylisteningsoundtracksandmusicals": _("Easy Listening, Soundtracks & Musicals"),
  "music/folk": _("Folk"),
  "music/hiphoprnbanddancehall": _("Hip Hop, RnB & Dancehall"),
  "music/jazzandblues": _("Jazz & Blues"),
  "music/popandchart": _("Pop & Chart"),
  "music/rockandindie": _("Rock & Indie"),
  "music/soulandreggae": _("Soul & Reggae"),
  "music/world": _("World"),
  "news": _("News"),
  "religionandethics": _("Religion & Ethics"),
  "sport": _("Sport"),
  "sport/archery": _("Archery"),
  "sport/athletics": _("Athletics"),
  "sport/badminton": _("Badminton"),
  "sport/baseball": _("Baseball"),
  "sport/basketball": _("Basketball"),
  "sport/bowls": _("Bowls"),
  "sport/boxing": _("Boxing"),
  "sport/canoeing": _("Canoeing"),
  "sport/cricket": _("Cricket"),
  "sport/cycling": _("Cycling"),
  "sport/darts": _("Darts"),
  "sport/disabilitysport": _("Disability Sport"),
  "sport/diving": _("Diving"),
  "sport/equestrian": _("Equestrian"),
  "sport/fencing": _("Fencing"),
  "sport/football": _("Football"),
  "sport/gaelicgames": _("Gaelic Games"),
  "sport/golf": _("Golf"),
  "sport/gymnastics": _("Gymnastics"),
  "sport/handball": _("Handball"),
  "sport/hockey": _("Hockey"),
  "sport/horseracing": _("Horse Racing"),
  "sport/judo": _("Judo"),
  "sport/modernpentathlon": _("Modern Pentathlon"),
  "sport/motorsport": _("Motorsport"),
  "sport/olympics": _("Olympics"),
  "sport/rowing": _("Rowing"),
  "sport/rugbyleague": _("Rugby League"),
  "sport/rugbyunion": _("Rugby Union"),
  "sport/sailing": _("Sailing"),
  "sport/shinty": _("Shinty"),
  "sport/shooting": _("Shooting"),
  "sport/snooker": _("Snooker"),
  "sport/softball": _("Softball"),
  "sport/swimming": _("Swimming"),
  "sport/tabletennis": _("Table Tennis"),
  "sport/taekwondo": _("Taekwondo"),
  "sport/tennis": _("Tennis"),
  "sport/triathlon": _("Triathlon"),
  "sport/volleyball": _("Volleyball"),
  "sport/waterpolo": _("Water Polo"),
  "sport/weightlifting": _("Weightlifting"),
  "sport/wintersports": _("Winter Sports"),
  "sport/wrestling": _("Wrestling"),
  "weather": _("Weather")
}

# lowest = at the top
shortref_to_sortrank_map = {
  "news": 1,
  "childrens": 2,
  "drama": 3,
  "entertainmentandcomedy": 4,
  "factual": 5,
  "learning": 6,
  "music": 7,
  "religionandethics": 8,
  "sport": 9,
  "weather": 10
}

'''
GenrePool: keeps track of the already-created genres, mainly so we can easily
           find already-existing parents for to-be-created genres
''' 
class GenrePool(object):
    __slots__ = [ 'genres', 'toplevel_genres' ]

    def __init__(self):
        self.clear()

    def clear(self):
        self.genres = { } # maps short_ref => genre object

    def get_genre(self, short_ref):
        # check if genre already exists
        if short_ref in self.genres:
          return self.genres[short_ref]

        # if not, create genre (and any parents which don't exist yet)
        lastslash_pos = short_ref.rfind('/')
        if lastslash_pos > 0:
          parent_ref = short_ref[0:lastslash_pos]
          gst.log('genre: ' + short_ref + ', parent_genre: ' + parent_ref)
          parent = self.get_genre(parent_ref)
        else:
          parent = None

        genre = Genre(short_ref, parent)
        self.genres[short_ref] = genre

        return genre

    def get_toplevel_genres(self):
        toplevel_genres = []
        for genre in self.genres.values():
          if not genre.parent:
            toplevel_genres.append(genre)
        return toplevel_genres

'''
Genre: represents a genre
'''
class Genre(object):
    __slots__ = [ 'short_ref', 'label', 'sort_rank', 'parent',  'children', 'brands' ]

    def __init__(self, short_ref, parent_genre):
        self.short_ref = short_ref

        if short_ref in shortref_to_label_map:
          self.label = shortref_to_label_map[short_ref]
        else:
          self.label = _("Unknown: ") + short_ref

        if short_ref in shortref_to_sortrank_map:
          self.sort_rank = shortref_to_sortrank_map[short_ref]
        else:
          self.sort_rank = 99999

        self.parent = parent_genre
        self.children = []
        self.brands = []

        if parent_genre is not None:
          parent_genre.add_child(self)

        gst.log('created genre ' + short_ref + ' = ' + self.label)

    def add_child(self, child_genre):
        if child_genre not in self.children:
          self.children.append(child_genre)

    def add_brand(self, brand):
        if brand not in self.brands:
            self.brands.append(brand)
            gst.log(self.short_ref + ': adding show ' + brand.title)

if __name__ == "__main__":
  pass

