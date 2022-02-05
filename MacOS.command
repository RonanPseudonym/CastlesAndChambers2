#!/usr/bin/env python

import os, platform, webbrowser, os, time
# https://www.python.org/ftp/python/3.9.0/python-3.9.0-macosx10.9.pkg

if int(platform.python_version().replace(".","")) < 340:
    os.system('clear')
    print("Your computer is currently running Python "+platform.python_version()+", instead of the needed 3.4 or greater. Python 3 will download once you press enter.")
    raw_input('')
    webbrowser.open("https://www.python.org/ftp/python/3.9.0/python-3.9.0-macosx10.9.pkg")
else:
    print("Running program...")
    directory = os.path.dirname(os.path.realpath(__file__))
    os.system("python3 "+os.path.join(directory, os.path.join("Assets","main.py")))