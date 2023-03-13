# get default/preferred engines
import os
import pickle

# define constants
import re

PATH = 'yaml_files'
# TODO: handle the second list case later
DENY_LIST = ['yaml_files/mt-defaults.wikimedia.yaml', 'yaml_files/MWPageLoader.yaml', 'yaml_files/languages.yaml',
             'yaml_files/JsonDict.yaml', 'yaml_files/Dictd.yaml', 'yaml_files/transform.js'] + [
                'yaml_files/Google.yaml', 'yaml_files/Yandex.yaml']


def get_preferred_engines():
    """ Get the preferred engines from the mt-defaults.wikimedia.yaml file and saves them in a list.
    It uses pickling to use available files when already processed and save memory.

    The output would look like this:
     {'af-nl': 'Apertium', 'ar-mt': 'Apertium', 'be-ru': 'Apertium', 'bg-mk': 'Apertium'...}

    TODO: add return value and enrich docstring
    """
    # check if file exists
    try:
        with open('preferred_engines.pickle', 'rb') as file:
            preferred_engines = pickle.load(file)

    # if it doesn't exist, create it
    except FileNotFoundError:
        # open file and read each line
        with open('yaml_files/mt-defaults.wikimedia.yaml', 'r') as file:
            lines = file.readlines()
        # get the preferred engines
        preferred_engines = {}
        for line in lines:
            if line:
                key = line.split(':')[0].strip()
                value = line.split(':')[1].strip()
                preferred_engines[key] = value

        # save the list in a pickle file
        with open('preferred_engines.pickle', 'wb') as file:
            pickle.dump(preferred_engines, file)

    return preferred_engines


# generate the CSV file
def generate_csv(preferred_engines):
    """ It parses specific files and generates a CSV file with the data that at least includes the source language,
    the target language, the translation engine used, and whether or not the translation engine is preferred or not

    # TODO: add return value, parameters, and enrich docstring
    """
    # parse each file
    for file in os.listdir(PATH):
        # parse file
        with open(file, 'rb') as file:
            if file not in DENY_LIST:
                lines = file.readlines()

        # get the translation engine used
        cvs_pairs_dict = {}
        engine = file.name.split('.')[0]
        standard = False if "languages:" in lines[2] else True  # TODO: this depends on whether the file has a languages key or not
        # if standard
        if standard:
            for line in lines:
                if line:
                    # get the source language
                    if ":" in line:
                        source = line.split(':')[0].strip()
                    # get the target language
                    else:
                        target = line.split('-')[1].strip()

                    cvs_pairs_dict["{}-{}".format(source, target)] = engine

        else:
            # languages list
            # regex to remove non-alphabetic characters
            languages = re.sub(r'[^a-zA-Z]', '', lines[2:]).split(',')
            # restrictions
            english_variants = ['en', 'simple']
            not_as_target = []
            for lang in languages:
                for target in languages:
                    # if the target language is not the source language and it's not in the not_as_target list,
                    # and it's not an english variant
                    if (lang != target) and (target not in not_as_target) and (lang and target not in english_variants):
                        cvs_pairs_dict["{}-{}".format(lang, target)] = engine

    # list for the lines of the CSV file
    csv_strings = []
    # iterate over dictionary and handle each case
    for key, value in cvs_pairs_dict.items():
        # get the source and target languages from key, check if the value or engine is the preferred to construct
        source, key = key.split('-')
        is_preferred = 'true' if preferred_engines.get(f'{source}-{target}') == engine else 'false'
        csv_string = f"{source},{target},{engine},{is_preferred}"

        # TODO: we will append to list but later write to file
        csv_strings.append(csv_string)

    # after processing all the files, write the list to a CSV file
    # TODO: change to CSV format and add header
    with open('cx_server_parsed.txt', 'w') as f:
        f.writelines([f"{x}\n" for x in csv_strings])

    return csv_strings


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('started')
    # get the preferred engines
    preferred_engines_out = get_preferred_engines()
    print(preferred_engines_out)

    # generate the CSV file
    csv_strings_out = generate_csv(preferred_engines_out)
    print(csv_strings_out)
