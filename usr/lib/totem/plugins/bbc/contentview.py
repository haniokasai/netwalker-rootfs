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
#
# TODO:
#  - clean up code: mixed studlyCaps and foo_bar; mixed callbacks and signals

import gobject
gobject.threads_init()
import glib
import gio
import pygst
pygst.require ("0.10")
import gst
import gtk
import pango

import os
import dircache
import errno
import random
import time
import thread

from rdflib.Graph import ConjunctiveGraph
from rdflib import Namespace
from rdflib import RDF

from xdg import BaseDirectory

import installablecodecs
import genres

'''
Define namespaces we will be using globally
'''
DC = Namespace('http://purl.org/dc/elements/1.1/')
PO = Namespace('http://purl.org/ontology/po/')
OWL = Namespace('http://www.w3.org/2002/07/owl#')
FOAF = Namespace('http://xmlns.com/foaf/0.1/')
PLAY = Namespace('http://uriplay.org/elements/')


'''
Global codec cache singleton
'''
codec_cache = None

'''
Container/Audio/Video codec mappings - global for readability
'''

# FIXME: Real Media formats
container_map = { 'application/ogg' : 'application/ogg',
                  'audio/ogg' : 'application/ogg',
                  'video/ogg' : 'application/ogg',
                  'video/x-ms-asf' : 'video/x-ms-asf',
                  'audio/x-ms-asf' : 'video/x-ms-asf',
                  'audio/mp3' : 'audio/mpeg, mpegversion=(int)1, layer=(int)3',
                  'audio/mp4' : 'audio/x-m4a',
                  'audio/mpeg' : 'audio/mpeg, mpegversion=(int)1',
                  'video/x-flv' : 'video/x-flv',
                  'video/3gpp' : 'application/x-3gp',
                  'application/x-3gp' : 'application/x-3gp',
                  'audio/x-matroska' : 'video/x-matroska',
                  'video/x-matroska' : 'video/x-matroska',
                  'video/mp4' : 'video/quicktime',
                  'video/mpeg' : 'video/mpeg, mpegversion=(int)1, ' +
                                 ' systemstream=(boolean)true;   ' + 
                                 'video/mpeg, mpegversion=(int)2, ' +
                                  ' systemstream=(boolean)true',
                  'video/mpeg2' : 'video/mpeg, mpegversion=(int)2,' +
                                  ' systemstream=(boolean)false',
                  'video/mp2t' : 'video/mpegts',
                  'video/mpegts' : 'video/mpegts' }

# FIXME: do we need both parsed=true and parsed=false for mp3?
audio_map = { 'audio/mp1' : 'audio/mpeg, mpegversion=(int)1, layer=(int)1',
              'audio/mp2' : 'audio/mpeg, mpegversion=(int)1, layer=(int)2',
              'audio/mp3' : 'audio/mpeg, mpegversion=(int)1, layer=(int)3',
              'audio/mp4' : 'audio/mpeg, mpegversion=(int)2; ' +
                            'audio/mpeg, mpegversion=(int)4',
              'audio/mpeg' : 'audio/mpeg, mpegversion=(int)1, layer=(int)3',
              'audio/x-wma' : 'audio/x-wma, wmaversion=(int)1; ' +
                              'audio/x-wma, wmaversion=(int)2',
              'audio/x-wmv' : 'audio/x-wma, wmaversion=(int)1; ' +
                              'audio/x-wma, wmaversion=(int)2',
              'audio/x-ms-wma' : 'audio/x-wma, wmaversion=(int)1; ' +
                                 'audio/x-wma, wmaversion=(int)2',
              'audio/x-ms-wmv' : 'audio/x-wma, wmaversion=(int)1; ' +
                                 'audio/x-wma, wmaversion=(int)2',
              'audio/vorbis' : 'audio/x-vorbis' }

