#!/usr/bin/env python3

import csv
import sys
import time
import dictcc_audio
import logging


#outline
#   open csv
#   asign names for each german word
#   call dict.cc script


def process_csv(prefix,csv,outputDirPath,startAt):
    suffixnum=0
    suffixstr="0"
    
    with open(csv, 'r') as csv:
        logging.debug('opening path '+outputDirPath)
        lines=csv.readlines()
        logging.info('Generating mp3 file names...')
        for i in range(len(lines)):
            suffixnum+=1
            suffixstr=str(suffixnum)
            while len(str(suffixstr)) < 4:
                suffixstr="0"+suffixstr
            lines[i]=(str(prefix)+suffixstr+'.mp3',lines[i])
        logging.info('Names successfully generated!')
    
        lineNo = 0
        
        for j in lines[startAt:]:
            logging.debug('Waiting 3 seconds before calling...')
            time.sleep(3)
            path = outputDirPath + "/" + j[0]
            word = j[1]
            try:
                wort = getWort(word)
            except:
                logging.error("input has apparent bad word at line " + (lineNo+1) + ": " + word);
                sys.exit(1)
            logging.info('Saving word '+wort+'to path '+path)
            logging.debug('Calling dictcc_audio...')
            dictcc_audio.get_mp3(path,wort)
            lineNo+=1
        logging.info('Operation successful!')



def getWort (inputString):

    chunks = inputString.lower().split(' ')
    
    tmpWord = chunks[0]
    if( chunks[0] == "die" or chunks[0] == "der" or chunks[0] == "das" ):
        tmpWord = chunks[1]
    
    
    chars = list(tmpWord)
    
    
    buff = []
    
    
    keepParens = False
    inParens = False
    
    for i in range(0,len(chars)):
        c = chars[i]
        if(c == "("):
            inParens = True
            if(i == 0):
                keepParens = True
            continue
        if(c == ")"):
            inParens = False
            keepParens = False
            continue
        if(inParens):
            if(keepParens):
                buff.append(c)
            continue
        buff.append(c)
        
    #TODO - convert buff to string
    #return join("",buff)
    return ''.join(buff)
    
    
    
    



if __name__ == "__main__":
    import argparse
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser(epilog="TODOs - add python doc for functions; write anki decks")
    parser.add_argument('prefix', help="prefix for mp3 files; should be in the form 'XX-', where XX = chapter number")
    parser.add_argument("--csv", help="downloads mp3s for words in csv, defaults to dictSearch.csv",default="dictSearch.csv")
    parser.add_argument("--dir", help="directory where mp3s are saved, defaults to results/",default="results")
    parser.add_argument("--startAt", help="line to start processing",default=1)
    args = parser.parse_args()
    outputDir = args.dir

    #create output dir if it does not exist
    import os
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)

    process_csv(args.prefix,args.csv,outputDir,args.startAt-1)

