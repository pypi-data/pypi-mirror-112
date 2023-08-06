# Copyright (c) 2021 Grumpy Cat Software S.L.
#
# This Source Code is licensed under the MIT 2.0 license.
# the terms can be found in LICENSE.md at the root of
# this project, or at http://mozilla.org/MPL/2.0/.

import unittest

from shapelets import init_session
from shapelets.dsl import DataApp


class DataAppServiceTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls._client = init_session("admin", "admin", "https://127.0.0.1", 8443)

    def test_remove_me(self):
        daniel = DataApp("Daniel V2.0", "Indescribable")

        # number = daniel.number(default_value=3.14)
        # daniel.place(number)
        client = DataAppServiceTest._client
        app = client.register_data_app(daniel)
        print(app)
