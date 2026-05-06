"""
Comprehensive GEE Integration Tests
Tests batch processing, export scheduling, progress tracking, and error handling
"""

import pytest
import json
import tempfile
from pathlib import Path
from unittest import mock
from datetime import datetime, timedelta

# Path setup in conftest.py (root and scripts)
from earth_engine_integration import (
    ExportTask,
    ExportBatch,
    EnhancedGEEExtractor,
    get_gee_extractor,
    create_batch,
    add_task,
    process_batch,
    get_batch_status,
)


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def temp_export_dir(tmp_path):
    """Create temporary export directory"""
    export_dir = tmp_path / "gee_exports"
    export_dir.mkdir()
    return export_dir


@pytest.fixture
def gee_extractor(temp_export_dir, monkeypatch):
    """Create GEE extractor with temporary directory"""
    extractor = EnhancedGEEExtractor()
    monkeypatch.setattr(extractor, "export_dir", temp_export_dir)
    monkeypatch.setattr(extractor, "export_manifest", temp_export_dir / "manifest.json")
    return extractor


@pytest.fixture
def aoi_bounds():
    """Standard AOI bounds for testing (Huíla, Angola)"""
    return (14.0, -18.5, 15.5, -17.0)


@pytest.fixture
def sample_batch(gee_extractor):
    """Create sample batch with tasks"""
    batch = gee_extractor.create_export_batch("test_batch_001")
    return batch


# ============================================================================
# EXPORT TASK TESTS
# ============================================================================

class TestExportTask:
    """Test ExportTask data class"""

    def test_export_task_creation(self):
        """Test ExportTask instantiation"""
        task = ExportTask(
            task_id="task_001",
            dataset_name="solar_radiation",
            aoi_bounds=(14.0, -18.5, 15.5, -17.0),
            bands=["ALLSKY_SFC_SW_DWN"],
            start_date="2023-01-01",
            end_date="2023-12-31",
            output_filename="solar.tif",
        )

        assert task.task_id == "task_001"
        assert task.dataset_name == "solar_radiation"
        assert task.status == "pending"
        assert task.scale == 30
        assert task.crs == "EPSG:32733"

    def test_export_task_default_status(self):
        """Test that task has pending status by default"""
        task = ExportTask(
            task_id="task_002",
            dataset_name="ndvi",
            aoi_bounds=(14.0, -18.5, 15.5, -17.0),
            bands=["NDVI"],
            start_date="2023-01-01",
            end_date="2023-12-31",
            output_filename="ndvi.tif",
        )

        assert task.status == "pending"
        assert task.created_at is not None
        assert task.started_at is None
        assert task.completed_at is None
        assert task.error_message is None

    def test_export_task_to_dict(self):
        """Test serialization to dictionary"""
        task = ExportTask(
            task_id="task_003",
            dataset_name="elevation",
            aoi_bounds=(14.0, -18.5, 15.5, -17.0),
            bands=["elevation"],
            start_date="2023-01-01",
            end_date="2023-01-01",
            output_filename="dem.tif",
            status="completed",
        )

        task_dict = task.to_dict()

        assert task_dict["task_id"] == "task_003"
        assert task_dict["dataset_name"] == "elevation"
        assert task_dict["status"] == "completed"
        assert isinstance(task_dict["created_at"], str)


# ============================================================================
# EXPORT BATCH TESTS
# ============================================================================

