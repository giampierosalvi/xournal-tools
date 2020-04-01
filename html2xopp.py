from html.parser import HTMLParser
#import xml.etree.ElementTree as ET
# conda install -c conda-forge svglib 
# from svglib.svglib import svg2rlg
from os import path
import sys
import numpy as np
#import re
import gzip

class MainHTMLParser(HTMLParser):
    def __init__(self, svgParser, pathName):
        HTMLParser.__init__(self)
        self.svgParser = svgParser
        self.pathName = pathName
    def handle_starttag(self, tag, attrs):
        if tag=="object":
            params = dict()
            for attr in attrs:
                params[attr[0]] = attr[1]
            fo.write('<page width="'+params['width']+'" height="'+params['height']+'">\n')
            # this is hardcoded for now, but can be read from "rect"
            fo.write('<background type="solid" color="#ffffffff" style="plain"/>\n')
            fo.write('<layer>\n')
            print('now parse file:', params['data'])
            ff = open(path.join(self.pathName, params['data']), 'r')
            self.svgParser.feed(ff.read())
            ff.close()
            fo.write('</layer>\n')
            fo.write('</page>\n')

class SVGParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag=="path":
            params = dict()
            for attr in attrs:
                params[attr[0]] = attr[1]
            color = params['fill']
            if color == 'none':
                color = params['stroke']
            fo.write('<stroke tool="pen" ts="0ll" fn="" color="'+color+'ff" width="'+params['stroke-width']+'">')
            # here we are assuming that paths are in the form:
            # 'M' absolute coordinates of first point
            # 'l' sereies of relative coordinates of next points
            # 'Z' end of the path
            #matchObj = re.match('MlZ', params['d'])
            items = params['d'][1:].split(' ')
            del items[2]  # 'l'
            if items[-1] == 'Z':
                del items[-1] # 'Z'
            items = [float(item) for item in items]
            coords = np.array(items).reshape((-1,2)).cumsum(axis=0).reshape(-1)
            textcoo = [str(item) for item in list(coords)]
            fo.write(' '.join(textcoo))
            fo.write('</stroke>\n')


if len(sys.argv) != 3:
    print('Usage:')
    print('python html2xopp.py input.html outputDir')


htmlFileName = sys.argv[1] # 'examples/2019-11-21_spr_meeting.html'
pathName = path.dirname(htmlFileName)
xoppDirName = sys.argv[2]
xoppBaseName = path.basename(htmlFileName)[:-5]+'.xopp'
xoppFileName = path.join(xoppDirName, xoppBaseName)

svgParser = SVGParser()
mainParser = MainHTMLParser(svgParser, pathName)

fo = gzip.open(xoppFileName, 'wt') # '2019-11-21_spr_meeting.xopp'

# print hardcoded header
fo.write('<?xml version="1.0" standalone="no"?>\n')
fo.write('<xournal creator="Xournal++ 1.0.13" fileversion="4">\n')
fo.write('<title>Xournal++ document - see https://github.com/xournalpp/xournalpp</title>\n')
fi = open(htmlFileName, "r")
mainParser.feed(fi.read())
fi.close()
fo.write('</xournal>\n')
fo.close()

# TODO:
# Did not work on '~/MEGA/styluslabs/write/2020-01-24 Open AI Lab.html'
