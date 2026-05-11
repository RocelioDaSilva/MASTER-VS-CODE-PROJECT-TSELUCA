import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../app_codebase/geesp-angola/backend')))
from utils.helpers import setup_project_paths
setup_project_paths()

from unittest.mock import patch, MagicMock
import pytest

MODULE_PATH = 'scripts.gee_extraction'

@patch(f'{MODULE_PATH}.ee')
def test_gee_init_success(mock_ee):
    # ee.Initialize should be callable without raising
    mock_ee.Initialize.return_value = None
    from scripts.gee_extraction import GEEExtractor

    extractor = GEEExtractor(project_id='test')
    assert extractor.project_id == 'test'
    mock_ee.Initialize.assert_called_once()

@patch(f'{MODULE_PATH}.ee')
def test_extract_solar_radiation(mock_ee):
    # Prepare mock chain for ImageCollection.select().mean()
    mock_collection = MagicMock()
    mock_image = MagicMock()
    mock_collection.select.return_value = mock_collection
    mock_collection.mean.return_value = mock_image
    mock_ee.ImageCollection.return_value = mock_collection
    mock_ee.Geometry = MagicMock()

    from scripts.gee_extraction import GEEExtractor
    extractor = MagicMock()
    # instantiate real extractor but patch its __init__ to avoid ee.Initialize
    with patch('scripts.gee_extraction.GEEExtractor.__init__', lambda self, project_id=None: None):
        ge = __import__('scripts.gee_extraction', fromlist=['GEEExtractor']).GEEExtractor()
        # Call method with dummy args
        result = __import__('scripts.gee_extraction', fromlist=['GEEExtractor']).GEEExtractor.extract_solar_radiation(ge, aoi='aoi', start_date='2022-01-01', end_date='2022-12-31')
        assert result == mock_image
        mock_ee.ImageCollection.assert_called()

@patch(f'{MODULE_PATH}.ee')
def test_export_to_geotiff_starts_task(mock_ee):
    # Mock the batch export chain
    mock_task = MagicMock()
    mock_task.start = MagicMock()
    mock_export = MagicMock()
    mock_export.start = MagicMock()
    # ee.batch.Export.image.toDrive should return a task-like object
    mock_ee.batch = MagicMock()
    mock_ee.batch.Export = MagicMock()
    mock_ee.batch.Export.image = MagicMock()
    mock_ee.batch.Export.image.toDrive.return_value = mock_task

    # Patch GEEExtractor.__init__ to skip Initialize
    with patch('scripts.gee_extraction.GEEExtractor.__init__', lambda self, project_id=None: None):
        from scripts.gee_extraction import GEEExtractor
        ge = GEEExtractor()
        task = GEEExtractor.export_to_geotiff(ge, image='img', aoi='aoi', filename='out.tif')
        assert task is mock_task
        mock_ee.batch.Export.image.toDrive.assert_called_once()
        # Ensure start was called on task
        mock_task.start.assert_called_once()

@patch(f'{MODULE_PATH}.ee')
def test_create_aoi_from_bbox_calls_bbox(mock_ee):
    # Ensure Geometry.BBox is called with correct coords
    mock_bbox = MagicMock()
    mock_ee.Geometry = MagicMock()
    mock_ee.Geometry.BBox.return_value = mock_bbox
    with patch('scripts.gee_extraction.GEEExtractor.__init__', lambda self, project_id=None: None):
        from scripts.gee_extraction import GEEExtractor
        ge = GEEExtractor()
        res = GEEExtractor.create_aoi_from_bbox(ge, [14.0, -18.5, 15.5, -17.0])
        mock_ee.Geometry.BBox.assert_called_once_with(14.0, -18.5, 15.5, -17.0)
        assert res == mock_bbox
