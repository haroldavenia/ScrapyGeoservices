from src.services.EsriRestService import EsriRestService
from src.utils.Utils import read_previous_json, generate_report, save_previous_json_backup, write_JSON_file


class EsriController:

    @staticmethod
    async def query_layer(kwargs):
        service = EsriRestService(kwargs.get('layer_url'), "attributes." + kwargs.get('attr_id', 'objectid'))
        await service.query_layer(where=kwargs.get('where_clause', '1=1'), out_fields=kwargs.get('out_fields', "*"),
                                  return_geometry=kwargs.get('return_geometry', True),
                                  geometry=kwargs.get('geometry', None))
        name_file = kwargs.get('name_file', "esri_layer_query")
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
