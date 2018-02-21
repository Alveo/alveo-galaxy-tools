'''
Created on 12 Oct 2016

@author: rui
'''
#!/usr/bin/env python

import sys
import optparse

def stop_err( msg ):
    sys.stderr.write( msg )
    sys.exit()

def main():
    usage = """%prog [options]
    
options (listed below) default to 'None' if omitted
    """
    parser = optparse.OptionParser(usage=usage)
    
    
    parser.add_option(
        '-d','--delimiter',
        dest='delim',
        default = False,
        help='define the file delimiter')
    
    parser.add_option(
        '-f','--file',
        dest='input_txt',
        default = False,
        help='Name of file to be chopped. STDIN is default')
       

    options, args = parser.parse_args()
    delimiter = "\n"
    
    if options.delim != '':
        delimiter = options.delim
        

    if options.input_txt:
        files = options.input_txt.split(',')
        for f in files:
            infile = open ( f, 'r')
            print delimiter 
            for line in infile:
                line = line.rstrip( '\r\n' )
                print line   


if __name__ == "__main__": main()






























