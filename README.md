# cloudpassage_slim
## A pure-python zero-dependency API abstraction for CloudPassage Halo

Prototype.

### Usage

1. Download and expand the `cloudpassage_slim.tar.gz` file in the target environment.
1. Start the Python interpreter
1. To run an event stream to stdout (Completing the HALO_API_KEY, HALO_API_SECRET, and ISO8601_TIME_STAMP variables):

```
halo_key = "HALO_API_KEY"
halo_secret = "HALO_API_SECRET"
import cloudpassage_slim
session = cloudpassage_slim.HaloSession(halo_key, halo_secret)
start_time = "ISO8601_TIME_STAMP"
start_url = "/v1/events"
item_key = "events"
event_streamer = cloudpassage_slim.TimeSeries(session, start_time, start_url, item_key)
for event in event_streamer:
    print("id: %s -- Timestamp: %s -- Type: %s" % (event["id"], event["created_at"], event["type"]))
```

ctrl-c to exit.
