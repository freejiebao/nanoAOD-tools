#!/bin/bash
# A simple script
python run_helper.py -y 2016 -x
echo "=============================================================================="
echo "----------------------------finish adding xsweight----------------------------"
echo "=============================================================================="
python run_helper.py -y 2016 -s -post skim_l2
python run_helper.py -y 2016 -s -post vbs_l2 -pre skim_l2
python run_helper.py -y 2016 -s -post lowmjj_l2 -pre skim_l2
echo "=============================================================================="
echo "--------------------------finish two leptons regions--------------------------"
echo "=============================================================================="
python run_helper.py -y 2016 -s -post skim_l3
python run_helper.py -y 2016 -s -post vbs_l3 -pre skim_l3
echo "=============================================================================="
echo "-------------------------finish three leptons regions-------------------------"
echo "=============================================================================="
python run_helper.py -y 2016 -s -post skim_l4
python run_helper.py -y 2016 -s -post vbs_l4 -pre skim_l4
echo "=============================================================================="
echo "--------------------------finish four leptons regions-------------------------"
echo "=============================================================================="
python run_helper.py -y 2016 -e -post vbs_l2
python run_helper.py -y 2016 -e -post lowmjj_l2
python run_helper.py -y 2016 -e -post vbs_l3
python run_helper.py -y 2016 -e -post vbs_l4
echo "=============================================================================="
echo "----------------------finish adding lepton scale factor-----------------------"
echo "=============================================================================="
