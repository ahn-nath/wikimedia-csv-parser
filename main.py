# get default/preferred engines
import os
import pickle
import yaml
import csv

# define constants
PATH = 'config_files'
DENY_LIST = ['{}/mt-defaults.wikimedia.yaml'.format(PATH), '{}/MWPageLoader.yaml'.format(PATH),
             '{}/languages.yaml'.format(PATH),
             '{}/JsonDict.yaml'.format(PATH), '{}/Dictd.yaml'.format(PATH), '{}/transform.js'.format(PATH),
             'test_files/mt-defaults.wikimedia_test.yaml', 'test_files/expected_output_test.csv']


def get_preferred_engines(file_path='{}/mt-defaults.wikimedia.yaml'.format(PATH), debug=False):
    """
        Get the preferred engines from the mt-defaults.wikimedia.yaml file and saves them in a list.
        It uses pickling to use available files when already processed and save memory.

        :return: a dictionary with the preferred engines
    """
    # check if file exists
    try:
        if debug:
            raise FileNotFoundError

        with open('preferred_engines.pickle', 'rb') as file:
            preferred_engines_data = pickle.load(file)

    # if it doesn't exist, create it
    except FileNotFoundError:
        # use yaml module to parse the file
        with open(file_path, 'r') as file:
            preferred_engines_data = yaml.safe_load(file)

        # save the list in a pickle file
        with open('preferred_engines.pickle', 'wb') as file:
            pickle.dump(preferred_engines_data, file)

    return preferred_engines_data


# parse the CSV file depending on the type of file (standard format or not)
def parse_csv(engine, standard, lines):
    """
        It parses the CSV file and returns a dictionary with the source and target languages as keys and the engine as value.

        :param engine:
        :param standard:
        :param lines:
        :return:
    """
    cvs_pairs_dict = {}

    # if standard input
    if standard:
        # iterate over each source (dictionary key) and their values
        for source in lines:
            # for each target (dictionary value) in array of source, add pair
            for target in lines[source]:
                cvs_pairs_dict["{}:{}".format(source, target)] = engine
    else:
        # remove special characters and save all languages to list
        languages = lines["languages"]
        # restrictions
        english_variants = ['en', 'simple']
        not_as_target = []

        # iterate over each language and get the source and target languages
        for lang in languages:
            # if lang is "False", replace with "no".
            # NOTE: the YAML library converts "no" to False for some strange reason
            lang = 'no' if not lang else lang
            for target in languages:
                # if target is "False", replace with "no".
                target = 'no' if not target else target
                # if the target language is not the source, and it's not in the not_as_target list,
                if (lang != target) and (target not in not_as_target):
                    # and it's not an english variant
                    if lang not in english_variants or target not in english_variants:
                        cvs_pairs_dict["{}:{}".format(lang, target)] = engine

    return cvs_pairs_dict


# generate the CSV file
def generate_csv(preferred_engines, output_file_name='output_files/cx_server_parsed.csv', source_file_path=PATH):
    """
        It parses specific files and generates a CSV file with the data that at least includes the source language,
        the target language, the translation engine used, and whether or not the translation engine is preferred or not

        :return: cvs strings generated for the cx_server_parsed.csv file
        :parameter: preferred_engines: a dictionary with the preferred engines

    """
    # parse each file
    # list for the lines of the CSV file
    csv_strings = ["source language,target language,translation engine,is preferred engine?"]

    # prepare the CSV file to write
    with open(output_file_name, 'w') as file_output:
        writer = csv.writer(file_output)
        writer.writerow(
            ["source language", "target language", "translation engine", "is preferred engine?"])

        # iterate over each file in the directory
        for f in os.listdir(source_file_path):
            # parse file
            with open(f'{source_file_path}/{f}') as file:
                if file.name not in DENY_LIST:
                    lines = yaml.safe_load(file)

                    # get the translation engine used
                    engine = os.path.splitext(f)[0]
                    standard = False if "languages" in lines else True

                    # parse the CSV file
                    cvs_pairs_dict = parse_csv(engine, standard, lines)

                    for key, value in cvs_pairs_dict.items():
                        # get source and target languages, check if the value or engine is the preferred to construct
                        source, target = key.split(':', 2)
                        engine = value
                        # we will mark as true if the engine is the preferred one in the preferred_engines dictionary
                        is_preferred = 'true' if preferred_engines.get(f'{source}-{target}') == engine else 'false'
                        # add the line to the CSV file
                        writer.writerow([source, target, engine, is_preferred])
    return csv_strings


if __name__ == '__main__':
    # get the preferred engines
    preferred_engines_out = get_preferred_engines()
    # generate the CSV file
    csv_strings_out = generate_csv(preferred_engines_out)
