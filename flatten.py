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


import uuid
import os
import requests


dep_instance = os.getenv("DEP_INSTANCE")
job_callback_url = os.getenv("JOB_CALLBACK_URL")
input_file = os.getenv("input_csv")
delimiter = os.getenv("delimiter")
unique_col = os.getenv("unique_column")
time_col = os.getenv("time_column")
name_pattern = os.getenv("name_pattern")
data_cache_path = "/data_cache"


with open("{}/{}".format(data_cache_path, input_file), "r") as in_file:
    old_first_line = in_file.readline().strip().split(delimiter)
    time_col_num = old_first_line.index(time_col)
    unique_col_num = old_first_line.index(unique_col)
    unique_items = list()
    for line in in_file:
        line = line.split(delimiter)
        if line[unique_col_num] not in unique_items:
            unique_items.append(line[unique_col_num])

new_first_line = [time_col]
fields = old_first_line.copy()
fields.remove(unique_col)
fields.remove(time_col)

for item in unique_items:
    if "unique_column" in name_pattern:
        new_first_line = new_first_line + [name_pattern.format(unique_column=unique_col, unique_item=item, column_name=field) for field in fields]
    else:
        new_first_line = new_first_line + [name_pattern.format(unique_item=item, column_name=field) for field in fields]

new_first_line_map = dict()

for pos in range(len(new_first_line)):
    new_first_line_map[new_first_line[pos]] = pos

reserved_pos = (time_col_num, unique_col_num)
output_file = uuid.uuid4().hex

print("flattening ...")
with open("{}/{}".format(data_cache_path, input_file), "r") as in_file:
    with open("{}/{}".format(data_cache_path, output_file), "w") as out_file:
        out_file.write("{}\n".format(delimiter.join(new_first_line)))
        current_timestamp = None
        line_count = 0
        for line in in_file:
            line = line.strip()
            line = line.split(delimiter)
            if line[time_col_num] != current_timestamp:
                try:
                    out_file.write("{}\n".format(delimiter.join(flat_line)))
                    line_count += 1
                except NameError:
                    pass
                flat_line = [str()] * len(new_first_line)
                flat_line[0] = line[time_col_num]
                current_timestamp = line[time_col_num]
            for pos in range(len(line)):
                if pos not in reserved_pos:
                    if "unique_column" in name_pattern:
                        flat_line[new_first_line_map[name_pattern.format(unique_column=unique_col, unique_item=line[unique_col_num], column_name=old_first_line[pos])]] = line[pos]
                    else:
                        flat_line[new_first_line_map[name_pattern.format(unique_item=line[unique_col_num], column_name=old_first_line[pos])]] = line[pos]
        out_file.write("{}\n".format(delimiter.join(flat_line)))
        line_count += 1

with open("{}/{}".format(data_cache_path, output_file), "r") as file:
    for x in range(5):
        print(file.readline().strip())
print("total number of lines written: {}".format(line_count))

try:
    resp = requests.post(
        job_callback_url,
        json={dep_instance: {"output_csv": output_file}}
    )
    if not resp.ok:
        raise RuntimeError(resp.status_code)
except Exception as ex:
    try:
        os.remove("{}/{}".format(data_cache_path, output_file))
    except Exception:
        pass
    raise ex
