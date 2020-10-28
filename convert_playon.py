#!/usr/bin/python

import sys
import os
import os.path
import subprocess
import re

inputFolder  = '/tank/nfsshare/Videos/PlayOn'
outputFolder = '/tank/nfsshare/Videos/PlayOn-trimmed'
startSkipSeconds = 5
endSkipSeconds = 6

def main ( argv = None):
    o_exists = os.path.exists(outputFolder)
    i_exists = os.path.exists(inputFolder)
    print(i_exists,o_exists)
    if not o_exists:
        os.makedirs(outputFolder)

    for root, dirs, files in os.walk(inputFolder):
        print('root',root,'dirs',dirs,'files',files)
        destdir = outputFolder + root[len(inputFolder):]
        exists = os.path.exists(destdir)
        if not exists:
            os.makedirs(destdir)
        for file in files:
            full_fn = os.path.join(root,file)
#            full_fn = full_fn.replace(' ','\\ ')
            print full_fn
            import pdb;pdb.set_trace()
            process = subprocess.Popen(['ffprobe',full_fn,'-show_chapters','-print_format','json'],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = process.communicate()
            print('stdout',out)
            print('stderr',err)
if __name__ == '__main__':
    main()
    exit(0)
