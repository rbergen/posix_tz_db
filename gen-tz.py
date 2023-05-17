#!/usr/bin/env python

# This script is based on the one in https://github.com/nayarsystems/posix_tz_db. As such, this script is subject to the
# MIT license.

import sys
import argparse
import json
import os

ZONES_ROOT = "/usr/share/zoneinfo/"
ZONES_DIRS = [
    "Africa",
    "America",
    "Antarctica",
    "Arctic",
    "Asia",
    "Atlantic",
    "Australia",
    "Europe",
    "Indian",
    "Pacific",
    "Etc"
]


def traverse_directory_trees(parent_directory, directory_list):
    contents = []

    def traverse_directory(directory):
        absolute_directory = os.path.join(parent_directory, directory)
        items = sorted(os.listdir(absolute_directory))
        for item in items:
            item_path = os.path.join(directory, item)
            absolute_item_path = os.path.join(absolute_directory, item)
            if os.path.isfile(absolute_item_path):
                contents.append(item_path)
            else:
                traverse_directory(item_path)

    for directory in directory_list:
        traverse_directory(directory)

    return contents


def get_tz_string(timezone):
    data = open(ZONES_ROOT + timezone, "rb").read().split(b"\n")[-2]
    return data.decode("utf-8")


def make_timezones_dict(timezones):
    result = {}
    for timezone in timezones:
        timezone = timezone.strip()
        result[timezone] = get_tz_string(timezone)
    return result


def print_csv(timezones_dict):
    for name, tz in timezones_dict.items():
        print('"{}","{}"'.format(name, tz))


def print_json(timezones_dict):
    json.dump(timezones_dict, sys.stdout, indent=0, sort_keys=False, separators=(",", ":"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generates POSIX timezones strings reading data from " + ZONES_ROOT)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-j", "--json", action="store_true", help="outputs JSON")
    group.add_argument("-c", "--csv", action="store_true", help="outputs CSV")
    data = parser.parse_args()

    timezones_list = traverse_directory_trees(ZONES_ROOT, ZONES_DIRS)
    timezones_dict = make_timezones_dict(timezones_list)

    if data.json:
        print_json(timezones_dict)
    else:
        print_csv(timezones_dict)
