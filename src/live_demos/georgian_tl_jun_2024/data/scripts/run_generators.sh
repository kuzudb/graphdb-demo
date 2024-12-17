#!/bin/bash

python clean_data.py
python generate_customers.py
python generate_tasters.py
python generate_follows.py
python generate_lives_in.py
python generate_purchased.py
python generate_tasted.py