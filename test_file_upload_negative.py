import pytest
from pathlib import Path
import requests
import tests.utils.configuration as configuration

test_results = {}

@pytest.mark.parametrize("description, file_data, expected_status", [
    ("без авторизации", {"auth": False}, 401),
    ("без файла", {"no_file": True}, 400),
    ("с неподдерживаемым MIME", {"mime_type": "application/x-unknown"}, 415),
    ("с пустым файлом", {"empty_file": True}, 400),
    ("с изменённым расширением (jpg → txt)", {"fake_extension": True}, 415)
])
def test_file_upload_negative(description, file_data, expected_status, access_token, assets_dir, tmp_path):

    file_path = assets_dir / "test_image.jpg"
    url = configuration.BASE_URL + configuration.FILE_UPLOAD_PATH
    headers = {}

    if file_data.get("auth", True):
        headers["Authorization"] = f"Bearer {access_token}"

    data = {
        "scale": "1.0",
        "positionX": "0.0",
        "positionY": "0.0"
    }

    files = {}

    current_dir = Path(__file__).parent
    assets_dir = current_dir / "assets"
    file_path = assets_dir / "test_image.jpg"  # валидный файл

    if file_data.get("empty_file"):
        empty_path = tmp_path / "empty_test_file.jpg"
        empty_path.write_bytes(b"")
        file_path = empty_path

    if file_data.get("fake_extension"):
        # создаём копию с поддельным расширением во временной папке tmp_path
        fake_path = tmp_path / "test_image.txt"
        fake_path.write_bytes(file_path.read_bytes())
        file_path = fake_path

    if not file_data.get("no_file"):
        assert file_path.exists(), f"Файл не найден: {file_path}"
        mime_type = file_data.get("mime_type", "image/jpeg")

        with open(file_path, "rb") as f:
            # имя файла в кортеже должно соответствовать расширению, чтобы проверить именно расширение
            filename = file_path.name
            files["file"] = (filename, f, mime_type)

            response = requests.post(url, headers=headers, files=files, data=data)
    else:
        # запрос без файла
        response = requests.post(url, headers=headers, data=data)

    try:
        assert response.status_code == expected_status
        test_results[description] = "PASSED"
    except AssertionError:
        test_results[description] = "FAILED"
        raise
