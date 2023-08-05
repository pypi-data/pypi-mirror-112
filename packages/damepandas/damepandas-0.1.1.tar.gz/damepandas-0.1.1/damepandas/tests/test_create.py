#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2019  David Arroyo Menéndez

# Author: David Arroyo Menéndez <davidam@gnu.org>
# Maintainer: David Arroyo Menéndez <davidam@gnu.org>

# This file is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.

# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with damepandas; see the file LICENSE.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA 02110-1301 USA,

from unittest import TestCase

import numpy as np
import pandas as pd


class TestCreate(TestCase):

    def test_series(self):
        s1 = pd.Series(['a', 'b'])
        self.assertEqual(len(s1), 2)
        self.assertEqual('0    a\n1    b\ndtype: object', repr(s1))

    def test_dataframe(self):
        df2 = pd.DataFrame([['c', 3], ['d', 4]], columns=['letter', 'number'])
        self.assertTrue(len(df2) > 0)
        string1 = '  letter  number\n0      c       3\n1      d       4'
        self.assertEqual(string1, repr(df2))

    def test_dataframe_from_dict(self):
        pdffd = pd.DataFrame.from_dict(dict([('A', [1, 2, 3]),
                                             ('B', [4, 5, 6])]))
        self.assertEqual(len(pdffd), 3)
        self.assertEqual('   A  B\n0  1  4\n1  2  5\n2  3  6', repr(pdffd))

    def test_range(self):
        dates = pd.date_range('20130101', periods=6)
        string1 = "DatetimeIndex(['2013-01-01', "
        string1 = string1 + "'2013-01-02', '2013-01-03', '2013-01-04',\n"
        string1 = string1 + "               '2013-01-05', '2013-01-06'],\n"
        string1 = string1 + "              dtype='datetime64[ns]', freq='D')"
        self.assertEqual(string1, repr(dates))
        self.assertTrue(len(dates) > 0)

    def test_fill_random(self):
        dates = pd.date_range('20130101', periods=6)
        df = pd.DataFrame(np.random.randn(6, 4),
                          index=dates,
                          columns=list('ABCD'))
        self.assertTrue(len(df) > 0)