# FIXME: video/x-ms-wmv: ask if this refers to a particular wmv version or if it can be any version/profile
# BBC regard video/x-svq as equivalent to video/x-flash-video, so we just
# treat them all the same here and require all of them in this case
video_map = { 'video/x-vp6' : 'video/x-vp6',
              'video/x-flash-video' : 'video/x-svq, svqversion=(int)1; ' +
                                      'video/x-svq, svqversion=(int)3; ' +
                                      'video/x-flash-video, flvversion=(int)1',
              'video/H263-200' : 'video/x-svq, svqversion=(int)1; ' +
                                 'video/x-flash-video, flvversion=(int)1',
              'video/x-svq' : 'video/x-svq, svqversion=(int)1; ' +
                              'video/x-svq, svqversion=(int)3; ' +
                              'video/x-flash-video, flvversion=(int)1',
              'video/H264' : 'video/x-h264',
              'video/mpeg' : 'video/mpeg, mpegversion=(int)1, ' +
                             ' systemstream=(boolean)false;   ' + 
                             'video/mpeg, mpegversion=(int)2, ' +
                              ' systemstream=(boolean)false',
              'video/mpeg1' : 'video/mpeg, mpegversion=(int)1, ' +
                              ' systemstream=(boolean)false',
              'video/mpeg2' : 'video/mpeg, mpegversion=(int)2, ' +
                              ' systemstream=(boolean)false',
              'video/x-dirac' : 'video/x-dirac',
              'video/x-wmv' : 'video/x-wmv, wmvversion=(int)1; ' +
                              'video/x-wmv, wmvversion=(int)2; ' +
                              'video/x-wmv, wmvversion=(int)3',
              'video/x-ms-wmv' : 'video/x-wmv, wmvversion=(int)1; ' +
                                 'video/x-wmv, wmvversion=(int)2; ' +
                                 'video/x-wmv, wmvversion=(int)3' }

###############################################################################

'''
CodecCache: keeps track of what is currently installed and what we might be
            able to install; caches things internally in a dict so we don't
            have to do expensive checks more often than necessary; do not
            cache results elsewhere and make sure to listen to the 'loaded'
            signal and refilter any content once the database of installable
            and installed codecs is loaded (methods may just return False if
            the database hasn't been loaded yet)
'''
class CodecCache(gobject.GObject):
    __slots__ = [ 'codec_cache', 'installable_codecs' ]

    __gsignals__ = dict(loaded=(gobject.SIGNAL_RUN_LAST, None, ()))

    def __init__(self):
        gobject.GObject.__init__ (self)
        self.codec_cache = { }
        self.installable_codecs = None

    def reload_async(self):
        gst.log('starting codec cache loading')
        thread.start_new_thread(self._loading_thread, ())

    def _loading_thread(self):
        ''' idle callback to marshal result back into the main thread '''
        def _loading_done_idle_cb(res):
            gst.log('codec cache loaded (%d elements)' % (len(res)))
            self.installable_codecs = res
            self.emit('loaded')
            return False # don't want to be called again

        gst.log('in codec cache loading thread')
        # the following can take quite a few seconds on machines with very
        # low cpu power (culprit: apt.Cache()), so we do this in a separate
        # thread and then trigger a refiltering of the treeview when done
        res = installablecodecs.getInstallableCodecs()
        gst.log('codec cache loading done, marshalling result into main thread')
        gobject.idle_add(_loading_done_idle_cb, res)
 
    def haveDecoderForCaps(self, decoder_caps):
        caps_string = decoder_caps.to_string()

        if caps_string in self.codec_cache:
          return self.codec_cache[caps_string]

        registry = gst.registry_get_default()
        features = registry.get_feature_list(gst.TYPE_ELEMENT_FACTORY)

        for feature in features:
          # only take into account elements playbin will use
          if feature.get_rank() < gst.RANK_MARGINAL:
            continue
          klass = feature.get_klass()
          # ignore Depayloaders for now
          if klass.find('Demux') >= 0 or \
             klass.find('Decoder') >= 0 or \
             klass.find('Parse') >= 0:
            for pad_template in feature.get_static_pad_templates():
              if pad_template.direction == gst.PAD_SINK:
                if not pad_template.get_caps().intersect(decoder_caps).is_empty():
                  self.codec_cache[caps_string] = True
                  gst.debug('%s can handle %s' % (feature.get_name(), caps_string))
                  return True
        self.codec_cache[caps_string] = False
        gst.debug('no element found that can handle ' + caps_string)
        return False

    ''' do not cache the result of this function '''
    def isInstalledOrInstallable(self, caps_needed):
        if not caps_needed or caps_needed.is_empty() or caps_needed.is_any():
          return False

        if self.installable_codecs is None:
          gst.log('database of installable codecs not loaded yet')
          return False

        for s in caps_needed:
          if not self.haveDecoderForCaps(gst.Caps(s)):
            gst.debug('no decoder for %s installed' % (s.to_string()))
            if not s.get_name() in self.installable_codecs:
              gst.debug('%s not installable either'  % (s.to_string()))
              return False

        return True

###############################################################################

