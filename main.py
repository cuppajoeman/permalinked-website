import uuid
import re
import os
import json
from os import walk

script_directory = os.path.dirname(os.path.realpath(__file__))
os.chdir("content")
content_directory = os.getcwd()

directory_structure = {}

file_path_to_new_path = {}


def add_uuid_to_files_without_one():
    for dir_path, dirs, file_names in walk(content_directory):
        for name in file_names:

            uuid_already_in_filename = "UUID_" in name

            if not uuid_already_in_filename:
                full_path = os.path.join(dir_path, name)
                filename_no_extension, extension = os.path.splitext(name)
                generated_UUID = uuid.uuid4()
                new_path = os.path.join(dir_path, f"{filename_no_extension}_UUID_{generated_UUID}{extension}")

                file_path_to_new_path[full_path] = new_path

    for file_path, new_path in file_path_to_new_path.items():
        os.rename(file_path, new_path)


# we know all files now have a uuid with them

add_uuid_to_files_without_one()


def generate_uuid_to_paths():
    uuid_to_path = {}
    for dir_path, dirs, file_names in walk(content_directory):
        for name in file_names:
            if (match := re.search(r"UUID_(.*?)\.", name)) is not None:
                full_path = os.path.join(dir_path, name)
                relative_path = os.path.relpath(full_path, content_directory)
                uuid_in_name = match.group(1)
                uuid_to_path[uuid_in_name] = relative_path

    return uuid_to_path


def write_to_json(data):
    os.chdir("..")
    with open('uuid_to_paths.json', 'w') as fp:
        json.dump(data, fp, indent=4)


write_to_json(generate_uuid_to_paths())
