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
        '-a','--ascii',
        dest='ascii',
        action='store_true',
        default = False,
        help='Use ascii codes to defined ignored beginnings instead of raw characters')
        
    parser.add_option(
        '-q','--fastq',
        dest='fastq',
        action='store_true',
        default = False,
        help='The input data in fastq format. It selected the script skips every even line since they contain sequence ids')

    parser.add_option(
        '-i','--ignore',
        dest='ignore',
        help='A comma separated list on ignored beginnings (e.g., ">,@"), or its ascii codes (e.g., "60,42") if option -a is enabled')

    parser.add_option(
        '-s','--start',
        dest='start',
        default = '0',
        help='Trim from beginning to here (1-based)')

    parser.add_option(
        '-e','--end',
        dest='end',
        default = '0',
        help='Trim from here to the ned (1-based)')

    parser.add_option(
        '-f','--file',
        dest='input_txt',
        default = False,
        help='Name of file to be chopped. STDIN is default')
            
    parser.add_option(
        '-c','--column',
        dest='col',
        default = '0',
        help='Column to chop. If 0 = chop the whole line')
       

    options, args = parser.parse_args()
    invalid_starts = []
    
    
    if options.input_txt:
        files = options.input_txt.split(',')
        for f in files:
            infile = open ( f, 'r')
            print f
            for line in infile:
                print line
                print "------------------- 00 ---"
                line = line.rstrip( '\r\n' )

                print line   


if __name__ == "__main__": main()






























