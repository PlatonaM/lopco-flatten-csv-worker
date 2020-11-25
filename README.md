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
            "time_format": null
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
