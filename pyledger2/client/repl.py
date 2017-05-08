#    Pyledger. A simple ledger for smart contracts implemented in Python
#    Copyright (C) 2017  Guillem Borrell Nogueras
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from functools import partial
from pyledger2.client.lib import *


def disconnect(*args, protocol=None):
    protocol.sendClose(code=1000, reason='Client manual disconnection')
    return False, 'Successfully closed, you can kill this with Ctrl-C'


def contracts(*args, protocol=None):
    return True, contracts_request()


instructions = {
    'disconnect': disconnect,
    'contracts': contracts
}

command_help = {
    'disconnect': """
This is the help of disconnect
    """,
    'contracts': """
This is the help of contracts
    """,
    'api': """
This is the help of api
    """,
    'call': """
This is the help of call
    """
}

help_str = """
The Pyledger REPL is a console to interact with a Pyledger server.
The list of available commands is the following

 help          Shows this help
 disconnect    Disconnects from the server in a clean way.
 contracts     Lists the available contracts in the server
 api           Shows the api for a particular contract
 call          Calls a method of a contract

This client may have some limitations respect to a custom client.
For instance, the server may push notifications to the clients,
and using the client API, you could define callbacks to those
pushed messages.

Read the full documentation in http://pyledger.readthedocs.io
"""


def general_parser(line, protocol=None, instruction_dict=None, user_instruction_dict=None):
    message = line.decode('utf-8').replace('\r', '').replace('\n', '')
    message_words = message.split()

    if not message:
        return False, ''

    if 'help' in message_words[0].casefold():
        if len(message_words) == 1:
            return False, help_str
        else:
            if message_words[1].casefold() in command_help:
                return  False, command_help[message_words[1].casefold()]
    if message_words[0] not in instruction_dict:
        return False, 'Command could not be parsed'
    else:
        successful, message = instruction_dict[message_words[0]](message_words[1:], protocol=protocol)

    return successful, message

parse = partial(general_parser, instruction_dict=instructions)
