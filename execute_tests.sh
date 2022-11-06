#!/bin/sh

python3 -m unittest ./grid/test_grid.py

python3 -m unittest ./db/test_db.py

python3 -m unittest test_app.py
