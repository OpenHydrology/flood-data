# -*- coding: utf-8 -*-

import nose.tools as nt
import os
from floodestimation import parsers
from floodestimation import entities


DATA_FOLDER = './data'


class TestValidFiles(object):
    def _files_by_ext(self, ext):
        return [f for dp, dn, filenames in os.walk(DATA_FOLDER)
                for f in filenames if os.path.splitext(f)[1].lower() == ext]

    @staticmethod
    def all_unique(x):
        seen = set()
        return not any(i in seen or seen.add(i) for i in x)

    def test_cd3_files(self):
        for cd3_fn in self._files_by_ext('.cd3'):
            yield self.check_cd3_file, cd3_fn

    def check_cd3_file(self, cd3_fn):
        c = parsers.Cd3Parser().parse(os.path.join(DATA_FOLDER, cd3_fn))
        nt.assert_greater(c.id, 2000,
                          msg="Catchment {} does not have a `id`>2000.".format(cd3_fn))
        nt.assert_less(c.id, 1000000,
                       msg="Catchment {} does not have a `id`<1000000.".format(cd3_fn))
        nt.assert_true(isinstance(c.descriptors.centroid_ngr, entities.Point),
                       msg="Catchment {} does not have centroid coordinates.".format(cd3_fn))
        nt.assert_true(c.location is not None and len(c.location) > 3,
                       msg="Catchment {} does not have a valid `location`".format(cd3_fn))
        nt.assert_true(c.watercourse is not None and len(c.location) > 3,
                       msg="Catchment {} does not have a valid `watercourse`".format(cd3_fn))

    def test_cd3_descriptors(self):
        descrs = [
            # param, min, max
            ('centroid_ngr_x', 0.1, 800000),
            ('centroid_ngr_y', 0.1, 1200000),
            ('dtm_area', 0.1, 20000),
            ('bfihost', 0, 1),
            ('saar', 400, 4000),
            ('farl', 0.5, 1),
            ('fpext', 0, 0.5),
            ('sprhost', 1, 70),
            ('urbext2000', 0, 1)
        ]
        for cd3_fn in self._files_by_ext('.cd3'):
            c = parsers.Cd3Parser().parse(os.path.join(DATA_FOLDER, cd3_fn))
            for descr in descrs:
                yield self.check_descriptor_between, c, descr[0], descr[1], descr[2]

    def check_descriptor_between(self, catchment, descr, lower, upper):
        nt.assert_greater_equal(getattr(catchment.descriptors, descr), lower,
                                msg="Catchment {} does not have a `descriptors.`{}>={}"
                                .format(catchment.id, descr, lower))
        nt.assert_less_equal(getattr(catchment.descriptors, descr), upper,
                             msg="Catchment {} does not have a `descriptors.`{}<={}"
                             .format(catchment.id, descr, upper))

    def test_am_files(self):
        for am_fn in self._files_by_ext('.am'):
            yield self.check_am_file, am_fn

    def check_am_file(self, am_fn):
        records = parsers.AmaxParser().parse(os.path.join(DATA_FOLDER, am_fn))
        nt.assert_true(self.all_unique(am.water_year for am in records),
                       msg="Records in {} do not have unique water years.".format(am_fn))
        for i, am in enumerate(records):
            nt.assert_greater(am.water_year, 1800,
                              msg="Record {} in {} does not have a `water_year`>1800.".format(i + 1, am_fn))
            nt.assert_less(am.water_year, 2500,
                           msg="Record {} in {} does not have a `water_year`<2500.".format(i + 1, am_fn))
            nt.assert_greater(am.flow, 0,
                              msg="Record {} in {} does not have a `flow`>0.".format(i + 1, am_fn))
            nt.assert_less(am.flow, 10000,
                           msg="Record {} in {} does not have a `flow`<1000.".format(i + 1, am_fn))

    def test_am_foreach_cd3(self):
        for cd3_fn in self._files_by_ext('.cd3'):
            yield self.check_am_for_cd3, cd3_fn

    def check_am_for_cd3(self, cd3_fn):
        cd3_fp = os.path.join(DATA_FOLDER, cd3_fn)
        nt.assert_true(os.path.isfile(os.path.splitext(cd3_fp)[0] + '.am') or
                       os.path.isfile(os.path.splitext(cd3_fp)[0] + '.AM'),
                       msg="Catchment {} does not have a corresponding .am file.".format(cd3_fn))
