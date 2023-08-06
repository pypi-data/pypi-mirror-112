# !/usr/bin/env python
# coding: utf-8
import os

from googlesheettranslate.main import GoogleTranslationSheet

ROOT = os.path.join(os.path.dirname(__file__))
GOOGLETRANS = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRHwRalwUDWbaIH2gU66lYnhf-Y0g7hxQxilnjTYnSkbVMAQNr6_pB_rwVrZUGX4huxM525w1U6JbA-/pubhtml?gid=863127413&single=true"
builder = GoogleTranslationSheet().EnabledProxy().builderOutputTarget(ROOT).builderFromGoogleSheet(GOOGLETRANS)
# builder = GoogleTranslationSheet().builderOutputTarget("${localization}").builderFromCSV("${TRANSLATION_F}")
builder.GetReader().overrideFileFormat("_{}.json", True)
builder.run("CN")
builder.run("EN")
builder.run("ZH")
builder.run("JP")
builder.run("TH")
builder.run("IN")
builder.run("KR")
builder.run("RU")
builder.run("AR")
builder.run("DE")
builder.run("ES")
builder.run("FR")
builder.run("IT")
