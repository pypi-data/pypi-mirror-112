# -*- coding: utf-8 -*-
import ipaddress

import requests


class Ipverse:
    """
        A class to represent a IPBlocks.
        ...

        Attributes
        ----------
        country : str
            country abbreviation
        _url : str
            site url

        Methods
        -------
        get_all_ranger_by_country():
            returns the country IP block list
        """

    def __init__(self):
        """
        _url : str
            site url
        """
        self._url = 'http://ipverse.net/ipblocks/data/countries/'

    def get_all_ranger_by_country(self, country):
        """
        returns the country IP block list
        :return: list
        """
        r = requests.get(self._url + country.lower() + '.zone')
        return [
            ipaddress.ip_network(cidr, False)
            for cidr in r.text.splitlines()
            if not cidr.startswith('#')
        ]

    @staticmethod
    def get_range_ip_by_mask(range):
        return [ip for ip in ipaddress.IPv4Network(range)]

    def find_ip_in_date(self):
        """
        criar uma função que leia um dado dado bruto e procure por ip, apos procurar o ip
        1-indentificar cidade, estado, pais, bloco de ip
        2-verificar a integridade do ip
        3-categorizar as blackslist do ip
        4-saida json
        :return:
        """