'''
UriPlayObject: base class for Brand, Episode, Encoding, Location etc.
'''
class UriPlayObject(object):
    __slots__ = [ 'rdf_attribute_mapping' ]

    def __init__(self):
        self.rdf_attribute_mapping = []

    def parseProperties(self, conjunctive_graph, graph_obj):
        for rdf_tag, prop_name in self.rdf_attribute_mapping:
          self.__setattr__(prop_name, None)
        for rdf_tag, prop_name in self.rdf_attribute_mapping:
          for match in conjunctive_graph.objects(graph_obj, rdf_tag):
            self.__setattr__(prop_name, match.encode('utf-8'))
            break # we can handle only one value for each property name

###############################################################################

'''
Brand: a show/series/group of episodes
'''
class Brand(UriPlayObject):
    __slots__ = [ 'title', 'description', 'episodes', 'genres' ]

    def __init__(self):
        self.episodes = []
        self.genres = []
        self.rdf_attribute_mapping = [ ( DC['title'], 'title' ),
                                       ( DC['description'], 'description' ) ]

    def parseBrand(self, conjunctive_graph, graph_brand):
        self.parseProperties(conjunctive_graph, graph_brand)

        self.episodes = []
        for e in conjunctive_graph.objects(graph_brand, PO['episode']):
          episode = Episode()
          episode.parseEpisode(conjunctive_graph, e)
          self.episodes.append(episode)

        self.genres = []
        for match in conjunctive_graph.objects(graph_brand, PO['genre']):
          genre_utf8 = match.encode('utf-8')
          pos = genre_utf8.find('/genres/')
          if pos > 0:
            pos += len('/genres/')
            genre = genre_utf8[pos:]
          else:
            gst.warning('Unexpected genre identifier: ' + genre_utf8)
            genre = 'other'
          if genre not in self.genres:
            self.genres.append(genre)

    def hasUsableEpisodes(self):
        for episode in self.episodes:
          if episode.hasUsableEncodings():
            return True
        return False

    def getUsableEpisodes(self):
        usable_episodes = []
        for episode in self.episodes:
          if episode.hasUsableEncodings():
            usable_episodes.append(episode)
        return usable_episodes

###############################################################################

'''
Episode: a single episode of a Brand (even though we parse the different
         versions, for now we'll just pretend there is only one version and
         map the encodings attribute to the encodings of the first version
         we find, to make things easier)
'''
class Episode(UriPlayObject):
    __slots__ = [ 'title', 'description', 'versions', 'encodings' ]

    def __init__(self):
        self.encodings = []
        self.rdf_attribute_mapping = [ ( DC['title'], 'title' ),
                                       ( DC['description'], 'description' ) ]

    def parseEpisode(self, conjunctive_graph, graph_episode):
        self.parseProperties(conjunctive_graph, graph_episode)
        self.versions = []
        for v in conjunctive_graph.objects(graph_episode, PO['version']):
          version = EpisodeVersion()
          version.parseVersion(conjunctive_graph, v)
          self.versions.append(version)
          # encodings of episode = encodings of first version of episode
          if not self.encodings:
            self.encodings = version.encodings

    def hasUsableEncodings(self):
        for encoding in self.encodings:
          if encoding.isUsable():
            return True
        return False

    # TODO: this does not take into account codec quality, highest bitrate wins
    def getBestEncoding(self, connection_speed=0):
        gst.log('connection speed: %d kbit/s' % (connection_speed))
        best_encoding = None
        for encoding in self.encodings:
          if not encoding.isUsable():
            continue
          gst.log('have encoding with bitrate: %d kbit/s' % (encoding.getBitrate()))
          if best_encoding:
            if encoding.getBitrate() > best_encoding.getBitrate():
              if connection_speed <= 0 or encoding.getBitrate() <= connection_speed:
                best_encoding = encoding
          else:
            best_encoding = encoding
        if best_encoding:
          gst.log('best encoding has bitrate of %d kbit/s' % (best_encoding.getBitrate()))  
        return best_encoding

    def getUri(self, connection_speed=0):
        encoding = self.getBestEncoding(connection_speed)
        if encoding:
          location = encoding.getBestLocation()
          if location:
            return location.uri
        return None

###############################################################################

'''
EpisodeVersion: a version of an Episode (e.g. UK vs. US or pg-13 vs. 18)
'''
class EpisodeVersion(UriPlayObject):
    __slots__ = [ 'encodings' ]

    def __init__(self):
        self.encodings = []
        self.rdf_attribute_mapping = []

    def parseVersion(self, conjunctive_graph, graph_version):
        self.parseProperties(conjunctive_graph, graph_version)
        self.encodings = []
        for e in conjunctive_graph.objects(graph_version, PLAY['manifestedAs']):
          encoding = Encoding()
          encoding.parseEncoding(conjunctive_graph, e)
          self.encodings.append(encoding)

###############################################################################

