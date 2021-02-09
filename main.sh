#!/bin/sh

#   Copyright 2020 InfAI (CC SES)
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.


# Environment variables:
#
# $DEP_INSTANCE
# $JOB_CALLBACK_URL
# $input_csv
# $delimiter
# $time_format
# $time_column
# $unique_column
# $separator


output_file="$(cat /proc/sys/kernel/random/uuid | echo $(read s; echo ${s//-}))"
input_file_path="/data_cache/${input_csv}"
output_file_path="/data_cache/${output_file}"

echo "adding unix timestamps ..."
if python -u add_unix_time.py "$input_file_path" "${input_file_path}_1" "$delimiter" "$time_format" "$time_column"; then
    head -5 "${input_file_path}_1"
    sed_string="s/[^$delimiter]//g"
    col_num=$(head -1 "${input_file_path}_1" | sed $sed_string | wc -c)
    echo "sorting lines ..."
    if sort -n -t $delimiter -k $col_num "${input_file_path}_1" > "${input_file_path}_2"; then
        head -5 "${input_file_path}_2"
        let col_num=col_num-1
        echo "removing unix timestamps ..."
        if cut -d $delimiter -f "1"-$col_num "${input_file_path}_2" > "${input_file_path}_3"; then
            head -5 "${input_file_path}_3"
            first_line=$(head -n 1 $input_file_path)
            echo "flattening ..."
            if python -u flatten.py "${input_file_path}_3" "$output_file_path" "$first_line" "$unique_column" "$time_column" "$delimiter" "$separator"; then
                head -5 "$output_file_path"
                echo "total number of lines written:" $(( $(wc -l < "$output_file_path") - 1 ))
                if ! curl -s -S --header 'Content-Type: application/json' --data "{\""$DEP_INSTANCE"\": {\"output_csv\": \""$output_file"\"}}" -X POST "$JOB_CALLBACK_URL"; then
                    echo "callback failed"
                    rm "$output_file_path"
                fi
            else
                echo "flattening failed"
            fi
        else
            echo "removing unix timestamps failed"
        fi
    else
        echo "sorting lines failed"
    fi
else
    echo "adding unix timestamps failed"
fi

if [ -f "${input_file_path}_1" ]; then
    rm "${input_file_path}_1"
fi
if [ -f "${input_file_path}_2" ]; then
    rm "${input_file_path}_2"
fi
if [ -f "${input_file_path}_3" ]; then
    rm "${input_file_path}_3"
fi
