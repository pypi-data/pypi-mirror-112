import json
import requests


NP_BASE_URL = "https://nerdpool-api.acdh-dev.oeaw.ac.at/api/"


class NerdPoolClient():
    """
    Class to interact with nerdpool-api endpoint
    """

    def __init__(self, base_url=NP_BASE_URL):
        self.base_url = base_url
        self.endpoints = self.fetch_endpoints()
        self.data_set_ep = self.endpoints['ner-source']
        self.sample_ep = self.endpoints['ner-sample']
        self.data_sets = self.list_data_set_titles()

    def __str__(self):
        return "Nerdpool API Client"

    def fetch_endpoints(self):
        r = requests.get(self.base_url)
        return r.json()

    def fetch_data_sets(self):
        r = requests.get(self.data_set_ep)
        return r.json()['results']

    def list_data_set_titles(self):
        return [x['title'] for x in self.fetch_data_sets()]

    def sample_to_json(self, sample):

        """
        takes a ner-sample as it comes from nerdpool-api and returns a spacy conform dict
        :param sample: ner-sample as it comes from nerdpool-api

        :returns: a dict like `{"text": "Wien ist groß.", "entities": [0, 3, "LOC"]}
        :rtype: dict
        """

        ner_sample = sample['ner_sample']
        item = {}
        item['text'] = ner_sample['text']
        item['entities'] = ner_sample['entities']
        return item

    def yield_samples(self, url, limit=False):

        """ iterator to yield all ner-samples

        :param url: The url of the data to fetch
        :type dataset_title: str
        :param limit: Bool to flag if only a short sample\
        of samples should be fetched, defaults to `False`
        :type limit: bool

        :return: An iterator yielding abbreviations
        :rtype: iterator
        """
        next = True
        counter = 0
        if limit:
            max_samples = 5
        while next:
            response = requests.get(url)
            print(response.url)
            result = response.json()
            if result.get('next', False):
                url = result.get('next')
            else:
                next = False
            results = result.get('results')
            for x in results:
                counter += 1
                if limit:
                    if counter <= max_samples:
                        next = False
                        yield(x)
                else:
                    yield(x)

    def dump_to_jsonl(self, url, limit=False, file_name="out.jsonl"):

        """
        dumps the data from the given URL to a jsonl file

        :param url: The url of the data to fetch
        :type dataset_title: str
        :param limit: Bool to flag if only a short sample\
        of samples should be fetched, defaults to `False`
        :type limit: bool
        :param file_name: the name of the file to save the dump
        :type file_name: string

        :return: The file name
        :rtype: str
        """
        with open(file_name, "w") as out_file:
            for x in self.yield_samples(url, limit=limit):
                item = self.sample_to_json(x)
                out_file.write(json.dumps(item, ensure_ascii=False))
                out_file.write("\n")
        return file_name