'''
Encoding: a specific encoding of an Episode (format/bitrate/size etc.)
'''
class Encoding(UriPlayObject):
    __slots__ = [ 'container_format', 'bitrate', 'size', 'video_codec',
                  'video_bitrate', 'video_fps', 'video_height', 'video_width',
                  'audio_codec', 'audio_bitrate', 'audio_channels',
                  'locations', 'required_caps' ]

    def __init__(self):
        self.required_caps = None
        self.rdf_attribute_mapping = [
            ( PLAY['dataContainerFormat'], 'container_format' ),
            ( PLAY['bitRate'], 'bitrate' ),
            ( PLAY['dataSize'], 'size' ),
            ( PLAY['videoCoding'], 'video_codec' ),
            ( PLAY['videoBitrate'], 'video_bitrate' ),
            ( PLAY['videoFrameRate'], 'video_fps' ),
            ( PLAY['videoVerticalSize'], 'video_height' ),
            ( PLAY['videoHorizontalSize'], 'video_width' ),
            ( PLAY['audioCoding'], 'audio_codec' ),
            ( PLAY['audioBitrate'], 'audio_bitrate' ),
            ( PLAY['audioChannels'], 'audio_channels' )]

    def parseEncoding(self, conjunctive_graph, graph_encoding):
        self.parseProperties(conjunctive_graph, graph_encoding)
        self.locations = []
        for l in conjunctive_graph.objects(graph_encoding, PLAY['availableAt']):
          location = Location()
          location.parseLocation(conjunctive_graph, l)
          self.locations.append(location)
          self.required_caps = self.postProcessCodecs()

    def postProcessCodecs(self):
        required_caps = gst.Caps()
        if self.video_codec:
          self.video_codec = self.video_codec.lower()
          if self.video_codec in video_map:
            required_caps.append(gst.Caps(video_map[self.video_codec]))
          else:
            gst.warning('unmapped video codec ' + self.video_codec)
            return None
        if self.audio_codec:
          self.audio_codec = self.audio_codec.lower()
          if self.audio_codec in audio_map:
            required_caps.append(gst.Caps(audio_map[self.audio_codec]))
          else:
            gst.warning('unmapped audio codec ' + self.audio_codec)
            return None
        if self.container_format:
          self.container_format = self.container_format.lower()
          if self.container_format in container_map:
            required_caps.append(gst.Caps(container_map[self.container_format]))
          else:
            gst.warning('unmapped container format ' + self.container_format)
            return None

        if not required_caps.is_empty():
          return required_caps
        else:
          return None

    def isUsable(self):
        global codec_cache

        if self.required_caps:
          return codec_cache.isInstalledOrInstallable(self.required_caps)
        else:
          return False

    def getBitrate(self):
      if not self.bitrate:
        return 0
      return eval(self.bitrate)

    def getBestLocation(self):
        locations = self.locations
        random.shuffle(locations)
        for loc in locations:
          if loc.isUsable():
            return loc
        return None

###############################################################################

'''
Location: location (URI) of a specific encoding
'''
class Location(UriPlayObject):
    __slots__ = [ 'uri', 'type', 'sub_type', 'is_live' ]

    # Note: type, subType and isLive are more often not available than available
    def __init__(self):
        self.rdf_attribute_mapping = [
            ( PLAY['uri'], 'uri' ),
            ( PLAY['transportType'], 'type' ),
            ( PLAY['transportSubType'], 'sub_type' ),
            ( PLAY['transportIsLive'], 'is_live' )]

    def parseLocation(self, conjunctive_graph, graph_location):
        self.parseProperties(conjunctive_graph, graph_location)

    def isUsable(self):
        if self.uri and self.uri.startswith('http'):
          return True
        return False

###############################################################################

