# !/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

import csv
import os

import requests
from bs4 import BeautifulSoup

from .x import Reader
from .x.Err import WrongReaderType

statement = 'End : {}, IO File {}'

CVS, GOOGLE_SHEET, CSV, EXCEL = range(4)


class GoogleTranslationSheet:
    """
    featured translation service does not need to use creditentials
    """

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:79.0) Gecko/20100101 Firefox/79.0',
        'Accept-Language': 'en-US,en;q=0.5',
        'X-Requested-With': 'XMLHttpRequest'
    }

    proxies = {
        "http": "socks5://127.0.0.1:1086",
        "https": "socks5://127.0.0.1:1086",
    }

    def __init__(self):
        self.exportedSheetUrl = ""
        self.html = ""
        self.tab = ""
        self.engine_name = ""
        self.target_folder = ""
        self.input_filepath = ""
        self.tab_content = dict()
        self.saveToCvs = True
        self._reader_type = 0
        self.reader_debug = False
        self._use_proxies = False
        self._readerEngine = Reader()

    def EnabledProxy(self, replaces: dict = None) -> "GoogleTranslationSheet":
        self._use_proxies = True
        if replaces is not None:
            self.proxies = replaces
        return self

    def builderCvs(self, enabled: bool) -> "GoogleTranslationSheet":
        """
        enable CVS file save to the local path
        :param enabled:
        :return:
        """
        self.saveToCvs = enabled
        return self

    def builderOutputTarget(self, tar: str) -> "GoogleTranslationSheet":
        """
        save files at the specific target folder
        :param tar:
        :return:
        """
        self.target_folder = tar
        return self

    def builderTransformers(self, engine_name: str) -> "GoogleTranslationSheet":
        """
        using the transform engine from the specification tool
        :param engine_name:
        :return:
        """
        self.engine_name = engine_name
        return self

    def builderReaderDebug(self, de: bool) -> "GoogleTranslationSheet":
        """
        given the extra log detail to the reader
        :param de: yes or no
        :return:
        """
        self.reader_debug = de
        return self

    def builderReader(self, module_reader: Reader) -> "GoogleTranslationSheet":
        """
        building reader module by external instance
        :param module_reader:
        :return:
        """
        self._readerEngine = module_reader
        return self

    def builderFromCVS(self, filename: str = "") -> "GoogleTranslationSheet":
        """
        CVS file started
        :param filename:
        :return:
        """
        self.input_filepath = filename
        self._reader_type = CVS
        return self

    def builderFromCSV(self, filename: str = "") -> "GoogleTranslationSheet":
        """
        CVS file started
        :param filename:
        :return:
        """
        self.input_filepath = filename
        self._reader_type = CSV
        return self

    def builderFromExcel(self, filename: str = "") -> "GoogleTranslationSheet":
        """
        CVS file started
        :param filename:
        :return:
        """
        self.input_filepath = filename
        self._reader_type = EXCEL
        return self

    def builderFromGoogleSheet(self, url: str, tabname: str = "") -> "GoogleTranslationSheet":
        """
        this is the required for the basic meta information for loading google sheet
        :param url:
        :param tabname:
        :return:
        """
        self.exportedSheetUrl = url
        self.tab = tabname
        self._reader_type = GOOGLE_SHEET
        return self

    def builderFromGoogleSheetMeta(self, sheetID: str = "", gridID: str = "", tabg: str = "") -> "GoogleTranslationSheet":
        """
        building by the sheet IDs
        :param sheetID:
        :param gridID:
        :param tabg:
        :return:
        """
        self.exportedSheetUrl = f"https://docs.google.com/spreadsheets/d/e/{sheetID}/pubhtml?gid={gridID}&single=true"
        self.tab = tabg
        self._reader_type = GOOGLE_SHEET
        return self

    def GetReader(self) -> Reader:
        """
        make modification setting for the internal Reader instance
        :return:
        """
        return self._readerEngine

    def getFileNameInternal(self, index: int) -> str:
        """
        get the naming for the cvs file
        :param index:
        :return:
        """
        return os.path.join(self.target_folder, f"data{str(index)}.cvs")

    def _run_csv(self, Lang="CN") -> None:
        """
        read the cvs now
        :return:
        """
        if self._reader_type != CSV:
            raise WrongReaderType("You have not set proper csv file path for the translation source.")

        self._readerEngine.newSheet()
        self._readerEngine.setLang(Lang)

        with open(self.input_filepath, newline='') as csvfile:
            line_ex = csv.reader(csvfile, delimiter=',', quotechar='|')
            self.tab_content = [[y for y in row] for row in line_ex]
            self._readerEngine.setDebug(self.reader_debug).setTarget(self.target_folder).useEngine(
                self.engine_name).LoopMatrix(self.tab_content)

    def _run_excel(self, Lang="CN") -> None:
        if self._reader_type != EXCEL:
            raise WrongReaderType("You are not using excel.")
        self._readerEngine.newSheet()
        self._readerEngine.setLang(Lang)
        self._readerEngine.setDebug(self.reader_debug).setTarget(self.target_folder).useEngine(
            self.engine_name).LoopExcel(self.input_filepath)

    def _run_cvs(self, Lang="CN") -> None:
        """
        read the cvs now
        :return:
        """
        if self._reader_type != CVS:
            raise WrongReaderType("You have not set proper cvs file path for the translation source.")

        self._readerEngine.newSheet()
        self._readerEngine.setLang(Lang)

        with open(self.input_filepath, newline='') as csvfile:
            line_ex = csv.reader(csvfile, delimiter=' ', quotechar='|')
            line_lis = list()
            for row in line_ex:
                if len(row) == 0:
                    continue

                blist = row[0].split(",")
                newb = []
                for h in blist:
                    newb.append(self._process_s(h))
                print(newb)

                line_lis.append(newb)

            self.tab_content = line_lis

            # self.tab_content = [map(lambda x: self._process_s, line_lis)]
            self._readerEngine.startRow(0).setDebug(self.reader_debug).setTarget(self.target_folder).useEngine(
                self.engine_name).LoopMatrix(self.tab_content)

    def _process_s(self, string: str) -> str:
        if string.startswith('"'):
            string = string[1:]

        if string.endswith('"'):
            string = string[:-1]
        return string

    def _run_google_url(self, Lang="CN") -> None:
        """
                run up the engine for given parameters
                :param proxies: whether the connection is using VPN or no
                :param Lang: the language column that matched to the sheet
                :return:
                """

        if self._reader_type != GOOGLE_SHEET:
            raise WrongReaderType("You have not set proper google sheet url for the translation source.")
        self._readerEngine.newSheet()
        self._readerEngine.setLang(Lang)
        if self._use_proxies is True:
            self.html = requests.get(self.exportedSheetUrl, headers=self.headers, proxies=self.proxies).text
        else:
            self.html = requests.get(self.exportedSheetUrl, headers=self.headers).text

        soup = BeautifulSoup(self.html, "lxml")
        tables = soup.find_all("table")
        index = 0

        for table in tables:
            output_f = self.getFileNameInternal(index)
            self.tab_content = [[td.text for td in row.find_all("td")] for row in table.find_all("tr")]
            if self.saveToCvs:
                with open(output_f, "w") as f:
                    wr = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
                    wr.writerows(self.tab_content)

            self._readerEngine.setDebug(self.reader_debug).setTarget(self.target_folder).useEngine(
                self.engine_name).LoopTable(self.tab_content)

            index = index + 1

    def run(self, Lang="CN"):
        if self._reader_type == CVS:
            self._run_cvs(Lang)
        elif self._reader_type == CSV:
            self._run_csv(Lang)
        elif self._reader_type == GOOGLE_SHEET:
            self._run_google_url(Lang)
        elif self._reader_type == EXCEL:
            self._run_excel(Lang)
        else:
            raise WrongReaderType("Incomplete source set.")
