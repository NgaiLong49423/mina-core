"""Shared Google Drive authentication helpers for Mina Core.

This module centralizes OAuth flow and Drive service creation,
using credentials/token stored under the local `secrets/` folder.
"""

from __future__ import annotations

import os
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Readonly access to Drive; adjust if you need more scopes.
SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

_BASE_DIR = Path(__file__).resolve().parent

# Cho phép override thư mục secrets qua biến môi trường MINA_SECRETS_DIR.
_secrets_dir_env = os.getenv("MINA_SECRETS_DIR")
if _secrets_dir_env:
    _SECRETS_DIR = Path(_secrets_dir_env).expanduser().resolve()
else:
    _SECRETS_DIR = _BASE_DIR / "secrets"
_TOKEN_PATH = _SECRETS_DIR / "token.json"
_CREDENTIALS_PATH = _SECRETS_DIR / "credentials.json"


def get_credentials() -> Credentials:
    """Load or obtain OAuth credentials for Google Drive.

    - Prefers an existing token.json in Mina_Core/secrets.
    - If token is missing/invalid, runs the local OAuth flow
      based on credentials.json in the same secrets folder.
    """
    creds: Credentials | None = None

    if _TOKEN_PATH.exists():
        creds = Credentials.from_authorized_user_file(str(_TOKEN_PATH), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not _CREDENTIALS_PATH.exists():
                raise FileNotFoundError(
                    "Không tìm thấy credentials.json. "
                    "Hãy đặt file này trong thư mục 'secrets' cạnh Mina_Core "
                    "hoặc cấu hình biến môi trường MINA_SECRETS_DIR trỏ tới thư mục chứa file. "
                    f"(Đường dẫn đang dùng: {_SECRETS_DIR})"
                )
            flow = InstalledAppFlow.from_client_secrets_file(
                str(_CREDENTIALS_PATH), SCOPES
            )
            creds = flow.run_local_server(port=0)

        _SECRETS_DIR.mkdir(parents=True, exist_ok=True)
        _TOKEN_PATH.write_text(creds.to_json(), encoding="utf-8")

    return creds


def get_drive_service():
    """Return an authenticated Google Drive v3 service client."""
    creds = get_credentials()
    return build("drive", "v3", credentials=creds)
