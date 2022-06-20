#!/bin/bash

cd /home/carlos/gits/my-blog-analyzer
PATH=/usr/local/bin:$PATH
pipenv run python log_analyzer.py

