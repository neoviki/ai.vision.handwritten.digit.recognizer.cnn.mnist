#!/bin/bash
if [[ ! -d model ]]; then
    mkdir model
fi
cd src
python3 HandWriten_Digit_Classifier_Main.py