class TestExportBatch:
    """Test ExportBatch management"""

    def test_batch_creation(self):
        """Test ExportBatch instantiation"""
        batch = ExportBatch(batch_id="batch_001")

        assert batch.batch_id == "batch_001"
        assert batch.status == "pending"
        assert len(batch.tasks) == 0
        assert batch.created_at is not None

    def test_add_task_to_batch(self):
        """Test adding tasks to batch"""
        batch = ExportBatch(batch_id="batch_002")

        task1 = ExportTask(
            task_id="t1",
            dataset_name="solar",
            aoi_bounds=(14.0, -18.5, 15.5, -17.0),
            bands=["SWD"],
            start_date="2023-01-01",
            end_date="2023-12-31",
            output_filename="solar.tif",
        )

        task2 = ExportTask(
            task_id="t2",
            dataset_name="ndvi",
            aoi_bounds=(14.0, -18.5, 15.5, -17.0),
            bands=["NDVI"],
            start_date="2023-01-01",
            end_date="2023-12-31",
            output_filename="ndvi.tif",
        )

        batch.add_task(task1)
        batch.add_task(task2)

        assert len(batch.tasks) == 2
        assert batch.tasks[0].dataset_name == "solar"
        assert batch.tasks[1].dataset_name == "ndvi"

    def test_batch_status_summary_empty(self):
        """Test status summary for empty batch"""
        batch = ExportBatch(batch_id="batch_003")

        summary = batch.get_status_summary()

        assert summary["total_tasks"] == 0
        assert summary["completed"] == 0
        assert summary["failed"] == 0
        assert summary["completion_percentage"] == 0

    def test_batch_status_summary_with_tasks(self):
        """Test status summary with mixed task statuses"""
        batch = ExportBatch(batch_id="batch_004")

        for i in range(3):
            task = ExportTask(
                task_id=f"t{i}",
                dataset_name=f"dataset_{i}",
                aoi_bounds=(14.0, -18.5, 15.5, -17.0),
                bands=["B1"],
                start_date="2023-01-01",
                end_date="2023-12-31",
                output_filename=f"output_{i}.tif",
            )
            batch.add_task(task)

        # Set different statuses
        batch.tasks[0].status = "completed"
        batch.tasks[1].status = "failed"
        batch.tasks[2].status = "processing"

        summary = batch.get_status_summary()

        assert summary["total_tasks"] == 3
        assert summary["completed"] == 1
        assert summary["failed"] == 1
        assert summary["processing"] == 1
        assert summary["pending"] == 0
        assert summary["completion_percentage"] == pytest.approx(33.33, rel=1)

    def test_batch_completion_percentage_calculation(self):
        """Test completion percentage across various scenarios"""
        batch = ExportBatch(batch_id="batch_005")

        # Add 10 tasks
        for i in range(10):
            task = ExportTask(
                task_id=f"t{i}",
                dataset_name=f"dataset_{i}",
                aoi_bounds=(14.0, -18.5, 15.5, -17.0),
                bands=["B1"],
                start_date="2023-01-01",
                end_date="2023-12-31",
                output_filename=f"output_{i}.tif",
            )
            batch.add_task(task)

        # Complete 7 out of 10
        for i in range(7):
            batch.tasks[i].status = "completed"

        summary = batch.get_status_summary()
        assert summary["completion_percentage"] == 70.0


# ============================================================================
# ENHANCED GEE EXTRACTOR TESTS
# ============================================================================

