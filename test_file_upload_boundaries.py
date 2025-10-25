import pytest
from pathlib import Path
import requests
import tests.utils.configuration as configuration

@pytest.mark.parametrize("description, file_size_mb, expected_status", [
    ("файл чуть меньше 10 МБ", 9.9, 200),
    ("файл ровно 10 МБ", 10.0, 200),
    ("файл чуть больше 10 МБ", 10.1, 400),  # или 400 — зависит от сервера
])
# Используем фикстуру tmp_path для записи в нее файлов измененного размера

def test_file_upload_boundary_sizes(description, file_size_mb, expected_status, access_token, assets_dir, tmp_path):

    url = configuration.BASE_URL + configuration.FILE_UPLOAD_PATH
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    data = {
        "scale": "1.0",
        "positionX": "0.0",
        "positionY": "0.0"
    }

    current_dir = Path(__file__).parent
    assets_dir = current_dir / "assets"
    original_file = assets_dir / "test_image.jpg"
    assert original_file.exists(), f"Файл не найден: {original_file}"

    size_bytes = int(file_size_mb * 1024 * 1024)
    temp_file = tmp_path / f"resized_{file_size_mb}_mb.jpg"

    if not temp_file.exists() or temp_file.stat().st_size != size_bytes:
        with open(original_file, "rb") as src:
            content = src.read()

        if len(content) < size_bytes:
            padding = b"\x00" * (size_bytes - len(content))
            resized_content = content + padding
        else:
            resized_content = content[:size_bytes]

        with open(temp_file, "wb") as out:
            out.write(resized_content)

    with open(temp_file, "rb") as f:
        files = {"file": (temp_file.name, f, "image/jpeg")}
        response = requests.post(url, headers=headers, files=files, data=data)

    assert response.status_code == expected_status, (
        f"{description}: ожидался статус {expected_status}, получен {response.status_code}. "
        f"Ответ: {response.text}"
    )
