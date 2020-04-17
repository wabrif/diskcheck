#!/usr/bin/python3

#from __future__ import print_function
#from __future__ import division

import os
import time
import sys
import shutil
import argparse
import requests

def disk_free(path):
    """
    path: string
    Gets the disk usage statistics about the given path.
    returns: free space in kbytes.
    """

    st = os.statvfs(path)
    rtob = st.f_frsize // 1024
    free = st.f_bavail * rtob
    total = st.f_blocks * rtob
    used = (st.f_blocks - st.f_bfree) * rtob
    return free

def oldest_directory(path):
    """
    path: string
    Gets the oldest directory in a path
    returns: name of the oldest directory
    """

    oldesttime = time.time()
    oldestdir = None
    for fname in os.walk(path):
        fullpath = os.path.join(path, fname)
        if os.path.isdir(fullpath) and os.path.getmtime(fullpath) <= oldesttime:
            oldesttime = os.path.getmtime(fullpath)
            oldestdir = fullpath
    return oldestdir

def pushover(API_ENDPOINT,USER,API_KEY,priority):
    """
    API_ENDPOINT: string
    USER: string
    API_KEY: string
    priority: string
    Sends a message to Pushover
    returns: text response from Pushover
    """
    API_ENDPOINT = API_ENDPOINT
    USER = USER
    API_KEY = API_KEY
    priority = priority
    data = {'token':API_KEY,
            'user':USER,
            'message':'Disk space low on hpserver',
            'priority':priority}
    r = requests.post(url = API_ENDPOINT, data = data)
    return r.text

def main():
    parser = argparse.ArgumentParser(description="Check the amount of free diskspace for a directory and then send notification to pushover if its too low")
    parser.add_argument("directory", help="Path to the directory to check")
    parser.add_argument("user", help="The user key")
    parser.add_argument("apikey", help="The application key")
    parser.add_argument("-m", "--minimumfreespace", type=int, default=50000000, help="The minimum freespace to allow before starting the clean-up")
    #parser.add_argument("-k", "--apkey", type=str, help="The application key")
    args = parser.parse_args()
    basepath = args.directory
    USER = args.user
    API_KEY = args.apikey
    minimumfreespace = args.minimumfreespace

    API_ENDPOINT = "https://api.pushover.net/1/messages.json"
    priority = '1'
    if not os.path.isdir(basepath):
        print(basepath," isn't a valid directory")
        exit()
    alertfreespace = 5 * minimumfreespace
    if disk_free(basepath) <= minimumfreespace:
        try:
            result = pushover(API_ENDPOINT,USER,API_KEY,priority)
            print(result)
        except:
            print ("Pushover failed")
            raise

if __name__ == '__main__':
    main()
