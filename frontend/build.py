#!/bin/env python

from glob import glob
from subprocess import call

uis = glob('ui/*.ui')
for ui in uis:
    print 'building: ' + ui
    fname = ui[3:-3]
    call(['bash','-c','pyuic4 -o ui_' + fname + '.py ' + ui])
