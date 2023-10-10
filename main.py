import uuid
import re
import os
import json
from os import walk


def get_content_directory():
    with open('configuration.json') as f:
        d = json.load(f)
        s = "content_directory_relative_to_this_file"
        assert s in d
        content_directory = d[s]
        return content_directory


def add_uuid_to_files_without_one():
    file_path_to_new_path = {}
    for dir_path, dirs, file_names in walk(content_directory):

        if "permalinked-website" in dir_path:
            continue


        for name in file_names:
            print(dir_path, name)

            relative_path = os.path.relpath(dir_path, content_directory)

            current_file_is_root_index = relative_path == "." and name == "index.html"

            if current_file_is_root_index:
                continue

            uuid_already_in_filename = "UUID_" in name

            if not uuid_already_in_filename:
                full_path = os.path.join(dir_path, name)
                filename_no_extension, extension = os.path.splitext(name)
                generated_UUID = uuid.uuid4()
                new_path = os.path.join(dir_path, f"{filename_no_extension}_UUID_{generated_UUID}{extension}")

                file_path_to_new_path[full_path] = new_path

    for file_path, new_path in file_path_to_new_path.items():
        os.rename(file_path, new_path)


def generate_uuid_to_paths():
    uuid_to_path = {}
    for dir_path, dirs, file_names in walk(content_directory):

        if "permalinked-website" in dir_path:
            continue

        for name in file_names:
            if (match := re.search(r"UUID_(.*?)\.", name)) is not None:
                full_path = os.path.join(dir_path, name)
                relative_path = os.path.relpath(full_path, content_directory)
                uuid_in_name = match.group(1)
                uuid_to_path[uuid_in_name] = relative_path

    return uuid_to_path


def write_to_json(data):
    with open('uuid_to_paths.json', 'w') as fp:
        json.dump(data, fp, indent=4)


if __name__ == "__main__":

    content_directory = get_content_directory()

    script_directory = os.path.dirname(os.path.realpath(__file__))
    os.chdir(content_directory)
    content_directory = os.getcwd()

    add_uuid_to_files_without_one()
     
    os.chdir(script_directory)
    # we know all files now have a uuid with them
    write_to_json(generate_uuid_to_paths())
