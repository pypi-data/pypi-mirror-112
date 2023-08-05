from __future__ import print_function
from IPython.core.magic import (Magics, magics_class, line_magic,
                                    cell_magic, line_cell_magic)
import sys

from os.path import exists
from time import sleep
from os import remove
from IPython import get_ipython

if "ipykernel" in sys.modules:
    # This code can be put in any Python module, it does not require IPython
    # itself to be running already.  It only creates the magics subclass but
    # doesn't instantiate it yet.
    #refs:
    # https://ipython.readthedocs.io/en/stable/config/custommagics.html
    #and
    # https://stackoverflow.com/questions/61556938/packaging-a-python-project-and-its-associated-ipython-magic-extension
    #and
    # https://stackoverflow.com/questions/10361206/how-to-run-an-ipython-magic-from-a-script-or-timing-a-python-script

    # The class MUST call this class decorator at creation time
    @magics_class
    class MyMagics(Magics):

        @cell_magic
        def utestcell(self, line, cell):
            """Read the current cell's content, concatenate it with unittests to .py file and run unittests
            optional arguments:

              -c (concatenated file) : (str)
                  name of the file (default : code.py) containing a cell's code with
                  the unittests appended to it
              -v (verbose)
                  -v parameter passed to unittest module (verbosity of tests)
              -u (url) : (str)
                  url of unittest (e.g Raw link on Github)
              -ur (url + replace): (str)
                  same as above + erase unittest and redownload before running tests (useful to obtain latest version)
              -t : (str)
                  .py file containing the unittests on local machine
              -tr : (str)
                  same as above + erase unittest before running tests (useful to obtain latest version)
            """

            ipython = get_ipython()

            line = line.strip() #to remove any white spaces before/trailing

            verbose = False
            fname = 'code.py' #default name
            url = ''
            replace_unittest = False
            utest = 'utest.py'

            for p in line.split(" "): #go through the paraneters passed (can be passed
                #in any order)
                if p.strip() == '-v':
                    verbose = True

                elif p.strip()[0:3] == '-c:': #for concatenated (filename of
                    #concatenated .py file)
                    fname = p.strip()[3:]

                elif p.strip()[0:3] == '-u:': #u for url
                    url = p.strip()[3:]
                elif p.strip()[0:4] == '-ur:': #u for url
                    url = p.strip()[4:]
                    replace_unittest = True

                elif p.strip()[0:3] == '-t:': #t for test/unittest
                    utest = p.strip()[3:]

                #elif p.strip()[0:4] == '-tr:': #t for test/unittest and r for replace
                #    #i.e. download each time
                #    utestname = p.strip()[4:]
                #    replace_unittest = True

            #remove fname if it already exists to avoid errors
            while exists(fname):
                if exists(fname):
                    remove(fname)
                    #%rm $fname
                    sleep(0.001)

            #if we have a parameter starting with '-u:' and the file named utest.py
            #doesn't already exist
            # then download the unittest from the url
            if url != '':
                #test if file already exists, from url this is the last string after
                #last \ character
                utest = url.split('/')[-1]
                if replace_unittest == True and exists(utest) : #remove utest.py
                    #%rm $utest
                    remove(utest)
                    sleep(0.001)
                if not exists(utest):
                    #download file
                    import requests
                    r = requests.get(url, allow_redirects=False)
                    with open(utest, 'wb') as f:
                        f.write(r.content)

            #open the cell's and unit tests contents (if it exists), concatenate them
            #and save in fname
            with open(fname, 'wt') as fd:
                #first save content of cell in file 'fname'
                fd.write(cell)
                #next append the unit tests if utest.py exists
                if exists(utest):
                    with open(utest, 'rt') as u:
                        fd.write(u.read()) #here use .read() as unittest is a pointer

            while not exists(fname): #need to wait until the file exists.
                sleep(0.001)

            #run the python file with cell's content along with utest file, in verbose
            #mode by default,
            if '-v' in line.split(" "):
                #%run $fname -v
                command = "%run"+ " "+fname+" -v"
                #%run $fname -v
                ipython.magic(command)
            else:
                #%run $fname
                command = "%run"+ " "+fname
                #%run $fname
                ipython.magic(command)


    # In order to actually use these magics, must register them with a
    # running IPython.

    def load_ipython_extension(ipython):
        """
        Any module file that define a function named `load_ipython_extension`
        can be loaded via `%load_ext module.path` or be configured to be
        autoloaded by IPython at startup time.
        """
        #register the class itself without instantiating it.  IPython will
        # call the default constructor on it.
        ipython.register_magics(MyMagics)
