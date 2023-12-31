# import sys
# import json
# import os

# def load_parser(origin):
#     parser_module = __import__(f"parsers.{origin}", fromlist=[''])
#     return parser_module

# def filter_data_for_origin(data, origin):
#     return [item for item in data if item.get('origin') == origin]

# def process_data(origin, data):
#     parser = load_parser(origin)
#     return parser.parse_data(data)

# def save_data(extracted_data, output_file):
#     with open(output_file, 'w') as outfile:
#         json.dump(extracted_data, outfile, indent=2)

# if __name__ == "__main__":
#     input_file = sys.argv[1]
#     output_file = sys.argv[2]
#     origin = sys.argv[3]

#     with open(input_file, 'r') as file:
#         data = json.load(file)

#     filtered_data = filter_data_for_origin(data, origin)
#     extracted_data = process_data(origin, filtered_data)
#     save_data(extracted_data, output_file)

#     print(f"Data extracted and saved to {output_file}")

import sys
import json
import os
import glob

def load_parser(origin):
    parser_module = __import__(f"parsers.{origin}", fromlist=[''])
    return parser_module

def filter_data_for_origin(data, origin):
    return [item for item in data if item.get('origin') == origin]

def process_data(origin, data):
    parser = load_parser(origin)
    return parser.parse_data(data)

def save_data(extracted_data, origin):
    os.makedirs('data', exist_ok=True)
    output_file = f"data/{origin}.json"
    with open(output_file, 'w') as outfile:
        json.dump(extracted_data, outfile, indent=2)
    print(f"Data extracted and saved to {output_file}")

def get_all_parsers():
    parser_files = glob.glob('parsers/*.py')
    return [os.path.basename(f)[:-3] for f in parser_files if not f.endswith('__init__.py')]

if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else 'plots.json'
    parsers = sys.argv[2:] if len(sys.argv) > 2 else get_all_parsers()

    with open(input_file, 'r') as file:
        data = json.load(file)

    for origin in parsers:
        filtered_data = filter_data_for_origin(data, origin)
        extracted_data = process_data(origin, filtered_data)
        save_data(extracted_data, origin)
