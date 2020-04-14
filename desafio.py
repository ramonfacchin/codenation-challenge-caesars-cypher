#!/usr/bin/python3

import hashlib
import json as JSON
from requests import Session
from requests import Request

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


def request_challenge(session):
    req = Request('GET',
                  URL+TOKEN,
                  headers={'Content-Type': 'application/json'}).prepare()
    resp = session.send(req)
    desafio = Desafio(resp.json())
    return desafio


def post_challenge(session):
    # resp = requests.post(URL_ANSWER+TOKEN,
    #                     files={'answer': str(desafio).encode('utf-8')})
    with open('answer.json') as entrada:
        req = Request('POST',
                      URL_ANSWER+TOKEN,
                      headers={'Content-Type': 'multipart/form-data'},
                      files={'answer': entrada})
        print(req.headers)
        resp = session.send(req.prepare())
        if resp.status_code == 200:
            print('success sending. response = {}'.format(resp.content))
        else:
            print('error sending. status = {}, response = {}'
                  .format(resp.status_code, resp.content))


if __name__ == "__main__":
    with open('answer.json', 'w') as saida:
        session = Session()
        desafio = request_challenge(session)
        desafio.answer()
        print(desafio, file=saida)
        post_challenge(session)
