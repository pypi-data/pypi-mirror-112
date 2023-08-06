#!/bin/sh


LOCALMAIN=main.py
CREDIT=$PWD/private/credit.json
SHEET_ID="1hVeMszzTnGbvA-xCfYjdknOb0AS3eD54ISHfnchz9xU"
ID="2PACX-1vQ-pT3N4TN-Od5EI2XhywuAo79dLmZpF_8bWqBg2t-8XmiBQv1w8h7gG7PtKctXY3BUV2fo7Ohg484W"
python3 $LOCALMAIN $CREDIT $SHEET_ID "android"
python3 $LOCALMAIN $CREDIT $SHEET_ID "ios"
python3 $LOCALMAIN $CREDIT $SHEET_ID "ios-swift"