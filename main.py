# get default/preferred engines
import os
import pickle

# define constants
PATH = 'yaml_files'
# TODO: handle the second list case later
DENY_LIST = ['yaml_files/mt-defaults.wikimedia.yaml', 'yaml_files/MWPageLoader.yaml', 'yaml_files/languages.yaml',
             'yaml_files/JsonDict.yaml', 'yaml_files/Dictd.yaml'] + ['yaml_files/Google.yaml', 'yaml_files/Yandex.yaml']


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
        engine = file.name.split('.')[0]
        csv_string = ''
        csv_strings = []
        for line in lines:
            if line:
                # get the source language
                if ":" in line:
                    source = line.split(':')[0].strip()
                # get the target language
                else:
                    target = line.split('-')[1].strip()

                # get whether the translation engine is preferred or not
                if source and target:
                    is_preferred = 'true' if preferred_engines.get(f'{source}-{target}') == engine else 'false'
                    csv_string = f"{source},{target},{engine},{is_preferred}"
                    # TODO: we will append to list but later write to file
                    csv_strings.append(csv_string)

    return csv_strings


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('started')
    preferred_engines_out = get_preferred_engines()
    print(preferred_engines_out)
