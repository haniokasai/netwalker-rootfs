#!/usr/bin/env python
import threading, Queue, time, re, os, tempfile
import aptsources
from timeit import Timer
import urllib
import socket
import random

# Python requires to set the time out globally
socket.setdefaulttimeout(2)

class MirrorTest(threading.Thread):
    """Determines the best mirrors by perfoming ping and download test."""
    class PingWorker(threading.Thread):
        """Use the command line command ping to determine the server's
           response time. Using multiple threads allows to run several
           test simultaneously."""
        def __init__(self, jobs, results, id, parent, borders=(0,1), mod=(0,0)):
            self.borders = borders
            self.mod = mod
            self.parent = parent
            self.id = id
            self.jobs = jobs
            self.results = results
            self.match_result = re.compile(r"^rtt .* = [\.\d]+/([\.\d]+)/.*")
            threading.Thread.__init__(self)
        def run(self):
            result = None
            while MirrorTest.completed < MirrorTest.todo and\
                  self.parent.running.isSet():
                try:
                    mirror = self.jobs.get(True, 1)
                    host = mirror.hostname
                except:
                    continue
                self.parent.report_action("Pinging %s..." % host)
                commando = os.popen("ping -q -c 2 -W 1 -i 0.5 %s" % host,
                                    "r")
                while True:
                    line = commando.readline()
                    if not line:
                        break
                    result = re.findall(self.match_result, line)
                MirrorTest.completed_lock.acquire()
                MirrorTest.completed += 1
                self.parent.report_progress(MirrorTest.completed,
                                            MirrorTest.todo,
                                            self.borders,
                                            self.mod)
                if result:
                    self.results.append([float(result[0]), host, mirror])
                MirrorTest.completed_lock.release()

    def __init__(self, mirrors, test_file, running=None):
        threading.Thread.__init__(self)
        self.test_file = test_file
        self.threads = []
        MirrorTest.completed = 0
        MirrorTest.completed_lock = threading.Lock()
        MirrorTest.todo = len(mirrors)
        self.mirrors = mirrors
        if not running:
            self.running = threading.Event()
        else:
            self.running = running

    def run_full_test(self):
        """Run a test of the mirror test."""
        results_ping = self.run_ping_test(max=10)
        results = self.run_download_test(map(lambda r: r[2], results_ping))
        for (t, h) in results:
            print h.hostname,t

    def report_action(self, text):
        """Should be used by all sub test to collect action status messages
           in a central place."""
        print text

    def report_progress(self, current, max, borders=(0,100), mod=(0,0)):
        """Should be used by all sub test to collect progress messages
           in a central place."""
        print "Completed %s of %s" % (current + mod[0], max + mod[1])

    def run_ping_test(self, mirrors=None, max=None, borders=(0,1), mod=(0,0)):
        """Performs ping tests of the given mirrors and returns the
           best results (specified by max).
           Mod and borders could be used to tweak the reported result if
           the download test is only a part of a whole series of tests."""
        if mirrors == None:
            mirrors = self.mirrors
        jobs = Queue.Queue()
        for m in mirrors:
            jobs.put(m)
        results = []
        #FIXME: Optimze the number of ping working threads LP#90379
        for i in range(25):
            t = MirrorTest.PingWorker(jobs, results, i, self, borders, mod)
            self.threads.append(t)
            t.start()

        for t in self.threads:
            t.join()

        results.sort()
        return results[0:max]

    def run_download_test(self, mirrors=None, max=None, borders=(0,1), 
                          mod=(0,0)):
        """Performs download tests of the given mirrors and returns the
           best results (specified by max).
           Mod and borders could be used to tweak the reported result if
           the download test is only a part of a whole series of tests."""
        def test_download_speed(mirror):
            url = "%s/%s" % (mirror.get_repo_urls()[0],
                             self.test_file)
            self.report_action("Downloading %s..." % url)
            start = time.time()
            try:
                data = urllib.urlopen(url).read(102400)
                return time.time() - start
            except:
                return 0
        if mirrors == None:
            mirrors = self.mirrors
        results = []

        for m in mirrors:
            if not self.running.isSet():
                break
            download_time = test_download_speed(m)
            if download_time > 0:
                results.append([download_time, m])
            self.report_progress(mirrors.index(m), len(mirrors), (0.50,1), mod)
        results.sort()
        return results[0:max]

if __name__ == "__main__":
    distro = aptsources.distro.get_distro()
    distro.get_sources(aptsources.SourcesList())
    pipe = os.popen("dpkg --print-architecture")
    arch = pipe.read().strip()
    test_file = "dists/%s/%s/binary-%s/Packages.gz" % \
                (distro.source_template.name,
                 distro.source_template.components[0].name,
                 arch)
    app = MirrorTest(distro.source_template.mirror_set.values(),
                     test_file)
    app.run_full_test()
