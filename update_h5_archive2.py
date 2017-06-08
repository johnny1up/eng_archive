import time
import tables
import tables3_api
import numpy as np
import Ska.Table
import re
import os
import sys
import glob

def make_h5_col_file(dat, content, colname):
    """Make a new h5 table to hold column from ``dat``."""
    filename = os.path.join('data', content, 'msid', colname + '.h6')
    if os.path.exists(filename):
        os.unlink(filename)
    filedir = os.path.dirname(filename)
    if not os.path.exists(filedir):
        os.makedirs(filedir)
    
    filters = tables.Filters(complevel=5, complib='zlib')
    h5 = tables.open_file(filename, mode='w', filters=filters)
    
    col = dat[colname]
    h5shape = (0,) + col.shape[1:]
    h5type = tables.Atom.from_dtype(col.dtype)
    h5.create_earray(h5.root, 'data', h5type, h5shape, title=colname,
                    expectedrows=86400*365*10)
    h5.create_earray(h5.root, 'quality', tables.BoolAtom(), (0,), title='Quality',
                    expectedrows=86400*365*10)
    print 'Made', colname
    h5.close()

def append_h5_col(dats, content, colname, i_colname):
    filename = os.path.join('data', content, 'msid', colname + '.h6')
    h5 = tables.open_file(filename, mode='a')
    h5.root.data.append(np.hstack([x[colname] for x in dats]))
    h5.root.quality.append(np.hstack([x['QUALITY'][:,i_colname] for x in dats]))
    h5.close()

filetypes = Ska.Table.read_ascii_table('filetypes.dat')
filetypes = filetypes[ filetypes.pipe == 'ENG0' ]

for filetype in filetypes:
    if filetype.content != 'PCAD3ENG':
        continue
    print filetype
    content = filetype.content.lower()
    instrum = filetype.instrum.lower()
    fitsdir = os.path.abspath(os.path.join('data', content, 'fits'))

    fitsfiles = sorted(glob.glob(os.path.join(fitsdir, '*.fits.gz')))
    if not fitsfiles:
        continue

    dat = Ska.Table.read_fits_table(fitsfiles[0])
    for colname in dat.dtype.names:
        make_h5_col_file(dat, content, colname)

    h5dir = os.path.join('data', content, 'msid')
    if not os.path.exists(h5dir):
        os.makedirs(h5dir)

    dats = []
    for i, f in enumerate(fitsfiles):
        print 'Reading', i, len(fitsfiles), f
        dats.append(Ska.Table.read_fits_table(f))

    for i_colname, colname in enumerate(dat.dtype.names):
        if colname != 'QUALITY':
            print '.',
            append_h5_col(dats, content, colname, i_colname)
        print

