#By: Steven Richards <sbrichards@mit.edu>
#Simple script to check a turntable room for current song and query for DL link

import pycurl 
import StringIO
ttroom = str(raw_input("\n\nEnter a turntable room URL: "))
c = pycurl.Curl()
c.setopt(pycurl.URL, ttroom)
c.setopt(pycurl.HTTPHEADER, ["Accept:"])
roomcurld = StringIO.StringIO()
c.setopt(pycurl.WRITEFUNCTION, roomcurld.write)
c.perform()

roomdata = roomcurld.getvalue()

seekbeatcx = "<input name='cx'"
songtitlekey = '<div id="title">'
songartistkey = '<div id="artist">'
afterartist = '<div id="bottom"></div>'

roomtitle = roomdata[roomdata.find('<title>') + 19:roomdata.find('</title>')]
songstring = roomdata[roomdata.find(songtitlekey) + 16:roomdata.find(songartistkey) - 19]
songartist = roomdata[roomdata.find(songartistkey) + 17:roomdata.find(afterartist) - 59]

print "Room: "+ roomtitle
print "Song: "+ songstring
print "By:   "+ songartist +'\n'

print "Attempting to find a Download Link from seekmybeat.com\n"

seeksite = str('http://www.seekmybeat.com')

c.setopt(pycurl.URL, seeksite)
seekraw = StringIO.StringIO()
c.setopt(pycurl.WRITEFUNCTION, seekraw.write)
c.perform()
seekdata = seekraw.getvalue()
cxkey = seekdata[seekdata.find(seekbeatcx) + 38:seekdata.find("<input name='cof'") - 16]
songstring = songstring.replace(' ', '%20')
seeksearchurl = 'http://www.seekmybeat.com/?cx=' + cxkey + '%3Ak0r-dag7ms0&cof=FORID%3A10&ie=UTF-8&q=' + songstring + '&sa=+++Seek+My+Beat+++'

googlesearch = "http://www.google.com/cse?cx="+cxkey+"%3Ak0r-dag7ms0&cof=FORID%3A10&ie=UTF-8&q="+songstring+"&sa=+++Seek+My+Beat+++&ad=n9&num=10"

c.setopt(pycurl.URL, googlesearch)
seekraw = StringIO.StringIO()
c.setopt(pycurl.WRITEFUNCTION, seekraw.write)
c.perform()
seekraw = seekraw.getvalue()
begin = '<a class="l" href="'
end = 'onmousedown="return curwt'
dllink1 = seekraw[seekraw.find(begin) + 19:seekraw.find(end) - 2]
print 'Download Link Found: ' + dllink1 + '\n'
print "Note: this application's author is not liable nor can guarantee accuracy for the above link"
print 'All search results can be found here: \n' + googlesearch
