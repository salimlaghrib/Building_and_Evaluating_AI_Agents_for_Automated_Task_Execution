import pytest

from app.services.vision_service import VisionService


def test_resolve_image_path_accepts_jpg_name_for_existing_jpeg_upload():
    service = VisionService()

    image_path = service._resolve_image_path("matelas_02.jpg")

    assert image_path is not None
    assert image_path.name == "matelas_02.jpeg"
    assert image_path.exists()


def test_resolve_image_path_uses_project_uploads_directory():
    service = VisionService()

    image_path = service._resolve_image_path("uploads/raw/matelas_02.jpeg")

    assert image_path is not None
    assert image_path == service.uploads_dir / "matelas_02.jpeg"


def test_analyze_without_gemini_key_returns_error_instead_of_fake_order():
    service = VisionService()
    service.client = None

    with pytest.raises(RuntimeError, match="GEMINI_API_KEY non configurée"):
        service.analyze("matelas_01.jpg")
