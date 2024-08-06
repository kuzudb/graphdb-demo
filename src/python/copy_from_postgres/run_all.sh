#!/bin/bash

source .venv/bin/activate
# Run all the scripts in the correct order
python insert_data_pg.py
python copy_pg_to_kuzu.py
python analyze.py