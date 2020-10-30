#!/usr/bin/python

import sys
import os
import os.path
import subprocess
import re
import json

inputFolder  = '/tank/nfsshare/Videos/PlayOn'
outputFolder = '/tank/nfsshare/Videos/PlayOn-trimmed'
startSkipSeconds = 5
endSkipSeconds = 6

def single_chapter (full_fn,fn,duration):
    print('Single Chapter extract:',fn,duration)
    process = subprocess.Popen(['ffprobe','-v','0','-show_entries','format=duration','-of','compact=p=0:nk=1',full_fn],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    out.replace('\n','')
    dur = float(out)
    tot_dur = dur - startSkipSeconds - endSkipSeconds
    print('Original Dur',dur,'New Dur',tot_dur)
    dir_fn = outputFolder + full_fn[len(inputFolder):]
    exists = os.path.exists(dir_fn)
    if not exists:
        print('process')
        process = subprocess.Popen(['ffmpeg','-ss',str(startSkipSeconds),'-i',full_fn,'-t',str(tot_dur),'-c','copy',dir_fn],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        print('out',out)
        print('err',err)
    return

def main ( argv = None):
    o_exists = os.path.exists(outputFolder)
    i_exists = os.path.exists(inputFolder)
    print(i_exists,o_exists)
    if not o_exists:
        os.makedirs(outputFolder)

    for root, dirs, files in os.walk(inputFolder):
#        print('root',root,'dirs',dirs,'files',files)
        destdir = outputFolder + root[len(inputFolder):]
        exists = os.path.exists(destdir)
        if not exists:
            os.makedirs(destdir)
        for file in files:
            full_fn = os.path.join(root,file)
            print full_fn
            process = subprocess.Popen(['ffprobe',full_fn,'-show_chapters','-print_format','json'],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = process.communicate()
            myjson = json.loads(out)
            chap = myjson['chapters']
            m = re.search('Duration: (\d{2}:\d{2}\:\d{2}.\d+)',err)
            if len(chap) == 0:
                single_chapter(full_fn,file,m.group(1))
            else:
                print('Chap',chap)
if __name__ == '__main__':
    main()
    exit(0)
