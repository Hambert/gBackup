#!/usr/bin/python
#########################################################
# split a file into a set of portions; join.py puts them
# back together; this is a customizable version of the 
# standard unix split command-line utility; because it
# is written in Python, it also works on Windows and can
# be easily tweaked; because it exports a function, it 
# can also be imported and reused in other applications;
#########################################################

import sys, os
kilobytes = 1024
megabytes = kilobytes * 1000
#gigabytes = megabytes * 1000
chunksize = int(1000 * megabytes)                   # default: roughly a 1 GB Filezize

def split(path, fromfile, chunksize=chunksize): 

    partnum = 0
    input = open(path + fromfile, 'rb')                   # use binary mode on Windows
    while 1:                                       # eof=empty string from read
        chunk = input.read(chunksize)              # get next part <= chunksize
        if not chunk: break
        partnum  = partnum+1
        filename = os.path.join(path, ( fromfile + '.part%04d' % partnum))
        fileobj  = open(filename, 'wb')
        fileobj.write(chunk)
        fileobj.close()                            # or simply open(  ).write(  )
    input.close(  )
    assert partnum <= 9999                         # join sort fails if 5 digits
    return partnum

def join(fromdir, parts ):
    output = open(parts[0][:-4], 'wb')
    #parts  = os.listdir(fromdir)
    parts.sort(  )
    for filename in parts:
        filepath = os.path.join(fromdir, filename)
        fileobj  = open(filepath, 'rb')
        while 1:
            filebytes = fileobj.read()
            if not filebytes: break
            output.write(filebytes)
        fileobj.close(  )
    output.close(  )

if __name__ == '__main__':

    split("/Users/schohaus/Desktop/testfiles/","2019-02-07_Nextcloud.zip Kopie.gpg", chunksize)
    