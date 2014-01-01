#
# -*- coding: utf-8 -*-
#
# This file is part of reclass (http://github.com/madduck/reclass)
#
# Copyright © 2007–14 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#
from reclass.output import OutputterBase
import yaml

class Outputter(OutputterBase):

    def dump(self, data, pretty_print=False):
        return yaml.dump(data, default_flow_style=not pretty_print)
