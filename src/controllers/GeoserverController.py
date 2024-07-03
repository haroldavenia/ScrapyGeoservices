from src.services.GeoserverWMS import GeoserverWMS
from src.utils.Utils import read_previous_json, generate_report, save_previous_json_backup, write_JSON_file


class GeoserverController:

    @staticmethod
    async def query_layer(kwargs):
        service = GeoserverWMS(kwargs.get('layer_url', None), kwargs.get('attr_id', None), kwargs.get('max_record', 1000))
        await service.query_layer(type_name=kwargs.get('type_name', None), bbox=kwargs.get('bbox', None))
        name_file = kwargs.get('name_file', 'wms_geoserver_layer')
        if read_previous_json(name_file):
            added_features, removed_features, modified_features, columns_diff = service.get_features_updates(name_file)
            if not added_features.empty or not removed_features.empty or not modified_features.empty or columns_diff:
                excel_path = generate_report(added_features, removed_features, modified_features, columns_diff,
                                             name_file)
                save_previous_json_backup(name_file)
                json_path = write_JSON_file(service.to_json, name_file)
                return json_path, excel_path
            else:
                return None, None
        else:
            json_path = write_JSON_file(service.to_json, name_file)
            return json_path, None
