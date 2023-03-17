# Wikimedia CSV Parser

## Project description

This is a simple parser for Wikimedia CSV files. It is designed to be used with
the "https://github.com/wikimedia/mediawiki-services-cxserver/tree/master/config" directory.

Essentially, it is a parser for these files and creates a single flat, in-memory structure with all of the supported
pairs. It exports the data in a list of accepted yaml files as a CSV of all pairs, with at least the following columns:

| source language | target language | translation engine is | preferred engine? |
|-----------------|-----------------|-----------------------|-------------------|
| de              | en              | DeepL                 | true              |


The configuration files have several file structures. Most have the source as the top-level key, and target
languages as a list of values under that key. Those with "handler" indicate a non-standard
interpretation for the file.

Some YAML files should be ignored, currently:

- MWPageLoader.yaml,
- languages.yaml,
- JsonDict.yaml,
- Dictd.yaml
- mt-defaults.wikimedia.yaml.

The mt-defaults.wikimedia.yaml file is considered for the supported translation pairs and
default translation engine for each pair of the last column in our generated CSV file.

## Installation

#### Requirements

* Python 3.6 or higher
* pip
* git

#### Setup

* Clone the repository

  `git clone ahn-nath/wikimedia-csv-parser`
  
* Test the project
  
  `python test.py`
  
* Run the script

  `python main.py`




 
