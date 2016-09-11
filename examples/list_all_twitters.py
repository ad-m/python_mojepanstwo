#!/usr/bin/env python
# coding: utf-8
# pip install python-mojepanstwo requests requests_cache
from __future__ import print_function
import sys
from requests import Session
import argparse
from python_mojepanstwo import mojepanstwo
from python_mojepanstwo.exceptions import NotFoundException

try:
    from requests_cache import CachedSession
except ImportError:
    print("Cache is unsupported", file=sys.stderr)
    from requests import Session as CachedSession


class CSVView(object):
    def __init__(self, file):
        self.file = file

    def header(self):
        print(";".join(["No", "posel_id", "nazwa", "klub", "ostatnia_kadencja", "twitter"]),
              file=file)

    def _content_row(self, i, posel, twitter):
        return ";".join([str(i),
                         posel.poslowie__id,
                         posel.poslowie__nazwa,
                         posel.sejm_kluby__nazwa,
                         posel.poslowie__kadencja_ostatnia,
                         twitter.twitter_accounts__twitter_name]).encode('utf-8')

    def _content_err(self, i, posel):
        return ";".join([str(i),
                         posel.poslowie__id,
                         posel.poslowie__nazwa,
                         posel.sejm_kluby__nazwa,
                         posel.poslowie__kadencja_ostatnia,
                         "FAKE"]).encode('utf-8')

    def _content_no(self, i, posel):
        return ";".join([str(i),
                         posel.poslowie__id,
                         posel.poslowie__nazwa,
                         posel.sejm_kluby__nazwa,
                         posel.poslowie__kadencja_ostatnia,
                         "No Twitter"]).encode('utf-8')

    def content_row(self, i, posel, twitter):
        print(self._content_row(i, posel, twitter), file=self.file)

    def content_err(self, i, posel):
        print(self._content_err(i, posel), file=self.file)

    def content_no(self, i, posel):
        print(self._content_no(i, posel), file=self.file)

    def footer(self):
        pass


def business_logic(session, view):
    client = mojepanstwo(session)
    page = client.poslowie_list(page=0)
    for i, posel in enumerate(page.iter_full()):
        if posel.poslowie__twitter_account_id != '0':
            try:
                twitter = client.twitter_accounts_detail(pk=posel.poslowie__twitter_account_id)
                view.content_row(i, posel, twitter)
            except NotFoundException:
                view.content_err(i, posel)
        else:
            view.content_no(i, posel)
    view.footer()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'),
                        default=sys.stdout, help="Output file (default: stdout)")
    parser.add_argument('--no-cache', action='store_true',
                        help="Disable requests cache (default enabled)")
    args = parser.parse_args()

    session = Session() if args.no_cache else CachedSession()
    view = CSVView(args.outfile)

    business_logic(session, view)


if __name__ == "__main__":
    main()
