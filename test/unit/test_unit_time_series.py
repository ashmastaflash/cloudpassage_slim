import imp
import os
import sys


module_name = 'cloudpassage_slim'
here_dir = os.path.dirname(os.path.abspath(__file__))
module_path = os.path.join(here_dir, '../../')
sys.path.append(module_path)
fp, pathname, description = imp.find_module(module_name)
cloudpassage_slim = imp.load_module(module_name, fp, pathname, description)


class TestUnitTimeSeries(object):
    def test_unit_time_series_build_url_list(self):
        path = "/v1/whatever"
        params = {"server": "heyhowdy"}
        count = 0
        for item in cloudpassage_slim.TimeSeries.create_url_batch(path, 5,
                                                                  params):
            count += 1
            assert item[0] == path
            assert item[1]["server"] == "heyhowdy"
            assert item[1]["page"] == count
        assert count == 5

    def test_unit_time_series_sorted_items_from_pages(self):
        page1 = {"whatevers": [
                    {"item_number": 1,
                     "nonsort": "somesuch"},
                    {"item_number": 4,
                     "nonsort": "somesuch"}]}
        page2 = {"whatevers": [
                    {"item_number": 2,
                     "nonsort": "somesuch"},
                    {"item_number": 3,
                     "nonsort": "somesuch"}]}
        pages = [page1, page2]
        s = cloudpassage_slim.TimeSeries.sorted_items_from_pages(pages,
                                                                 "whatevers",
                                                                 "item_number")
        count = 0
        for item in s:
            count += 1
            assert item["item_number"] == count
        assert count == 4
