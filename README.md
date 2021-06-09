## lopco-flatten-csv-worker

Flattens a CSV file containing multiple lines per timestamp.

### Configuration

`delimiter`: Delimiter used in the CSV file.

`time_column`: Column containing timestamps.

`name_pattern`: Defines how names for new columns are generated and requires the placeholders `unique_item` and `column_name`:

`unique_column`: If provided, the given value is added to the names of newly generated columns.

    Examples:
    
    name_pattern = {unique_column}_{unique_item}_{column_name}
    
        time,location,power
        2021-02-01T05:00:00.000Z,ec-total,4454.38330078125
        2021-02-01T05:00:00.000Z,wm2-total,24993.80078125
        2021-02-01T05:00:00.000Z,wm2-heater,7296.2548828125
    
    result:
    
        time,location_ec-total_power,location_wm2-total_power,location_wm2-heater_power
        2021-02-01T05:00:00.000Z,4454.38330078125,24993.80078125,7296.2548828125
    
    name_pattern` = {unique_item}_{column_name}
    
        time,location,power
        2021-02-01T05:00:00.000Z,ec-total,4454.38330078125
        2021-02-01T05:00:00.000Z,wm2-total,24993.80078125
        2021-02-01T05:00:00.000Z,wm2-heater,7296.2548828125
    
    result:
    
        time,ec-total_power,wm2-total_power,wm2-heater_power
        2021-02-01T05:00:00.000Z,4454.38330078125,24993.80078125,7296.2548828125

### Inputs

Type: single

`input_csv`: CSV file to flatten.

### Outputs

Type: single

`output_csv`: Result CSV file.

### Description

    {
        "name": "Flatten CSV",
        "image": "platonam/lopco-flatten-csv-worker:latest",
        "data_cache_path": "/data_cache",
        "description": "Flatten a Comma-Separated Values file.",
        "configs": {
            "delimiter": null,
            "time_column": null,
            "unique_column": null,
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
