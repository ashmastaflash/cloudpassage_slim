import imp
import os
import sys


module_name = 'cloudpassage_slim'
here_dir = os.path.dirname(os.path.abspath(__file__))
module_path = os.path.join(here_dir, '../../')
sys.path.append(module_path)
fp, pathname, description = imp.find_module(module_name)
cloudpassage_slim = imp.load_module(module_name, fp, pathname, description)


class TestIntegrationTimeSeries(object):
    def get_halo_session(self):
        halo_key = os.getenv("HALO_API_KEY")
        halo_secret = os.getenv("HALO_API_SECRET")
        if None not in [halo_key, halo_secret]:
            session = cloudpassage_slim.HaloSession(halo_key, halo_secret)
        else:
            print("No API authentication env vars set!")
            print("You must set HALO_API_KEY, HALO_API_SECRET to test this!")
            raise ValueError
        return session

    def test_time_series_iter_events_5_pages(self):
        session = self.get_halo_session()
        start_time = "2017-10-01"
        start_url = "/v1/events"
        item_key = "events"
        event_streamer = cloudpassage_slim.TimeSeries(session, start_time,
                                                      start_url, item_key)
        event_counter = 0
        for event in event_streamer:
            print event["message"]
            assert "id" in event
            event_counter += 1
            if event_counter > 600:
                break