'''
ContentPool: downloads rdf file with available content and caches it locally,
             then parses the file and announces new brands and brands where
             the episode listing has changed. The cached file is saved with
             the ETag from the server/gio as part of the filename, so we can
             easily compare the tag to the server's later to check if we have
             to update the file or not (not that ETag here means what we get
             from the gio.FileInfo on the remote uri, and never refers to a
             gio-generated ETag for the local cache file, since those two
             are not comparable)
'''
# TODO:
#  - maybe derive from list store or filtermodel directly?
#  - aggregate codec-cache-loaded and loading-done into loading-done internally,
#    so caller doesn't have to worry about that
class ContentPool(gobject.GObject):
    __slots__ = [ 'cache_dir', 'brands' ]

    __gsignals__ = dict(codec_cache_loaded=(gobject.SIGNAL_RUN_LAST, None, ()),
                        progress_message=(gobject.SIGNAL_RUN_LAST, None, (str, )),
                        loading_error=(gobject.SIGNAL_RUN_LAST, None, (str, )),
                        loading_done=(gobject.SIGNAL_RUN_LAST, None, ()))

    CACHE_FILE_PREFIX = 'content-'
    CACHE_FILE_SUFFIX = '.cache'
    AVAILABLE_CONTENT_URI = 'http://open.bbc.co.uk/rad/uriplay/availablecontent'
    MAX_CACHE_FILE_AGE = 2*3600  # 2 hours

    def __init__(self):
        gobject.GObject.__init__ (self)

        self.brands = []
        self.cache_dir = os.path.join(BaseDirectory.xdg_cache_home, 'totem',
                                      'plugins', 'bbc')
        try:
          os.makedirs(self.cache_dir)
          gst.log('created cache directory ' + self.cache_dir)
        except OSError, err:
          if err.errno == errno.EEXIST:
            gst.log('cache directory ' + self.cache_dir + ' already exists')
          else:
            gst.error('failed to create cache directory ' + self.cache_dir +
                      ': ' + err.strerror)
            self.cache_dir = None

    def _on_codec_cache_loaded(self, pool):
        self.emit('codec-cache-loaded')

    ''' returns True if the given filename refers to one of our cache files '''
    def isCacheFileName(self, filename):
      if not filename.startswith(self.CACHE_FILE_PREFIX):
        return False
      if not filename.endswith(self.CACHE_FILE_SUFFIX):
        return False
      return True

    ''' removes all cache files that don't relate to the given etag '''
    def deleteStaleCacheFiles(self, except_etag=None):
        try:
          for fn in dircache.listdir(self.cache_dir):
            if self.isCacheFileName(fn):
              if except_etag == None or fn.find(except_etag) < 0:
                try:
                  gst.log('deleting stale cache file ' + fn)
                  os.remove(os.path.join(self.cache_dir,fn))
                except OSError:
                  pass
        except OSError:
          pass

    ''' finds the most recent cache file and returns its file name or None'''
    def findMostRecentCacheFile(self):
        best_mtime = 0
        best_name = None
        try:
          gst.log('Looking for cache files in ' + self.cache_dir)
          for fn in dircache.listdir(self.cache_dir):
            if self.isCacheFileName(fn):
              mtime = os.stat(os.path.join(self.cache_dir,fn)).st_mtime
              gst.log('Found cache file %s, mtime %ld' % (fn, long(mtime)))
              if mtime > best_mtime:
                best_name = fn
                best_mtime = mtime
        except OSError, err:
          gst.debug("couldn't inspect cache directory %s: %s" % (self.cache_dir, err.strerror))
          return None

        if not best_name:
          gst.log('No cache file found')
          return None

        return best_name

    ''' gets the ETag for the most recent cache file, or None '''
    def getCacheETag(self):
        etag = self.findMostRecentCacheFile()
        if not etag:
          return None
        prefix_len = len(self.CACHE_FILE_PREFIX)
        suffix_len = len(self.CACHE_FILE_SUFFIX)
        etag = etag[prefix_len:-suffix_len]
        gst.log('ETag: ' + etag)
        return etag

    ''' makes a full filename from an ETag '''
    def createCacheFileName(self, etag):
        if not etag:
          gst.debug('No ETag, using dummy ETag as fallback')
          etag = '000000-00000-00000000'
        fn = self.CACHE_FILE_PREFIX + etag +  self.CACHE_FILE_SUFFIX
        return os.path.join(self.cache_dir, fn)

    def parse_async(self, cache_fn):
        self.emit('progress-message', _("Parsing available content list ..."))
        thread.start_new_thread(self._parsing_thread, (cache_fn, ))

    def _parsing_thread(self, cache_fn):
        def _parse_idle_cb(err_msg, brands):
            self.brands = brands
            gst.info('Parsing done: %d brands' % (len(self.brands)))
            if err_msg:
              self.emit('loading-error', err_msg)
            else:
              self.emit('loading-done')
            return False

        err_msg = None
        brands = []
        gst.debug('Loading ' + cache_fn)
        store = ConjunctiveGraph()
        try:
          gst.debug('Reading RDF file ...')
          store.load(cache_fn)
          gst.debug('Parsing ' + cache_fn)
          brands = self.parseBrands(store)
        except:
          gst.warning('Problem parsing RDF')
          err_msg = 'Could not parse available content list'
        finally:
          gst.debug('Parsing done, marshalling result into main thread')
          gobject.idle_add(_parse_idle_cb, err_msg, brands)

    def _format_size_for_display(self, size):
        if size < 1024:
          return '%d bytes' % size
        if size < 1024*1024:
          return '%.1f kB' % (size / 1024.0)
        else:
          return '%.1f MB' % (size / (1024.0*1024.0))

    def load_async(self):
        def _query_done_cb(remote_file, result):
            # mutable container so subfunctions can share access
            # chunks, total_len
            pdata = [ [], 0 ] 

            def _read_async_cb(instream, result):
                try:
                  partial_data = instream.read_finish(result)
                  gst.log('Read partial chunk of %d bytes' % (len(partial_data)))
                  chunks = pdata[0]
                  bytes_read = pdata[1]
                  if len(partial_data) == 0:                  
                    instream.close()
                    outstream = cache_file.create(gio.FILE_CREATE_NONE)
                    for chunk in chunks:
                      outstream.write(chunk)
                    outsize = outstream.query_info('*').get_size()
                    outstream.close()
                    gst.info('Wrote %ld bytes' % (outsize))
                    self.parse_async(cache_fn)
                  else:
                    chunks.append(partial_data)
                    bytes_read += len(partial_data)
                    pdata[0] = chunks
                    pdata[1] = bytes_read
                    instream.read_async(10240, _read_async_cb, io_priority=glib.PRIORITY_LOW-1)
                    self.emit('progress-message',
                              _("Downloading available content list ... ") + '(' +
                              self._format_size_for_display(bytes_read) + ')')
                except IOError, e:
                  gst.warning('Error downloading ' + self.AVAILABLE_CONTENT_URI)
                  instream.close()
                  try:
                    cache_file.delete()
                  finally:
                    self.emit('loading-error', _("Error downloading available content list"))

            # _query_done_cb start:
            gst.log('Query done')
            try:
              remote_info = remote_file.query_info_finish(result)
            except Exception, e:
              # bail out if we can't query, not much point trying to download
              gst.warning('Could not query %s: %s' % (self.AVAILABLE_CONTENT_URI, e.message))
              self.emit('loading-error', _("Could not connect to server"))
              return

            gst.log('Got info, querying etag')
            remote_etag = remote_info.get_etag()
            if remote_etag:
              remote_etag = remote_etag.strip('"')
              gst.log('Remote etag: ' + remote_etag)

            cache_fn = self.createCacheFileName(remote_etag)
            cache_file = gio.File(cache_fn)

            # if file already exists, get size to double-check against server's
            try:
              cache_size = cache_file.query_info('standard::size').get_size()
            except:
              cache_size = 0
            finally:
              if etag and remote_etag and etag == remote_etag:
                remote_size = remote_info.get_size()
                if remote_size <= 0 or cache_size == remote_size:
                  gst.log('Cache file is up-to-date, nothing to do')
                  self.parse_async(cache_fn)
                  return

            # delete old cache file if it exists
            try:
              cache_file.delete()
            except:
              pass

            # FIXME: use gio.File.copy_async() once it's wrapped
            remote_file.read().read_async(10240, _read_async_cb, io_priority=glib.PRIORITY_LOW-1)
            gst.info('copying ' + self.AVAILABLE_CONTENT_URI + ' -> ' + cache_fn)
            self.emit('progress-message', _("Downloading available content list ..."))
            return

        # load_async start:
        gst.log('starting loading')

        # init global singleton variable codec_cache, if needed
        global codec_cache

        if not codec_cache:
          codec_cache = CodecCache()
          codec_cache.connect('loaded', self._on_codec_cache_loaded)
          codec_cache.reload_async()

        etag = self.getCacheETag()
        if etag:
          gst.log('Cached etag: ' + etag)
          self.deleteStaleCacheFiles(etag)
          existing_cache_fn = self.createCacheFileName(etag)
          existing_cache_file = gio.File(existing_cache_fn)
          existing_cache_info = existing_cache_file.query_info('time::modified')
          existing_cache_mtime = existing_cache_info.get_modification_time()
          # if the cache file is not older than N minutes/hours/days, then
          # we'll just go ahead and use it instead of downloading a new one,
          # even if it's not perfectly up-to-date.
          # FIXME: UI should have a way to force an update
          secs_since_update = time.time() - existing_cache_mtime
          if secs_since_update >= 0 and secs_since_update < self.MAX_CACHE_FILE_AGE:
            gst.log('Cache file is fairly recent, last updated %f secs ago' % (secs_since_update))
            self.parse_async(existing_cache_fn)
            return
        else:
          gst.log('Cached etag: None')

        # CHECKME: what happens if http is not available as protocol?
        remote_file = gio.File(self.AVAILABLE_CONTENT_URI)
        gst.log('Contacting server ' + self.AVAILABLE_CONTENT_URI)
        self.emit('progress-message', _("Connecting to server ..."))
        remote_file.query_info_async(_query_done_cb, '*')

    def parseBrands(self, graph):
        brands = []
        for b in graph.subjects(RDF.type, PO['Brand']):
          brand = Brand()
          brand.parseBrand(graph, b)
          brands.append(brand)
          gst.log('[%3d eps] %s %s' % (len(brand.episodes), brand.title, brand.genres))
        return brands

    ''' returns array of brands which can potentially be played '''
    def getUsableBrands(self):
        usable_brands = []
        for brand in self.brands:
          if brand.hasUsableEpisodes():
            usable_brands.append(brand)
        return usable_brands


