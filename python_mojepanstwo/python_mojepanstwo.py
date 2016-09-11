import requests

from .utils import urlencode_php
from .exceptions import RequestException, NotFoundException


class mojepanstwo(object):
    API_ENDPOINT = "https://api-v3.mojepanstwo.pl/"

    DATASET_ENUM = [
        "bdl_wskazniki",
        "bdl_wskazniki_grupy",
        "bdl_wskazniki_kategorie",
        "budzet_wydatki_czesci",
        "budzet_wydatki_dzialy",
        "budzet_wydatki_rozdzialy",
        "coe_sittings",
        "crawler_pages",
        "crawler_sites",
        "dotacje_ue",
        "dzialania",
        "dzielnice",
        "faktury",
        "gminy",
        "gminy_okregi_wyborcze",
        "handel_zagraniczny_towary",
        "instytucje",
        "kody_pocztowe",
        "kody_pocztowe_ulice",
        "kolej_linie",
        "kolej_stacje",
        "krakow_darczyncy",
        "krakow_dzielnice_rady_posiedzenia",
        "krakow_dzielnice_uchwaly",
        "krakow_glosowania",
        "krakow_glosowania_glosy",
        "krakow_jednostki",
        "krakow_komisje",
        "krakow_komisje_posiedzenia",
        "krakow_komisje_posiedzenia_punkty",
        "krakow_oswiadczenia",
        "krakow_pomoc_publiczna",
        "krakow_posiedzenia",
        "krakow_posiedzenia_punkty",
        "krakow_rada_uchwaly",
        "krakow_radni_dzielnic_glosy",
        "krakow_umowy",
        "krakow_urzednicy",
        "krakow_zamowienia_publiczne",
        "krakow_zarzadzenia",
        "krs_osoby",
        "krs_podmioty",
        "krs_podmioty_zmiany",
        "miejscowosci",
        "msig",
        "msig_dzialy",
        "msig_zmiany",
        "nik_raporty",
        "nik_raporty_dokumenty",
        "panstwa",
        "patenty",
        "poslowie",
        "poslowie_biura",
        "poslowie_biura_wydatki",
        "poslowie_glosy",
        "poslowie_oswiadczenia_majatkowe",
        "poslowie_rejestr_korzysci",
        "poslowie_wspolpracownicy",
        "poslowie_wyjazdy",
        "poslowie_wyjazdy_wydarzenia",
        "powiaty",
        "prawo",
        "prawo_hasla",
        "prawo_lokalne",
        "prawo_powiazane",
        "prawo_projekty",
        "prawo_urzedowe",
        "prawo_wojewodztwa",
        "radni_dzielnic",
        "radni_gmin",
        "radni_gmin_oswiadczenia_majatkowe",
        "rady_druki",
        "rady_druki_dokumenty",
        "rady_gmin",
        "rady_gmin_debaty",
        "rady_gmin_interpelacje",
        "rady_gmin_wystapienia",
        "rady_posiedzenia",
        "rcl_etapy",
        "sa_orzeczenia",
        "sa_sedziowie",
        "sejm_debaty",
        "sejm_dezyderaty",
        "sejm_druki",
        "sejm_glosowania",
        "sejm_interpelacje",
        "sejm_interpelacje_pisma",
        "sejm_kluby",
        "sejm_komisje",
        "sejm_komisje_opinie",
        "sejm_komisje_uchwaly",
        "sejm_komunikaty",
        "sejm_posiedzenia",
        "sejm_posiedzenia_punkty",
        "sejm_wystapienia",
        "senat_druki",
        "senat_glosowania",
        "senat_glosowania_glosy",
        "senat_kluby",
        "senat_posiedzenia",
        "senat_rejestr_korzysci",
        "senat_stenogramy",
        "senatorowie",
        "senatorowie_oswiadczenia_majatkowe",
        "senatorowie_pracownicy",
        "sn_orzeczenia",
        "sn_sedziowie",
        "sp_orzeczenia",
        "sp_tezy",
        "tematy",
        "twitter",
        "twitter_accounts",
        "twitter_tags",
        "umowy",
        "urzednicy",
        "urzednicy_rejestr_korzysci",
        "urzedy_gmin",
        "wojewodztwa",
        "wybory_darczyncy",
        "zamowienia_publiczne",
        "zamowienia_publiczne_dokumenty",
        "zamowienia_publiczne_wykonawcy",
        "zamowienia_publiczne_zamawiajacy",
        "zbiory"
    ]

    def __init__(self, session=None):
        self.session = session or requests.Session()

    def get_url(self, url):
        resp = self.session.get(url)
        if resp.status_code == 404:
            raise NotFoundException("Not found URL '{url}'".format(
                                    url=resp.json()['url']))
        if resp.status_code != 200:
            raise RequestException("Unknown requests error: {name}".format(
                                   name=resp.json()['name']))
        return resp.json()

    def query(self, uri, params=None):
        params = params or {}
        url = self.API_ENDPOINT + uri + "?" + urlencode_php(params)
        return self.get_url(url)

    def _list(self, uri, conditions=None, page=0, params=None, limit=50):
        params = params or {}
        conditions = conditions or {}

        queryset = params.copy()
        queryset['page'] = page
        queryset['limit'] = limit
        queryset['conditions'] = conditions
        return DataobjectList(json=self.query(uri=uri, params=queryset),
                              client=self)

    def _detail(self, uri, layers=None, params=None):
        layers = layers or []
        params = params or {}

        queryset = params.copy()
        queryset['layers'] = layers

        return Dataobject(json=self.query(uri=uri, params=queryset),
                          client=self)

    def __dir__(self):
        return [x + "_list" for x in mojepanstwo.DATASET_ENUM.keys()] + \
               [x + "_detail" for x in mojepanstwo.DATASET_ENUM.keys()]

    def __getattr__(self, name):

        if name.endswith('_list'):
            uri = "dane/%s/" % (name.replace('_list', ''), )

            def query_list(conditions=None, page=0, **kwargs):
                return self._list(uri=uri,
                                  page=page,
                                  conditions=conditions,
                                  **kwargs)
            return query_list
        if name.endswith('_detail'):
            uri = "dane/%s/%%s" % (name.replace('_detail', ''), )

            def query_detail(pk, layers=None, **kwargs):
                return self._detail(uri="dane/twitter_accounts/%s" % (pk, ),
                                    layers=layers,
                                    **kwargs)
            return query_detail
        raise AttributeError

    def refresh_dataset(self):
        response = self.query('swagger.json')
        self.DATASET_ENUM = response['parameters']['dataset']['enum']


