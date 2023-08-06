# !/usr/bin/env python
# coding: utf-8

from googlesheettranslate.main import GoogleTranslationSheet


builder = GoogleTranslationSheet().EnabledProxy().builderOutputTarget("${localization}").builderFromGoogleSheet("${GOOGLETRANS}")
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
