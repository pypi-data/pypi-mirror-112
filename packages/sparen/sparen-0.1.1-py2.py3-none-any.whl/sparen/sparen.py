#!/usr/bin/env python3

from __future__ import print_function
from inspect import stack, getframeinfo
import os
import sys
import time
import datetime
import inspect
import functools
import traceback

class Logging:

    def __init__(self, dblspace=False):
        self.console_colors = {
            'BLACK'     : '\033[90m',
            'RED'       : '\033[91m',
            'GREEN'     : '\033[92m',
            'YELLOW'    : '\033[93m',
            'BLUE'      : '\033[94m',
            'MAGENTA'   : '\033[95m',
            'CYAN'      : '\033[96m',
            'WHITE'     : '\033[97m',
            'BOLD'      : '\033[1m',
            'FAINT'     : '\033[2m',
            'ITALIC'    : '\033[3m',
            'UNDERLINE' : '\033[4m',
            'BLINK'     : '\033[5m',
            'NEGATIVE'  : '\033[7m',
            'STRIKEOUT' : '\033[9m',
            'DEFAULT'   : '\033[0m'
        }
        self.console_color_filters = {}
        self.endl = os.linesep
        self.logfile = ''
        self.dblspace = False

    def addLogFilter(self, f):
        p = f.split(':')
        if 1 < len(p):
            self.console_color_filters[p[0]] = p[1:]

    def addLogFilters(self, f):
        p = f.split(',')
        if p:
            for v in p:
                self.addLogFilter(v)

    def getLogFilters(self):
        return self.console_color_filters

    def setLogFile(self, fname):
        self.logfile = fname

    def setDoubleSpace(self, enable):
        self.dblspace = enable

    def _Log(self, st, *args):

        def formatStr(s):

            if isinstance(s, Exception):
                try:
                    tb = traceback.TracebackException.from_exception(s)
                    st = str(tb._str)
                    if not st:
                        st = str(tb.exe_type)
                    st += self.endl
                    for d in range(len(tb.stack)-1, -1, -1):
                        filename = os.path.basename(str(tb.stack[d][0]))
                        lineno = str(tb.stack[d][1])
                        fname = str(tb.stack[d][2])
                        line = str(tb.stack[d][3])
                        st += " > %s(%s)::%s() %s%s" % (filename, lineno, fname, line, self.endl)

                    return "[EXCEPTION] " + st
                except Exception as e:
                    return str("[EXCEPTION]" + traceback.format_exc())

            return str(s)

        # Concat args
        if 1 >= len(args):
            s = formatStr(*args)
        else:
            s = ''
            for a in args:
                if 0 < len(s):
                    if ' ' < s[len(s)-1]:
                        s += ' '
                s += formatStr(a)

        # Show file/function/line
        fi = inspect.getframeinfo(inspect.stack()[st][0])
        ls = os.path.basename(fi.filename) + ":" + fi.function + "(" + str(fi.lineno) + "): "
        s = str(s)

        # Apply color filters
        beg = ''
        end = ''
        if sys.stdout.isatty():
            try:
                for k,v in self.console_color_filters.items():
                    if 0 <= s.lower().find(k.lower()):
                        end = self.console_colors['DEFAULT']
                        for c in v:
                            c = c.upper()
                            if 'BLOCK' == c:
                                return
                            elif c in self.console_colors:
                                beg += self.console_colors[c]
            except Exception as e:
                print(e)
                beg = ''
                end = ''

        # Timestamp
        ts = datetime.datetime.now().strftime("[%H:%M:%S] ")

        # Context color
        sctx = ''
        ectx = ''
        if sys.stdout.isatty():
            sctx = self.console_colors['BLUE'] + self.console_colors['FAINT']
            ectx = self.console_colors['DEFAULT']

        # End of line
        endl = self.endl if self.dblspace else ''

        # Print the string
        print(sctx + ts + ls + ectx + beg + s + end + endl)
        sys.stdout.flush()

        # Write to log file if needed
        if self.logfile:
            with open(self.logfile, "a") as f:
                f.write(ts + ls + s + self.endl + endl)
                f.close()

    def __call__(self, *args):
        self._Log(2, *args)

    def showStatus(s, max=70):
        print("\r" + s.ljust(max, ' '), end='')
        sys.stdout.flush()


Log = Logging()


def plotArray(a, fn = None, scalex = True, scaley = True, height = 12, width = 70,
              plot='.', miny = 0, maxy = 100, marginy = 1):

    w = width
    h = height
    m = [[" " for x in range(0, w)] for y in range(0, h)]

    # Get values
    l = len(a)
    v = a if not fn else [fn(x) for x in a]

    # Are we scaling the y axis?
    if scaley:
        miny = min(v) - marginy
        maxy = max(v) + marginy
    rg = maxy - miny
    if 0 == rg:
        rg = 1

    x = 0
    xa = 0
    i = 0
    for i in range(0, l):

        # New y value
        y = (v[i]-miny) * h / rg
        y = int(y)

        # Update x pos
        while xa >= l:
            xa -= l
            x += 1

        if x >= w:
            break

        # Incremental division
        xa += w if scalex else l

        # Limit and choose char to plot
        pt = plot
        if y < 0:
            y = 0
            pt = '_'
        if y >= h:
            y = h - 1
            pt = '^'

        # Plot character
        m[h - y - 1][x] = pt


    # How wide is the y gutter
    j = max([len(str(int(miny))), len(str(int(maxy)))])

    y = h - 1
    pl = None
    ret = ''
    for r in m:
        py = miny+((y+1) * rg / h)
        py = int(py - (1 if 0 > py else 0))
        py = str(py).rjust(j, ' ')
        sy = '  ' if pl == py else py
        pl = py
        ret += "%s : %s" % (sy, ''.join(r)) + "\n"
        y -= 1

    ret += ' ' + (' '*j) + ('-' * (w + 2)) + "\n"
    ret += (' '*j) + '   ' + ''.join([(str((x+1)*10).rjust(9, ' ')+'^') for x in range(0, int(w/10))]) + "\n"

    return ret
