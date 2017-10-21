import operator
import time


class TimeSeries(object):
    """Wrap time-series object retrieval in a generator"""
    def __init__(self, session, start_time, start_url, params=""):
        self.start_time = start_time
        self.url = start_url
        self.params = params
        self.batch_size = 10
        self.session = session
        self.threads = self.session.threads
        return

    def __iter__(self):
        """Yields one item from a time-series query against Halo. Forever."""
        while True:
            for item in self.get_next_batch():
                yield item

    def get_next_batch(self):
        """Gets the next batch of time-series items from the Halo API"""
        url_list = self.create_url_list()
        pages = self.get_pages(url_list)
        # adjustment_factor = self.get_adjustment_factor(pages, self.page_size)
        # self.adjust_batch_size(adjustment_factor)
        items = self.sorted_items_from_pages(pages, "events", "created_at")
        try:
            if items[0]["id"] == self.last_item_id:
                del items[0]
        except IndexError:  # This happens when the return set is empty...
            time.sleep(3)
            return []
        try:
            last_item_timestamp = items[-1]['created_at']
            last_item_id = items[-1]['id']
        except IndexError:
            time.sleep(3)
            return []
        self.last_item_timestamp = last_item_timestamp
        self.last_item_id = last_item_id
        return items

    @classmethod
    def create_url_batch(cls, path, batch_size, params={}):
        """Create a batch of URLs for pulling time-series objects from Halo.

        Args:
            base_url(str): This is the path of the URL, not including hostname
                or parameters.
            batch_size(int): This is the number of URLs that will be generated.
            params(dict): These are parameters that will be added to each URL.

        Returns:
            list: This returns a list of tuples, where the first item in the
                tuple is the URL path, the second is the params to be appended
                to the URL when retrieved.
        """
        url_list = []
        for page in range(1, batch_size + 1):
            url = None
            params["page"] = page
            url = (path, dict(params))
            url_list.append(url)
        return url_list

    @classmethod
    def sorted_items_from_pages(cls, pages, pagination_key, sort_key):
        items = []
        for page in pages:
            for item in page[pagination_key]:
                items.append(item)
        result = sorted(items, key=operator.itemgetter(sort_key))
        return result
