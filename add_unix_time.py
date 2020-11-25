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


import datetime
import time
import sys


delimiter = sys.argv[3]
time_format = sys.argv[4]
time_col = sys.argv[5]


with open(sys.argv[1], "r") as in_file:
    with open(sys.argv[2], "w") as out_file:
        first_line = in_file.readline()
        first_line = first_line.strip() + delimiter + "unix_t\n"
        first_line = first_line.split(delimiter)
        count = len(first_line)
        time_col_num = first_line.index(time_col)
        for line in in_file:
            line = line.strip()
            line = line.split(delimiter)
            line.append("{}\n".format(time.mktime(datetime.datetime.strptime(line[time_col_num], time_format).timetuple())))
            out_file.write(delimiter.join(line))
