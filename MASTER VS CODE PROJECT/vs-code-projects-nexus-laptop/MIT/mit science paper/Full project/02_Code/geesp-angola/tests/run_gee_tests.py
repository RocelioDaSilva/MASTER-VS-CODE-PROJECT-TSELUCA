import sys
from pathlib import Path

# Ensure project root is on sys.path so `import scripts` works
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from unittest.mock import MagicMock
import importlib

MODULE_NAME = 'scripts.gee_extraction'

def test_gee_init_success():
    mock_ee = MagicMock()
    mock_ee.Initialize.return_value = None
    module = importlib.import_module(MODULE_NAME)
    setattr(module, 'ee', mock_ee)
    GEEExtractor = module.GEEExtractor
    extractor = GEEExtractor(project_id='test')
    assert extractor.project_id == 'test'
    print('test_gee_init_success: OK')

def test_extract_solar_radiation():
    mock_ee = MagicMock()
    mock_collection = MagicMock()
    mock_image = MagicMock()
    mock_collection.select.return_value = mock_collection
    mock_collection.mean.return_value = mock_image
    mock_ee.ImageCollection.return_value = mock_collection
    mock_ee.Geometry = MagicMock()
    module = importlib.import_module(MODULE_NAME)
    setattr(module, 'ee', mock_ee)
    original_init = module.GEEExtractor.__init__
    module.GEEExtractor.__init__ = lambda self, project_id=None: None
    try:
        ge = module.GEEExtractor()
        result = module.GEEExtractor.extract_solar_radiation(ge, aoi='aoi', start_date='2022-01-01', end_date='2022-12-31')
        assert result == mock_image
        print('test_extract_solar_radiation: OK')
    finally:
        module.GEEExtractor.__init__ = original_init

def test_export_to_geotiff_starts_task():
    mock_ee = MagicMock()
    mock_task = MagicMock()
    mock_task.start = MagicMock()
    mock_ee.batch = MagicMock()
    mock_ee.batch.Export = MagicMock()
    mock_ee.batch.Export.image = MagicMock()
    mock_ee.batch.Export.image.toDrive.return_value = mock_task
    module = importlib.import_module(MODULE_NAME)
    setattr(module, 'ee', mock_ee)
    original_init = module.GEEExtractor.__init__
    module.GEEExtractor.__init__ = lambda self, project_id=None: None
    try:
        ge = module.GEEExtractor()
        task = module.GEEExtractor.export_to_geotiff(ge, image='img', aoi='aoi', filename='out.tif')
        assert task is mock_task
        mock_ee.batch.Export.image.toDrive.assert_called_once()
        mock_task.start.assert_called_once()
        print('test_export_to_geotiff_starts_task: OK')
    finally:
        module.GEEExtractor.__init__ = original_init

def test_create_aoi_from_bbox_calls_bbox():
    mock_ee = MagicMock()
    mock_bbox = MagicMock()
    mock_ee.Geometry = MagicMock()
    mock_ee.Geometry.BBox.return_value = mock_bbox
    module = importlib.import_module(MODULE_NAME)
    setattr(module, 'ee', mock_ee)
    original_init = module.GEEExtractor.__init__
    module.GEEExtractor.__init__ = lambda self, project_id=None: None
    try:
        ge = module.GEEExtractor()
        res = module.GEEExtractor.create_aoi_from_bbox(ge, [14.0, -18.5, 15.5, -17.0])
        mock_ee.Geometry.BBox.assert_called_once_with(14.0, -18.5, 15.5, -17.0)
        assert res == mock_bbox
        print('test_create_aoi_from_bbox_calls_bbox: OK')
    finally:
        module.GEEExtractor.__init__ = original_init

if __name__ == '__main__':
    try:
        test_gee_init_success()
        test_extract_solar_radiation()
        test_export_to_geotiff_starts_task()
        test_create_aoi_from_bbox_calls_bbox()
        print('ALL GEE MOCK TESTS PASSED')
        sys.exit(0)
    except AssertionError as e:
        print('TEST FAILED:', e)
        sys.exit(2)
    except Exception as e:
        print('ERROR DURING TESTS:', e)
        sys.exit(3)
