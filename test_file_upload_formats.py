import pytest

import requests
import tests.utils.configuration as configuration

FILE_CASES = [
    ("test_image.jpg", "image/jpg"),
    ("test_image.png", "image/png"),
    ("test_image.gif", "image/gif"),
    ("test_image.webp", "image/webp"),

    # Документы
    ("test_doc.pdf", "document/pdf"),
    ("test_doc.docx", "document/docx"),
    ("test_doc.xlsx", "document/xlsx"),
    ("test_doc.xls", "document/xls"),
    ("test_doc.ppt", "document/ppt"),
    ("test_doc.pptx", "document/pptx"),
    ("test_doc.txt", "document/txt")


    # Аудио
    ("test_audio.mp3", "audio/mp3"),
    ("test_audio.wav", "audio/wav"),
    ("test_audio.ogg", "audio/ogg"),
    ("test_audio.opus", "audio/opus"),
    ("test_audio.webm_audio.webm", "audio/webm"),  # имя отличается, чтобы не путать с видео

    # Видео
    ("test_video.mov", "video/quicktime"),
    ("test_video.webm", "video/webm"),
    ("test_video.mkv", "video/x-matroska"),
    ("test_video.avi", "video/x-msvideo")
]



@pytest.mark.parametrize("filename, mime_type", FILE_CASES)
def test_file_upload(access_token, filename, mime_type, assets_dir):
    file_path = assets_dir / filename
    assert file_path.exists(), f"Файл не найден: {file_path}"
    
    url = configuration.BASE_URL + configuration.FILE_UPLOAD_PATH

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    with open(file_path, "rb") as f:
        files = {
            "file": (filename, f, mime_type)  # сам файл
        }
        data = {
            "type": mime_type  # дополнительное поле в multipart/form-data
        }
        response = requests.post(url, headers=headers, files=files, data=data)

    assert response.status_code == 200, f"Ошибка при загрузке {filename}: {response.text}"
    json_data = response.json()
    assert "url" in json_data
    assert json_data["filename"] == filename