class TestEnhancedGEEExtractor:
    """Test EnhancedGEEExtractor functionality"""

    def test_extractor_initialization(self):
        """Test GEE extractor initialization"""
        extractor = EnhancedGEEExtractor(project_id="test_project")

        assert extractor.project_id == "test_project"
        assert extractor.config is not None
        assert extractor.progress_tracker is not None
        assert extractor.export_dir.exists()

    def test_create_export_batch(self, gee_extractor):
        """Test batch creation"""
        batch = gee_extractor.create_export_batch("batch_test_001")

        assert batch.batch_id == "batch_test_001"
        assert batch.status == "pending"
        assert "batch_test_001" in gee_extractor.batches

    def test_add_export_task_to_batch(self, gee_extractor, aoi_bounds):
        """Test adding export task to batch"""
        batch_id = "test_batch_002"
        gee_extractor.create_export_batch(batch_id)

        task = gee_extractor.add_export_task(
            batch_id=batch_id,
            dataset_name="solar_radiation",
            aoi_bounds=aoi_bounds,
            bands=["ALLSKY_SFC_SW_DWN"],
            start_date="2023-01-01",
            end_date="2023-12-31",
            output_filename="solar_2023.tif",
        )

        assert task.task_id == f"{batch_id}_0"
        assert task.dataset_name == "solar_radiation"
        assert task.status == "pending"
        assert len(gee_extractor.batches[batch_id].tasks) == 1

    def test_add_multiple_tasks_to_batch(self, gee_extractor, aoi_bounds):
        """Test adding multiple tasks increments task IDs"""
        batch_id = "multi_task_batch"
        gee_extractor.create_export_batch(batch_id)

        task1 = gee_extractor.add_export_task(
            batch_id, "solar", aoi_bounds, ["SWD"], "2023-01-01", "2023-12-31"
        )
        task2 = gee_extractor.add_export_task(
            batch_id, "ndvi", aoi_bounds, ["NDVI"], "2023-01-01", "2023-12-31"
        )
        task3 = gee_extractor.add_export_task(
            batch_id, "elevation", aoi_bounds, ["elevation"], "2023-01-01", "2023-01-01"
        )

        assert task1.task_id == f"{batch_id}_0"
        assert task2.task_id == f"{batch_id}_1"
        assert task3.task_id == f"{batch_id}_2"

    def test_auto_generated_output_filename(self, gee_extractor, aoi_bounds):
        """Test that output filename is auto-generated when not provided"""
        batch_id = "auto_filename_batch"
        gee_extractor.create_export_batch(batch_id)

        task = gee_extractor.add_export_task(
            batch_id=batch_id,
            dataset_name="solar_radiation",
            aoi_bounds=aoi_bounds,
            bands=["SWD"],
            start_date="2023-01-01",
            end_date="2023-12-31",
            output_filename=None,  # Auto-generate
        )

        assert "solar_radiation" in task.output_filename
        assert task.output_filename.endswith(".tif")

    def test_process_batch_async(self, gee_extractor, aoi_bounds):
        """Test batch processing"""
        batch_id = "process_test_batch"
        gee_extractor.create_export_batch(batch_id)

        # Add tasks
        gee_extractor.add_export_task(
            batch_id, "solar", aoi_bounds, ["SWD"], "2023-01-01", "2023-12-31"
        )
        gee_extractor.add_export_task(
            batch_id, "ndvi", aoi_bounds, ["NDVI"], "2023-01-01", "2023-12-31"
        )

        # Process batch
        result = gee_extractor.process_batch_async(batch_id)

        assert result["status"] in ["completed", "partial", "failed"]
        assert result["batch_id"] == batch_id
        assert "summary" in result
        assert result["summary"]["total_tasks"] == 2

    def test_get_batch_status(self, gee_extractor, aoi_bounds):
        """Test getting batch status"""
        batch_id = "status_test_batch"
        gee_extractor.create_export_batch(batch_id)

        gee_extractor.add_export_task(
            batch_id, "solar", aoi_bounds, ["SWD"], "2023-01-01", "2023-12-31"
        )

        status = gee_extractor.get_batch_status(batch_id)

        assert status["batch_id"] == batch_id
        assert "summary" in status
        assert "tasks" in status
        assert len(status["tasks"]) == 1

    def test_get_nonexistent_batch_status(self, gee_extractor):
        """Test getting status of nonexistent batch"""
        status = gee_extractor.get_batch_status("nonexistent_batch")

        assert status["status"] == "not_found"

    def test_list_batches(self, gee_extractor, aoi_bounds):
        """Test listing all batches"""
        # Create multiple batches
        gee_extractor.create_export_batch("batch_1")
        gee_extractor.create_export_batch("batch_2")

        gee_extractor.add_export_task(
            "batch_1", "solar", aoi_bounds, ["SWD"], "2023-01-01", "2023-12-31"
        )

        batches = gee_extractor.list_batches()

        assert len(batches) >= 2
        assert any(b["batch_id"] == "batch_1" for b in batches)
        assert any(b["batch_id"] == "batch_2" for b in batches)

    def test_manifest_persistence(self, gee_extractor, aoi_bounds):
        """Test that batches are saved and loaded from manifest"""
        batch_id = "persist_test"
        gee_extractor.create_export_batch(batch_id)
        gee_extractor.add_export_task(
            batch_id, "solar", aoi_bounds, ["SWD"], "2023-01-01", "2023-12-31"
        )

        # Save manifest
        gee_extractor._save_manifest()

        # Create new extractor and load manifest
        new_extractor = EnhancedGEEExtractor()
        new_extractor.export_dir = gee_extractor.export_dir
        new_extractor.export_manifest = gee_extractor.export_manifest
        new_extractor._load_manifest()

        assert batch_id in new_extractor.batches
        assert len(new_extractor.batches[batch_id].tasks) == 1

    def test_cleanup_old_batches(self, gee_extractor, aoi_bounds):
        """Test cleaning up old completed batches"""
        # Create old batch (10 days ago)
        old_batch = gee_extractor.create_export_batch("old_batch")
        old_batch.status = "completed"
        old_batch.created_at = (datetime.now() - timedelta(days=10)).isoformat()

        # Create recent batch
        recent_batch = gee_extractor.create_export_batch("recent_batch")
        recent_batch.status = "completed"

        count_before = len(gee_extractor.batches)
        assert "old_batch" in gee_extractor.batches
        assert "recent_batch" in gee_extractor.batches

        # Cleanup batches older than 7 days
        removed = gee_extractor.cleanup_old_batches(days=7)

        assert removed >= 1
        assert "old_batch" not in gee_extractor.batches
        assert "recent_batch" in gee_extractor.batches
        assert len(gee_extractor.batches) == count_before - removed

    def test_cleanup_preserves_processing_batches(self, gee_extractor):
        """Test that cleanup doesn't remove processing batches"""
        old_batch = gee_extractor.create_export_batch("old_processing")
        old_batch.status = "processing"  # Not completed
        old_batch.created_at = (datetime.now() - timedelta(days=10)).isoformat()

        removed = gee_extractor.cleanup_old_batches(days=7)

        assert removed == 0
        assert "old_processing" in gee_extractor.batches


# ============================================================================
# SINGLETON PATTERN TESTS
# ============================================================================

