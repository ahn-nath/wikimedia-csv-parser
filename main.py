# get default/preferred engines
import pickle


def get_preferred_engines():
    """ Get the preferred engines from the mt-defaults.wikimedia.yaml file and saves them in a list.
    It uses pickling to use available files when already processed and save memory.  """
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
def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('started')
    preferred_engines_out = get_preferred_engines()
    print(preferred_engines_out)
