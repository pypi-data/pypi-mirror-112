#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import flask
import os

RESPONSE_CODE = 200
RESPONSE_MESSAGE = 'Hi!\n'

app = flask.Flask(__name__)

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS'])
def hello(path):
    return RESPONSE_MESSAGE, RESPONSE_CODE

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--bind-address',
                        help='Address to bind the server to',
                        dest='bind', default='127.0.0.1')
    parser.add_argument('-f', '--response-file', default=None,
                        help='A file containing a custom response message')
    parser.add_argument('-p', '--port', dest='port', default=4000, type=int,
                        help='The port to listen on')
    parser.add_argument('-r', '--response_code', dest='code', default=200, type=int,
                        help='The response code to send back to requests')
    return parser.parse_args()

def get_env():
    return {
        'BIND_ADDR': os.environ.get('HIAPI_BIND_ADDR'),
        'RESPONSE_FILE': os.environ.get('HIAPI_RESPONSE_FILE'),
        'PORT': os.environ.get('HIAPI_PORT'),
        'RESPONSE_CODE': os.environ.get('HIAPI_RESPONSE_CODE')
    }

def main():
    global RESPONSE_CODE
    global RESPONSE_MESSAGE
    opts = parse_args()

    # Override opts with values from the environment
    env = get_env()
    opts.bind = env['BIND_ADDR'] if env['BIND_ADDR'] else opts.bind
    opts.response_file = env['RESPONSE_FILE'] if env['RESPONSE_FILE'] else opts.response_file
    opts.port = env['PORT'] if env['PORT'] else opts.port
    opts.code = env['RESPONSE_CODE'] if env['RESPONSE_CODE'] else opts.code

    RESPONSE_CODE = opts.code

    if opts.response_file:
        try:
            with open(opts.response_file, 'r') as fh:
                RESPONSE_MESSAGE = fh.read()
        except IOError:
            print('Error: Could not read config file {}'.format(opts.config))

    app.run(host=opts.bind, port=opts.port)

if __name__ == "__main__":
    main()
