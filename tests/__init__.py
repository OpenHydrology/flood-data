# -*- coding: utf-8 -*-

import unittest
import os
from floodestimation import parsers
from floodestimation import entities


class TestValidFiles(unittest.TestCase):
    def _files_by_ext(self, ext):
        return [os.path.join(dp, f) for dp, dn, filenames in os.walk('./data')
                for f in filenames if os.path.splitext(f)[1].lower() == ext]

    @staticmethod
    def all_unique(x):
        seen = set()
        return not any(i in seen or seen.add(i) for i in x)

    def test_cd3_files(self):
        for cd3_fp in self._files_by_ext('.cd3'):
            cd3_fn = os.path.basename(cd3_fp)
            c = parsers.Cd3Parser().parse(cd3_fp)
            self.assertTrue(isinstance(c.descriptors.centroid_ngr, entities.Point),
                            msg="Catchment {} does not have centroid coordinates.".format(cd3_fn))
            self.assertGreater(c.descriptors.dtm_area, 0,
                               msg="Catchment {} does not have a `dtm_area`>0.".format(cd3_fn))
            self.assertLess(c.descriptors.dtm_area, 10000,
                            msg="Catchment {} does not have a `dtm_area`<10000.".format(cd3_fn))
            self.assertGreaterEqual(c.descriptors.bfihost, 0,
                                    msg="Catchment {} does not a `bfi_host`>=0.".format(cd3_fn))
            self.assertLessEqual(c.descriptors.bfihost, 1,
                                 msg="Catchment {} does not a `bfi_host`<=1.".format(cd3_fn))
            self.assertGreater(c.descriptors.saar, 250,
                               msg="Catchment {} does not have a `saar`>250.".format(cd3_fn))
            self.assertLess(c.descriptors.saar, 5000,
                            msg="Catchment {} does not have a `saar`<5000.".format(cd3_fn))

    def test_am_files(self):
        for am_fp in self._files_by_ext('.am'):
            am_fn = os.path.basename(am_fp)
            records = parsers.AmaxParser().parse(am_fp)
            self.assertTrue(self.all_unique(am.water_year for am in records),
                            msg="Records in {} do not have unique water years.".format(am_fp))
            for i, am in enumerate(records):
                self.assertGreater(am.water_year, 1800,
                                   msg="Record {} in {} does not have a `water_year`>1800.".format(i + 1, am_fn))
                self.assertLess(am.water_year, 2500,
                                msg="Record {} in {} does not have a `water_year`<2500.".format(i + 1, am_fn))
                self.assertGreater(am.flow, 0,
                                   msg="Record {} in {} does not have a `flow`>0.".format(i + 1, am_fn))
                self.assertLess(am.flow, 10000,
                                msg="Record {} in {} does not have a `flow`<1000.".format(i + 1, am_fn))

    def test_am_foreach_cd3(self):
        for cd3_fp in self._files_by_ext('.cd3'):
            cd3_fn = os.path.basename(cd3_fp)
            self.assertTrue(os.path.isfile(os.path.splitext(cd3_fp)[0] + '.am') or
                            os.path.isfile(os.path.splitext(cd3_fp)[0] + '.AM'),
                            msg="Catchment {} does not have a corresponding .am file.".format(cd3_fn))