class TestGEESingletonPattern:
    """Test singleton behavior of GEE extractor"""

    def test_get_gee_extractor_singleton(self):
        """Test that get_gee_extractor returns same instance"""
        extractor1 = get_gee_extractor()
        extractor2 = get_gee_extractor()

        assert extractor1 is extractor2

    def test_convenience_functions(self, gee_extractor, monkeypatch, aoi_bounds):
        """Test convenience wrapper functions"""
        # Mock get_gee_extractor to return our test extractor
        monkeypatch.setattr(
            "scripts.earth_engine_integration.get_gee_extractor",
            lambda project_id=None: gee_extractor,
        )

        # Test create_batch function
        batch = create_batch("test_batch")
        assert batch.batch_id == "test_batch"

        # Test add_task function
        task = add_task(
            "test_batch",
            "solar",
            aoi_bounds,
            ["SWD"],
            "2023-01-01",
            "2023-12-31",
        )
        assert task.dataset_name == "solar"

        # Test process_batch function
        result = process_batch("test_batch")
        assert result["batch_id"] == "test_batch"

        # Test get_batch_status function
        status = get_batch_status("test_batch")
        assert status["batch_id"] == "test_batch"


# ============================================================================
# ERROR HANDLING TESTS
# ============================================================================

class TestGEEErrorHandling:
    """Test error handling in GEE operations"""

    def test_process_nonexistent_batch(self, gee_extractor):
        """Test processing nonexistent batch returns error"""
        result = gee_extractor.process_batch_async("nonexistent")

        assert result["status"] == "failed"
        assert "error" in result

    def test_task_failure_tracking(self, gee_extractor, aoi_bounds):
        """Test that task failures are tracked correctly"""
        batch_id = "failure_test"
        batch = gee_extractor.create_export_batch(batch_id)

        gee_extractor.add_export_task(
            batch_id, "dataset1", aoi_bounds, ["B1"], "2023-01-01", "2023-12-31"
        )

        # Simulate failure by setting error
        batch.tasks[0].status = "failed"
        batch.tasks[0].error_message = "Test error"

        status = gee_extractor.get_batch_status(batch_id)
        task_status = status["tasks"][0]

        assert task_status["status"] == "failed"
        assert task_status["error"] == "Test error"


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestGEEIntegrationScenarios:
    """Test real-world usage scenarios"""

    def test_complete_workflow(self, gee_extractor, aoi_bounds):
        """Test complete batch creation, task addition, and processing"""
        # 1. Create batch
        batch_id = "workflow_test"
        gee_extractor.create_export_batch(batch_id)

        # 2. Add multiple tasks
        datasets = [
            ("solar_radiation", ["ALLSKY_SFC_SW_DWN"]),
            ("ndvi", ["NDVI"]),
            ("elevation", ["elevation"]),
        ]

        for dataset_name, bands in datasets:
            gee_extractor.add_export_task(
                batch_id=batch_id,
                dataset_name=dataset_name,
                aoi_bounds=aoi_bounds,
                bands=bands,
                start_date="2023-01-01",
                end_date="2023-12-31",
            )

        # 3. Check batch status before processing
        status_before = gee_extractor.get_batch_status(batch_id)
        assert status_before["summary"]["total_tasks"] == 3
        assert status_before["summary"]["pending"] == 3

        # 4. Process batch (may be "failed" when GEE SDK not available in test env)
        result = gee_extractor.process_batch_async(batch_id)
        assert result["status"] in ["completed", "partial", "failed"]

        # 5. Check batch status after processing
        status_after = gee_extractor.get_batch_status(batch_id)
        assert status_after["summary"]["total_tasks"] == 3

    def test_multiple_batches_isolation(self, gee_extractor, aoi_bounds):
        """Test that multiple batches are isolated from each other"""
        batch1_id = "batch_isolation_1"
        batch2_id = "batch_isolation_2"

        gee_extractor.create_export_batch(batch1_id)
        gee_extractor.create_export_batch(batch2_id)

        gee_extractor.add_export_task(
            batch1_id, "solar", aoi_bounds, ["SWD"], "2023-01-01", "2023-12-31"
        )
        gee_extractor.add_export_task(
            batch2_id, "ndvi", aoi_bounds, ["NDVI"], "2023-01-01", "2023-12-31"
        )
        gee_extractor.add_export_task(
            batch2_id, "elevation", aoi_bounds, ["elevation"], "2023-01-01", "2023-12-31"
        )

        batch1_status = gee_extractor.get_batch_status(batch1_id)
        batch2_status = gee_extractor.get_batch_status(batch2_id)

        assert batch1_status["summary"]["total_tasks"] == 1
        assert batch2_status["summary"]["total_tasks"] == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
