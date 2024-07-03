import asyncio
import json
import pandas as pd
from arcgis.features import FeatureLayer
from arcgis.geometry import filters
from src.utils.Utils import read_previous_json, read_features_from_json, compare_features


class EsriRestService:

    def __init__(self, layer_url, attr_id):
        self.__features = None
        self.__query_result = None
        self.__attr_id = attr_id
        self.__layer_url = "https://services.arcgis.com/example/arcgis/rest/services/LayerName/FeatureServer/0"
        self.__feature_layer = FeatureLayer(layer_url)
        self.__max_record_count = 1000

    async def query_layer(self, where="1=1", out_fields="*", return_geometry=True, geometry=None):
        self.__features = []
        object_ids_result = self.__feature_layer.query(
            where=where,
            return_ids_only=True,
            geometry_filter=filters.intersects(geometry) if geometry else geometry
        )
        object_ids = object_ids_result.get('objectIds', None)
        if object_ids is None:
            return

        tasks = []
        for start in range(0, len(object_ids), self.__max_record_count):
            end = start + self.__max_record_count
            oid_subset = object_ids[start:end]
            task = asyncio.create_task(self.query_subset(oid_subset, out_fields, return_geometry))
            tasks.append(task)

        await asyncio.gather(*tasks)

    async def query_subset(self, oid_subset, out_fields, return_geometry):
        result = self.__feature_layer.query(
            object_ids=','.join(map(str, oid_subset)),
            out_fields=out_fields,
            return_geometry=return_geometry
        )

        if self.__query_result is None:
            self.__query_result = result
            self.__features = result.features
        else:
            self.__query_result.features.extend(result.features)
            self.__features.extend(result.features)

    def get_feature_layer_df(self):
        data = json.loads(self.__query_result.to_json)
        return pd.json_normalize(data.get('features', None))

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
        return self.__query_result.to_json
