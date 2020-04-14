#!/usr/bin/python3

import requests
import hashlib
import json as JSON

TOKEN = 'a7529e4702fb24fd168716d6c58c7aea6ac62a2e'
URL = 'https://api.codenation.dev/v1/challenge/dev-ps/generate-data?token='
URL_ANSWER = '''
https://api.codenation.dev/v1/challenge/dev-ps/submit-solution?token=
'''
ALPHABET = 'abcdefghijklmnopqrstuvwxyz'


class Desafio:

    def __init__(self, json):
        self.numero_casas = json['numero_casas']
        self.token = json['token']
        self.cifrado = json['cifrado']
        self.decifrado = json['decifrado']
        self.resumo_criptografico = json['resumo_criptografico']

    def answer(self):
        self.decifrado = self.caesars_cypher(
            self.cifrado, self.numero_casas, True)
        self.resumo_criptografico =\
            hashlib.sha1(self.decifrado.encode('utf-8')).hexdigest()
        try:
            f = open('answer.json', 'w')
            print(str(desafio), file=f)
        finally:
            f.close()

    def shift_alphabet(self, shift):
        shifted = ALPHABET[shift:]+ALPHABET[:shift]
        return shifted

    def caesars_cypher(self, text, shift, decode):
        shifted = self.shift_alphabet(shift) if decode\
            else self.shift_alphabet(-shift)
        result = ''
        for c in text:
            if c not in shifted:
                result += c
            else:
                result += ALPHABET[shifted.index(c)]
        return result

    def __str__(self):
        return JSON.dumps(self.__dict__)


def request_challenge():
    resp = requests.get(URL+TOKEN)
    desafio = Desafio(resp.json())
    return desafio


def post_challenge(desafio):
    url = URL_ANSWER+TOKEN
    # url = 'https://httpbin.org/post' # use to test post method
    resp = requests.post(
        url, files={'file': ('answer.json', str(desafio).encode())})
    if resp.status_code == 200:
        print('success sending. response = {}'.format(resp.content))
    else:
        print('error sending. status = {}, response = {}'
              .format(resp.status_code, resp.content))


if __name__ == "__main__":
    desafio = request_challenge()
    desafio.answer()
    post_challenge(desafio)
