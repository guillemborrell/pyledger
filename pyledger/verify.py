import argparse
import sys
import hashlib
import base64
import json
import dill


def run():
    parser = argparse.ArgumentParser(description='Pyledger contract '
                                                 'verification')
    parser.add_argument('--data',
                        help='JSON dump to be verified',
                        type=str,
                        required=True)

    args = parser.parse_args()

    with open(args.data) as dump:
        statuses = json.load(dump)

        for i, status in enumerate(statuses[1:]):
            m = hashlib.sha256()
            m.update(base64.b64decode(statuses[i]['hash']))
            m.update(status['when'].encode('utf-8'))
            m.update(base64.b64decode(status['attributes']))

            if m.digest() == base64.b64decode(status['hash']):
                sys.stdout.write('.')
            else:
                sys.stdout.write('\n {}'.format(
                    'Inconsistency {}'.format(
                        status['when']
                    )
                ))

    sys.stdout.write('\n')
    print('DONE')
