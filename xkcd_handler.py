#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
XKCD Url handler for Terminator by Rémi Oudin <oudin@crans.org>
Terminator is a Terminal written by Chris Jones <cmsj@tenshu.net>
GPLv2 only
"""
import re
import terminatorlib.plugin as plugin
from terminatorlib.util import dbg


AVAILABLE = ['XKCDUrlHandler']

class XKCDUrlHandler(plugin.URLHandler):
    """ XKCD Url Handler. If the URL looks like xkcd/<number> or xkcd://<number>
    then it should be transformed into https://xkcd.com/<number>.
    """
    capabilities = ['url_handler']
    handler_name = 'xkcd_url'
    match = '\\bxkcd:?//?[0-9]+\\b'
    nameopen = "Open XKCD Comic"
    namecopy = "Copy XKCD Comic URL"

    def callback(self, url):
        "Look for the given xkcd strip."
        dbg("XKCD handler: %s" % url)
        item = re.findall(r'[0-9]+', url)
        url = 'https://xkcd.com/%s' % item[0]
        return url
