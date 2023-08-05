import argparse
# import os
import sys
import json


def main():
    parser = argparse.ArgumentParser(prog='vinset',
                                     description='VINSET package.')
    parser.add_argument('--version', action='version', version='1.0.1'),
    parser.add_argument("-i", dest="input_filename", required=True, type=argparse.FileType('r'), default=sys.stdin,
                        help="input mp4 file", metavar="filename.mp4")
    parser.add_argument("-o", dest="output_filename", required=True, type=argparse.FileType('w'), default=sys.stdout,
                        help="output mp4 file", metavar="filename.mp4")
    parser.add_argument("-c", dest="config_filename", required=True, type=argparse.FileType('r'), default=sys.stdin,
                        help="config jason file", metavar="filename.json")

    args = parser.parse_args()
    input_file = args.input_filename.name
    output_file = args.output_filename.name
    config_file = args.config_filename.name

    if str(input_file).endswith(".mp4"):
        print("Input file name:", input_file)
    else:
        print("Input file must be mp4.")
    if str(output_file).endswith(".mp4"):
        print("Output file name:", output_file)
    else:
        print("Output file must be mp4.")
    if str(config_file).endswith(".json"):
        print("Config file name:", config_file)
    else:
        print("Config file must be json.")

    load_success = False

    try:
        f = open(config_file)
        data = json.load(f)
        print(f"{config_file} is loaded successfully by json.")
        load_success = True
    except ValueError:
        print(f"{config_file} cannot be loaded by json.")

    if load_success:
        title = data["title"]
        # graph_position = data["position"]
        # # start point
        # graph_position_x = graph_position["x"]
        # graph_position_y = graph_position["y"]
        # graph_position_width = graph_position["width"]
        # graph_position_height = graph_position["height"]
        # graph_background = data["background"]
        # graph_background_fill = graph_background["fill"]
        # graph_background_opacity = graph_background["opacity"]
        # graph_y_limit = data["y-limit"]
        # graph_y_limit_type = graph_y_limit["type"]
        # graph_y_limit_limits = graph_y_limit["limits"]
        # graph_y_limit_limits_lower = graph_y_limit_limits["lower"]
        # graph_y_limit_limits_upper = graph_y_limit_limits["upper"]
        # graph_t_limit = data["x-limit"]
        # graph_t_limit_type = graph_t_limit["type"]
        # graph_t_limit_width = graph_t_limit["width"]
        # graph_series = data["series"]
        # graph_series_name = graph_series["name"]
        # # graph_series_type = gr
