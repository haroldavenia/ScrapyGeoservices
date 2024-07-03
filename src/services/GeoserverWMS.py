import asyncio
import json
from owslib.wfs import WebFeatureService
from src.utils.Utils import read_previous_json, read_features_from_json, compare_features


class GeoserverWMS:

    def __init__(self, layer_url, attr_id, __max_record):
        self.__features = None
        self.__query_result = None
        self.__layer_url = layer_url
        self.__max_record_count = 1000 if not __max_record else __max_record
        self.__attr_id = attr_id

    async def query_layer(self, type_name, bbox=None):
        self.__features = []
        start_index = 0
        wfs = WebFeatureService(self.__layer_url, version='2.0.0')

        while True:
            response = await asyncio.to_thread(
                wfs.getfeature,
                typename=type_name,
                bbox=bbox,
                outputFormat='application/json',
                maxfeatures=self.__max_record_count,
                startindex=start_index
            )

            result = json.loads(response.read().decode('utf-8'))
            features = result['features']

            if not features:
                break

            self.__features.extend(features)
            start_index += self.__max_record_count

            if self.__query_result is None:
                self.__query_result = result
            else:
                self.__query_result['features'].extend(result['features'])

    def get_features_updates(self, name_file):
        previous_file_path = read_previous_json(name_file)
        if previous_file_path:
            df_old = read_features_from_json(previous_file_path)
            return compare_features(df_old, self.get_feature_layer_df(), self.__attr_id)
        return None

    @property
    def features(self):
        return self.__features

    @property
    def id(self):
        return self.__attr_id

    @property
    def to_json(self):
        if self.__query_result is not None:
            try:
                return json.dumps(self.__query_result)
            except TypeError as e:
                raise ValueError("Failed to convert query result to JSON.") from e
        else:
            raise ValueError("Query result has not data to save.")
