import os

from googlesheettranslate.main import GoogleTranslationSheet

ROOT = os.path.join(os.path.dirname(__file__))
builder = GoogleTranslationSheet().builderOutputTarget(ROOT).builderFromExcel("emp-translation.xlsx")
builder.builderTransformers("i18n")
builder.GetReader().overrideFileFormat("__i{}.json", True)
builder.run("EN")
builder.run("ZH")
