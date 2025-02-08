#!/usr/bin/env python

import genanki

#TODO - 
#store ids in 'id.file' with data; 
#if no id.file exists, generate it with ids, then read
#Anki behavior is to replace decks and models that have have the same id 
#as the deck/model we are importing.
#deck_id  = random.randrange(1 << 30, 1 << 31)
#model_id = random.randrange(1 << 30, 1 << 31)
deck_id  = 2059400110
model_id = 1607392319

#TODO - 
#we should get the model from the headers in the csv
#and the card templates from files
my_model = genanki.Model(
  model_id,
  'German3 Model',
  fields=[
    #Filename,Deutsch,Englisch,Satz,Bild, Klang
    #D01-01,Der Loeffel-,Spoon,Besteck Suppe zu essen,<image>,<sound>
    {'name': 'Filename'},
    {'name': 'Deutsch'},
    {'name': 'Englisch'},
    {'name': 'Satz'},
    {'name': 'Bild'},
    {'name': 'Klang'},
  ],
  templates=[
    {
      'name': 'Card 3',
      'qfmt': '{{Bild}}',
      'afmt': '{{FrontSide}} <hr id=answer> {{Deutsch}} {{Klang}}',
    },
  ])

my_deck = genanki.Deck( deck_id, 'German3')

my_media = []

#TODO - get the card data here by looping through the csv
#TODO - get dirs where media is stored from argparse
#TODO - later -  fix genanki so that the model fields can take a type, and if the type is sound, 
#       it decorates the column with [sound:<sound file>], and it its an image, with '<image src="xxxx">
my_note = genanki.Note(
  model=my_model,
  fields=['D01-01','Der Loeffel-','Spoon','Besteck Suppe zu essen','<img src="D01-01.jpg">','[sound:D01-01.mp3]' ])
my_media.append('images/D01-01.jpg')
my_media.append('sounds/D01-01.mp3')
my_deck.add_note(my_note)

#TODO - get name of the output apkg from argparse
apkg_file = 'output.apkg'
my_package = genanki.Package(my_deck)
if len(my_media) > 0:
  my_package.media_files = my_media
my_package.write_to_file(apkg_file)

print("you can load " + apkg_file + " into Anki using File -> Import...")

