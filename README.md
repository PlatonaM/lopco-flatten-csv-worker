#### Description

    {
        "name": "Flatten CSV",
        "image": "platonam/lopco-flatten-csv-worker:latest",
        "data_cache_path": "/data_cache",
        "description": "Flatten a Comma-Separated Values file.",
        "configs": {
            "delimiter": null,
            "time_column": null,
            "unique_column": null,
            "time_format": null,
            "name_pattern": null
        },
        "input": {
            "type": "single",
            "fields": [
                {
                    "name": "input_csv",
                    "media_type": "text/csv",
                    "is_file": true
                }
            ]
        },
        "output": {
            "type": "single",
            "fields": [
                {
                    "name": "output_csv",
                    "media_type": "text/csv",
                    "is_file": true
                }
            ]
        }
    }

For the timestamp format as required by `time_format` please use these [format codes](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes).

----

The `name_pattern` config option defines how the names for new columns are generated and requires the following two placeholders:

- `unique_item`
- `column_name`

If the optional `unique_column` placeholder is provided the value of the `unique_column` config option will be added to the generated column names.

Examples:

`name_pattern` = `{unique_column}_{unique_item}_{column_name}`

    time,location,power
    2021-02-01T05:00:00.000Z,ec-total,4454.38330078125
    2021-02-01T05:00:00.000Z,wm2-total,24993.80078125
    2021-02-01T05:00:00.000Z,wm2-heater,7296.2548828125

result:

    time,location_ec-total_power,location_wm2-total_power,location_wm2-heater_power
    2021-02-01T05:00:00.000Z,4454.38330078125,24993.80078125,7296.2548828125

`name_pattern` = `{unique_item}_{column_name}`

    time,location,power
    2021-02-01T05:00:00.000Z,ec-total,4454.38330078125
    2021-02-01T05:00:00.000Z,wm2-total,24993.80078125
    2021-02-01T05:00:00.000Z,wm2-heater,7296.2548828125

result:

    time,ec-total_power,wm2-total_power,wm2-heater_power
    2021-02-01T05:00:00.000Z,4454.38330078125,24993.80078125,7296.2548828125