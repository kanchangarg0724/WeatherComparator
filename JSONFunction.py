import json
import config


def get_input():

    try:
        # Opening JSON file
        f = open('data.json')

        # returns JSON object as a dictionary
        data = json.load(f)

        # Closing file
        f.close()

        return data

    except Exception as err:
        print("Error: %s" % err)


def output_data():

    try:

        # Serializing json
        json_object = json.dumps(config.temp_output, indent=4)

        # Generating json output file
        with open("result.json", "w") as outfile:
            outfile.write(json_object)

    except Exception as err:
        print("Error: %s" % err)