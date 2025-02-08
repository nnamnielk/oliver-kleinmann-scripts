#!/usr/bin/env python3


import requests
import urllib.request
import time
import logging

#TODO - add support for non-german langs

def get_mp3(save_to_path,word):
    logging.info('Getting mp3 for:'+word+'.')
    #get dictcc's id for the word
    url = "https://de-en.dict.cc/?s=" + word
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    logging.debug('Going to url: '+url+' ,to get word ID.')
    response = requests.get(url,headers=headers)
    if response.status_code != 200:
        logging.error("Can't get word="+word+" from URL.")
    webhtml=response.text
    logging.debug('Searching for ID in dict.cc web content...')
    id=webhtml[webhtml.find('var idArr'):].split(',')[1]
    logging.info('Found id='+id+'. YAAAAAY!!!!')
    
    
    #download audio
    audio_url = "https://audio.dict.cc/speak.audio.v2.php?error_as_text=1&type=mp3&lang=de_rec_ip&lp=DEEN&id=" + str(id)
    #this is not friendly; have to chat with site owner, explain its for anki
    logging.info('Going to URL='+audio_url+' to get mp3.')
    doc = requests.get(audio_url,headers=headers)
    logging.debug('Writing mp3 to: '+save_to_path+'.')
    with open(save_to_path, 'wb') as f:
        f.write(doc.content)
    
    
    
if __name__ == "__main__":
    import argparse
    logging.basicConfig(level=logging.DEBUG)
    #parse args
    parser = argparse.ArgumentParser()
    parser.add_argument("word", help="generates anki card for word")
    parser.add_argument("-v", "--verbose", action="store_true", help="increase output verbosity")
    args = parser.parse_args()
    word = args.word
    #TODO - change path
    save_to_path = word + ".mp3"
    get_mp3(save_to_path,word)

