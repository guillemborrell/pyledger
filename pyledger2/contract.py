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

from .status import SimpleStatus
import abc


class BaseContract(abc.ABC):
    @abc.abstractproperty
    def status(self):
        pass


class SimpleContract(BaseContract):
    """
    Contract that uses SimpleStatus for serialization.

    The goal of this class is to make a contact feel just like a Python class.
    """
    status_class = SimpleStatus

    def __init__(self, **kwargs):
        self.keys = (k for k in kwargs)
        for k, v in kwargs.items():
            setattr(self, k, v)

    @property
    def status(self):
        return self.status_class(**{k: getattr(self, k) for k in self.keys})


BaseContract.register(SimpleContract)
