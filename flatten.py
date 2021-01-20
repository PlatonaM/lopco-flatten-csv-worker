"""
   Copyright 2020 InfAI (CC SES)
   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at
       http://www.apache.org/licenses/LICENSE-2.0
   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""


import sys


old_first_line = sys.argv[3]
delimiter = sys.argv[6]
separator = sys.argv[7]

old_first_line = old_first_line.strip()
old_first_line = old_first_line.split(delimiter)
unique_col_num = old_first_line.index(sys.argv[4])
time_col_num = old_first_line.index(sys.argv[5])

with open(sys.argv[1], "r") as in_file:
    unique_items = list()
    for line in in_file:
        line = line.split(delimiter)
        if line[unique_col_num] not in unique_items:
            unique_items.append(line[unique_col_num])

new_first_line = [sys.argv[5]]
fields = old_first_line.copy()
fields.remove(sys.argv[4])
fields.remove(sys.argv[5])

for item in unique_items:
    new_first_line = new_first_line + ["{}{}{}".format(field, separator, item) for field in fields]

new_first_line_map = dict()

for pos in range(len(new_first_line)):
    new_first_line_map[new_first_line[pos]] = pos

reserved_pos = (time_col_num, unique_col_num)

with open(sys.argv[1], "r") as in_file:
    with open(sys.argv[2], "w") as out_file:
        out_file.write("{}\n".format(delimiter.join(new_first_line)))
        current_timestamp = None
        for line in in_file:
            line = line.strip()
            line = line.split(delimiter)
            if line[time_col_num] != current_timestamp:
                try:
                    out_file.write("{}\n".format(delimiter.join(flat_line)))
                except NameError:
                    pass
                flat_line = [str()] * len(new_first_line)
                flat_line[0] = line[time_col_num]
                current_timestamp = line[time_col_num]
            for pos in range(len(line)):
                if pos not in reserved_pos:
                    flat_line[new_first_line_map[old_first_line[pos] + separator + line[unique_col_num]]] = line[pos]
        out_file.write("{}\n".format(delimiter.join(flat_line)))