###############################################################################

class ContentView(gtk.TreeView):
    __slots__ = [ 'pool', 'content_pool_loaded', 'codec_cache_loaded', 'genre_pool' ]
    __gsignals__ = dict(play_episode=
                        (gobject.SIGNAL_RUN_LAST, None,
                         (object,))) # Episode

    SORT_ID_1 = 0

    def __init__(self):
        gtk.TreeView.__init__ (self)
        self.setupModel()

        self.set_headers_visible(False)

        self.connect('row-activated', self.onRowActivated)

	self.set_property('has-tooltip', True)
	self.connect('query-tooltip', self.onQueryTooltip)

        self.set_message(_("Loading ..."))

        self.pool = ContentPool()
        self.pool.connect('codec-cache-loaded', self._on_codec_cache_loaded)
        self.pool.connect('progress-message', self._on_content_pool_message)
        self.pool.connect('loading-error', self._on_content_pool_error)
        self.pool.connect('loading-done', self._on_content_pool_loading_done)
        self.codec_cache_loaded = False
        self.content_pool_loaded = False
        self.genre_pool = genres.GenrePool()

    def load(self):
        self.pool.load_async()
        gst.log('started loading')

    def _on_content_pool_message(self, content_pool, msg):
        self.set_message(msg)

    def _on_content_pool_error(self, content_pool, err_msg):
        gst.warning('Failed to load available content: ' + err_msg)
        self.set_message(err_msg)

    def _on_content_pool_loading_done(self, content_pool):
        gst.log('content pool loaded')
        self.content_pool_loaded = True
        if self.codec_cache_loaded:
          self.populate()

    def _on_codec_cache_loaded(self, content_pool):
        gst.log('codec cache loaded, refilter')
        self.codec_cache_loaded = True
        #self.filter.refilter() FIXME: we don't filter at the moment
        if self.content_pool_loaded:
          self.populate()

    def populate_add_genre(self, genre, parent_iter):
        _iter = self.store.append(parent_iter, [None, None, None, genre])
        for child_genre in genre.children:
          self.populate_add_genre(child_genre, _iter)
        for brand in genre.brands:
          brand_iter = self.store.append(_iter, [brand, None, None, None])
          for ep in brand.episodes:
            self.store.append(brand_iter, [brand, ep, None, None])
        return _iter

    def populate(self):
        gst.log('populating treeview')

        brands = self.pool.getUsableBrands()
        gst.info('%d brands with usable episodes/encodings' % (len(brands)))

        # build genre tree in memory and add brands to genre objects
        self.genre_pool.clear()
        for brand in brands:
          for genre_shortref in brand.genres:
            genre = self.genre_pool.get_genre(genre_shortref)
            genre.add_brand(brand)

        # add everything to the list store
        self.store.clear()
        toplevel_iters = []
        for toplevel_genre in self.genre_pool.get_toplevel_genres():
          _iter = self.populate_add_genre(toplevel_genre, None)          
          toplevel_iters.append(_iter)
          
        # now make all this visible (view might be showing model with message)
        self.set_model(self.filter)

        # expand top-level categories
        for _iter in toplevel_iters:
          path = self.store.get_path(_iter)
          self.expand_row(path, False)

    def get_brand_tooltip(self, brand):
      if not brand or not brand.description:
        return None
      return '<b>%s</b>\n<i>%s</i>' % (gobject.markup_escape_text(brand.title),
                                        gobject.markup_escape_text(brand.description))

    def get_episode_tooltip(self, brand, episode):
      if not episode or not episode.description:
        return None
      return '<b>%s</b>\n<b><small>%s</small></b>\n<i>%s</i>' % (gobject.markup_escape_text(brand.title),
                                                                 gobject.markup_escape_text(episode.title),
                                                                 gobject.markup_escape_text(episode.description))

    def onQueryTooltip(self, view, x, y, keyboard_tip, tip):
      try:
        model, path, _iter = self.get_tooltip_context(x, y, keyboard_tip)
      except:
        return False # probably no content yet

      brand, episode, msg, genre = model.get(_iter, 0, 1, 2, 3)
      if msg or genre:
        return False
      if brand and not episode:
        markup = self.get_brand_tooltip(brand)
      elif brand and episode:
        markup = self.get_episode_tooltip(brand, episode)
      else:
        markup = None
      if markup:
        tip.set_markup(markup)
      else:
        tip.set_text(_("No details available"))
      return True

    def onRowActivated(self, view, path, col):
        model = self.get_model()
        if model:
          _iter = model.get_iter(path)
          brand, episode = self.get_model().get(_iter, 0, 1)
          if episode:
            self.emit('play-episode', episode)

    def renderGenreCell(self, column, renderer, model, _iter, genre):
        markup = '<b>%s</b>' % \
                 (gobject.markup_escape_text(genre.label))
        renderer.set_property('markup', markup)

    def renderBrandCell(self, column, renderer, model, _iter, brand):
        markup = '<b><small>%s <span color="LightGray">(%d)</span></small></b>' % \
                 (gobject.markup_escape_text(brand.title), len(brand.episodes))
        renderer.set_property('markup', markup)

    def renderEpisodeCell(self, column, renderer, model, _iter, brand, episode):
        markup = '<span><small>%s</small></span>' % (gobject.markup_escape_text(episode.title))
        renderer.set_property('markup', markup)

    def renderMessageCell(self, column, renderer, model, _iter, msg):
        markup = '<i>%s</i>' % (gobject.markup_escape_text(msg))
        renderer.set_property('markup', markup)
        
    def renderCell(self, column, renderer, model, _iter):
        brand, episode, msg, genre = model.get(_iter, 0, 1, 2, 3)
        if msg:
          self.renderMessageCell(column, renderer, model, _iter, msg)
        elif genre:
          self.renderGenreCell(column, renderer, model, _iter, genre)
        elif not episode:
          self.renderBrandCell(column, renderer, model, _iter, brand)
        else:
          self.renderEpisodeCell(column, renderer, model, _iter, brand, episode)

    # there must be a more elegant way to do this in python
    def sortFunc(self, model, iter1, iter2):
        brand1, episode1, genre1 = model.get(iter1, 0, 1, 3)
        brand2, episode2, genre2 = model.get(iter2, 0, 1, 3)

        # genres are sorted by genre.sort_rank
        if genre1 and genre2:
          if genre1.sort_rank != genre2.sort_rank:
            return genre1.sort_rank - genre2.sort_rank
          else:
            s1 = genre1.label
            s2 = genre2.label

        # genre always comes before any other siblings (like brands or episodes)
        elif genre1:
          return -1
        elif genre2:
          return 1

        # brands and episodes are sorted alphabetically by title
        elif not episode1 or not episode2:
          s1 = brand1.title
          s2 = brand2.title
        elif episode1 and episode2:
          s1 = episode1.title
          s2 = episode2.title
        else:
          gst.warning('should not be reached (should be genre label comparison)')

        # string comparison
        if s1 == s2:
          return 0
        elif s1 > s2:
          return 1
        else:
          return -1

    def set_message(self, msg):
        self.msg_store.clear()
        self.msg_store.append(None, [None, None, msg, None])
        self.set_model(self.msg_store)
        gst.log('set message "' + msg + '"')

    def setupModel(self):
        # columns: Brand, Episode, message string, Genre
        self.msg_store = gtk.TreeStore(object, object, str, object)
        self.store = gtk.TreeStore(object, object, str, object)
        self.filter = self.store.filter_new()

        column = gtk.TreeViewColumn()
        renderer = gtk.CellRendererText()
        renderer.set_property('ellipsize', pango.ELLIPSIZE_END)
        column.pack_start(renderer, expand=True)
        column.set_cell_data_func(renderer, self.renderCell)
        self.append_column(column)
        self.store.set_sort_func(self.SORT_ID_1, self.sortFunc)
        self.store.set_sort_column_id(self.SORT_ID_1, gtk.SORT_ASCENDING)

if __name__ == "__main__":
    # ensure the caps strings in the container/video/audio map are parsable
    for cs in video_map:
      caps = gst.Caps(video_map[cs])
    for cs in audio_map:
      caps = gst.Caps(audio_map[cs])
    for cs in container_map:
      caps = gst.Caps(container_map[cs])
    # test window
    window = gtk.Window()
    scrollwin = gtk.ScrolledWindow()
    scrollwin.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
    window.add(scrollwin)
    view = ContentView()
    view.load()
    scrollwin.add(view)
    window.show_all()
    gtk.main()

