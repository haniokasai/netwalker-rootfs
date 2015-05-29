import gtkhtml2
import gtk
import urllib
import urlparse

opener = urllib.FancyURLopener()
currentUrl = None

def is_relative_to_server(url):
    parts = urlparse.urlparse(url)
    if parts[0] or parts[1]:
        return 0
    return 1

def open_url(url):
    uri = resolve_uri(url)
    return opener.open(uri)

def resolve_uri(uri):
    if is_relative_to_server(uri):
        return urlparse.urljoin(currentUrl, uri)
    return uri

def request_url(document, url, stream):
    f = open_url(url)
    stream.write(f.read())

def link_clicked(document, link):
    print 'link_clicked:', link
    global currentUrl
    try:
        f = open_url(link)
    except OSError:
        print "failed to open", link
        return
    currentUrl = resolve_uri(link)
    document.clear()
    headers = f.info()
    mime = headers.getheader('Content-type').split(';')[0]
    if mime:
        document.open_stream(mime)
    else:
        document.open_stream('text/plain')
    document.write_stream(f.read())
    document.close_stream()

document = gtkhtml2.Document()
document.connect('request_url', request_url)
document.connect('link_clicked', link_clicked)

document.clear()
document.open_stream('text/html')
document.write_stream('<html><head></head><body>Hello, World!<br><a href="http://www.gnome.org/">click me</a></body></html>')
document.close_stream()

def request_object(*args):
    print 'request object', args

view = gtkhtml2.View()
view.set_document(document)
view.connect('request_object', request_object)

sw = gtk.ScrolledWindow()
sw.add(view)

window = gtk.Window()
window.add(sw)
window.set_default_size(400, 400)

window.show_all()

gtk.main()
