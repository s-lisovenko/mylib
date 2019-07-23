#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import sys

usage_template = "Использование: {} <директория проекта> <относительная директория с заголовками>"
usage = usage_template.format(sys.argv[0])

project_directory = sys.argv[1]
relative_include_directory = sys.argv[2]
include_directory = os.path.join(project_directory, relative_include_directory)
header_files =\
    [os.path.join(root, x) for root, _, files in os.walk(include_directory) for x in files]

def prepare_includes (root_directory, header_files):
    def get_rel_path (path):
        return os.path.relpath(path, root_directory)

    return [{"file": get_rel_path(file), "code": open(file).read()} for file in header_files]

code = """#include <mylib/myfeature.hpp>

int main ()
{
    mylib::myfunc(mylib::mystruct{});
}"""

request = json.dumps({
    "code": code,
    "options": "warning,c++17",
    "compiler": "gcc-7.3.0",
    "compiler-option-raw": "-I{}".format(relative_include_directory),
    "codes": prepare_includes(project_directory, header_files),
    "save": False})

print(request)