class Dataobject(object):
    @property
    def is_full(self):
        return 'layers' in self.data

    def __init__(self, json, client):
        self.json = json
        self.client = client

    def get_full(self):
        if self.is_full:
            return self
        return Dataobject(self.client.get_url(self.json['url']))

    def __getattr__(self, name):
        try:
            return self.json['data'][name.replace('__', '.')]
        except KeyError:
            return AttributeError

    def __dir__(self):
        return [x.replace('.', '__') for x in self.json['data'].keys()]

    def __repr__(self):
        if 'slug' in self.json:
            return "%s [id=%s, slug=%s]" % (self.json['dataset'],
                                            self.json['id'],
                                            self.json['slug'])
        return "%s [id=%s]" % (self.json['dataset'],
                               self.json['id'])


class DataobjectList(object):
    def __init__(self, json, client):
        self.json = json
        self.client = client

    @property
    def has_prev(self):
        return 'prev' in self.json['Links']

    @property
    def has_next(self):
        return 'next' in self.json['Links']

    def __getattr__(self, name):
        try:
            return self.json[name]
        except KeyError:
            return super(DataobjectList, (self).__getattr__(name))

    def __dir__(self):
        return super(DataobjectList, (self)).__dir__() + self.json.keys()

    def __len__(self):
        return len(self.json['Dataobject'])

    def __getitem__(self, key):
        return Dataobject(json=self.json['Dataobject'][key],
                          client=self.client)

    def __iter__(self):
        return (Dataobject(json=x,
                           client=self.client)
                for x in self.json['Dataobject'])

    def iter_full(self):
        def inter(start_page):
            page = start_page
            while True:
                for obj in page:
                    yield obj
                if page.has_next:
                    page = page.next_page()
                else:
                    break
        return inter(self)

    def _prev_or_next(self, prev_or_next):
        return DataobjectList(json=self.client.get_url(url=self.json['Links'][prev_or_next]),
                              client=self.client)

    def prev_page(self):
        return self._prev_or_next('prev')

    def next_page(self):
        return self._prev_or_next('next')
