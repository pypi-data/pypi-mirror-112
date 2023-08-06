"""LICENSE
Copyright 2020 Hermann Krumrey <hermann@krumreyh.com>

This file is part of jerrycan.

jerrycan is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

jerrycan is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with jerrycan.  If not, see <http://www.gnu.org/licenses/>.
LICENSE"""

from jerrycan.base import db
from jerrycan.db.ModelMixin import ModelMixin


class IDModelMixin(ModelMixin):
    """
    A mixin class that specifies a couple of methods all database
    models should implement.
    Includes an automatically incrementing ID.
    """

    id = db.Column(
        db.Integer, primary_key=True, nullable=False, autoincrement=True
    )
    """
    The ID is the primary key of the table and increments automatically
    """

    def __hash__(self) -> int:
        """
        Creates a hash so that the model objects can be used as keys
        :return: None
        """
        return hash(self.id)
