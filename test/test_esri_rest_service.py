import pytest
from arcgis.geometry import Envelope
from src.services.EsriRestService import EsriRestService
import os


# Fixture for setting up the service instance
@pytest.fixture
def esri_service():
    layer_url = "https://sampleserver6.arcgisonline.com/arcgis/rest/services/Census/MapServer/3"
    return EsriRestService(layer_url, "attributes.OBJECTID")


@pytest.mark.asyncio
async def test_query_layer(esri_service):
    await esri_service.query_layer()
    features = esri_service.get_features
    assert features is not None, "Features should not be None after querying the layer."
    assert len(features) > 0, "Features should not be empty after querying the layer."


@pytest.mark.asyncio
async def test_query_layer_with_geometry(esri_service):
    geometry = Envelope({
        "xmin": -130,
        "ymin": 20,
        "xmax": -60,
        "ymax": 50,
        "spatialReference": {"wkid": 4326}
    })
    await esri_service.query_layer(geometry=geometry)
    features = esri_service.get_features
    assert features is not None, "Features should not be None after querying the layer with geometry."
    assert len(features) > 0, "Features should not be empty after querying the layer with geometry."


@pytest.mark.asyncio
async def test_write_JSON_file(esri_service, tmp_path):
    await esri_service.query_layer()
    json_path = esri_service.write_JSON_file("test_esri_layer_query")
    assert os.path.exists(json_path), "JSON file should be created after writing."
    with open(json_path) as f:
        data = f.read()
        assert data is not None, "Data should be written in JSON file."


@pytest.mark.asyncio
async def test_get_feature_layer_df(esri_service):
    await esri_service.query_layer()
    df = esri_service.get_feature_layer_df()
    assert df is not None, "DataFrame should not be None."
    assert not df.empty, "DataFrame should not be empty."
    assert 'attributes.OBJECTID' in df.columns, "DataFrame should contain 'attributes.objectid' column."



@pytest.mark.asyncio
async def test_compare_features(esri_service, tmp_path):
    await esri_service.query_layer()
    features = esri_service.get_features
    assert features is not None, "Features should not be None after querying the layer."
    assert len(features) > 0, "Features should not be empty after querying the layer."

    json_path = esri_service.write_JSON_file("test_esri_layer_query")
    assert os.path.exists(json_path), "JSON file should be created after writing."

    geometry = Envelope({
        "xmin": -80.379278,  # Longitud mínima para Doral, Miami
        "ymin": 25.788655,  # Latitud mínima para Doral, Miami
        "xmax": -80.326853,  # Longitud máxima para Doral, Miami
        "ymax": 25.858582,  # Latitud máxima para Doral, Miami
        "spatialReference": {"wkid": 4326}  # Sistema de referencia espacial (WGS84)
    })
    await esri_service.query_layer(geometry=geometry)
    features = esri_service.get_features
    assert features is not None, "Features should not be None after querying the layer with geometry."
    assert len(features) > 0, "Features should not be empty after querying the layer with geometry."

    added, removed, modified, columns_diff = esri_service.get_features_updates("test_esri_layer_query")
    assert added.empty, "Added features should be empty."
    assert len(removed) > 0, "Removed features should be > 0"
    assert modified.empty, "Modified features should be empty."
    assert columns_diff is None, "Columns diff should be None."

    report_path = tmp_path / "test_report.xlsx"
    esri_service.generate_report(added, removed, modified, columns_diff, "test_esri_layer_query")
    assert os.path.exists(report_path), "Report file should be created after generating report."


# # Create an instance of the service and query the layer with optional parameters
# layer_url = "https://serviciosgis.ign.es/servicios/rest/services/Signa/Servicios_Industria/MapServer/23"
# service = EsriRestService(layer_url)
# bbox = Envelope({
#     "xmin": -3.756324,
#     "ymin": 40.382712,
#     "xmax": -3.625947,
#     "ymax": 40.428136,
#     "spatialReference": {"wkid": 4326}
# })
# # bbox = Envelope({
# #     "xmin": -19.246918,
# #     "ymin": 34.119511,
# #     "xmax": 14.129547,
# #     "ymax": 45.777847,
# #     "spatialReference": {"wkid": 4326}
# # })