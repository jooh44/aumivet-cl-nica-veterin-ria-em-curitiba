#!/usr/bin/env python3
"""Tray API auth and smoke-test helper.

Reads credentials from environment or an ignored .env.tray file.
Do not commit real credentials or generated tokens.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from urllib import parse, request
from urllib.error import HTTPError, URLError


ADS_ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT = ADS_ROOT.parent
GLOBAL_ENV_PATH = PROJECT_ROOT / ".env.tray"
LEGACY_ENV_PATH = ADS_ROOT / ".env.tray"
DEFAULT_ENV_PATH = GLOBAL_ENV_PATH
TRACKED_ENV_KEYS = [
    "TRAY_STORE_HOST",
    "TRAY_CALLBACK_URL",
    "TRAY_API_ADDRESS",
    "TRAY_CONSUMER_KEY",
    "TRAY_CONSUMER_SECRET",
    "TRAY_CODE",
    "TRAY_STORE_ID",
    "TRAY_ACCESS_TOKEN",
    "TRAY_REFRESH_TOKEN",
]


def load_env(path: Path) -> dict[str, str]:
    env = dict(os.environ)
    if not path.exists():
        return env

    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        env[key.strip()] = value.strip().strip('"').strip("'")
    return env


def persist_env(path: Path, env: dict[str, str], payload: dict) -> None:
    data = {key: env.get(key, "") for key in TRACKED_ENV_KEYS}
    if payload.get("api_host"):
        data["TRAY_API_ADDRESS"] = payload["api_host"]
    if payload.get("store_id"):
        data["TRAY_STORE_ID"] = str(payload["store_id"])
    if payload.get("access_token"):
        data["TRAY_ACCESS_TOKEN"] = payload["access_token"]
    if payload.get("refresh_token"):
        data["TRAY_REFRESH_TOKEN"] = payload["refresh_token"]

    targets: list[Path] = []
    for candidate in (path, GLOBAL_ENV_PATH, LEGACY_ENV_PATH):
        if candidate not in targets:
            targets.append(candidate)

    for target in targets:
        write_env_file(target, data)


def write_env_file(path: Path, data: dict[str, str]) -> None:
    header = [
        "# Tray credentials and rotating tokens.",
        "# Ignored by git. Synced by ads-rz/scripts/tray/tray_auth_check.py.",
    ]

    existing_lines = []
    if path.exists():
        existing_lines = path.read_text(encoding="utf-8").splitlines()

    seen: set[str] = set()
    rendered: list[str] = []

    for line in existing_lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in line:
            rendered.append(line)
            continue
        key, _ = line.split("=", 1)
        key = key.strip()
        if key in data:
            rendered.append(f"{key}={data[key]}")
            seen.add(key)
        else:
            rendered.append(line)

    for key in TRACKED_ENV_KEYS:
        if key not in seen:
            rendered.append(f"{key}={data.get(key, '')}")

    if not existing_lines:
        rendered = [*header, *rendered]

    path.write_text("\n".join(rendered).rstrip() + "\n", encoding="utf-8")


def normalize_api_address(value: str) -> str:
    value = value.strip().rstrip("/")
    if not value:
        raise ValueError("TRAY_API_ADDRESS ausente.")
    if not value.startswith(("http://", "https://")):
        value = f"https://{value}"
    return value


def masked(value: str, keep: int = 6) -> str:
    if not value:
        return ""
    if len(value) <= keep * 2:
        return "*" * len(value)
    return f"{value[:keep]}...{value[-keep:]}"


def request_json(method: str, url: str, data: dict[str, str] | None = None) -> tuple[int, dict]:
    body = None
    headers = {"Accept": "application/json"}
    if data is not None:
        body = parse.urlencode(data).encode("utf-8")
        headers["Content-Type"] = "application/x-www-form-urlencoded"

    req = request.Request(url, data=body, headers=headers, method=method)
    try:
        with request.urlopen(req, timeout=30) as response:
            raw = response.read().decode("utf-8", errors="replace")
            return response.status, json.loads(raw) if raw else {}
    except HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        try:
            payload = json.loads(raw) if raw else {}
        except json.JSONDecodeError:
            payload = {"raw": raw}
        return exc.code, payload
    except URLError as exc:
        raise RuntimeError(f"Falha de rede: {exc}") from exc


def print_token_result(payload: dict, reveal: bool = False) -> None:
    print(json.dumps({
        "message": payload.get("message"),
        "code": payload.get("code"),
        "store_id": payload.get("store_id"),
        "api_host": payload.get("api_host"),
        "date_expiration_access_token": payload.get("date_expiration_access_token"),
        "date_expiration_refresh_token": payload.get("date_expiration_refresh_token"),
        "access_token": payload.get("access_token") if reveal else masked(payload.get("access_token", "")),
        "refresh_token": payload.get("refresh_token") if reveal else masked(payload.get("refresh_token", "")),
    }, ensure_ascii=False, indent=2))


def cmd_auth(env: dict[str, str], reveal: bool, env_path: Path) -> int:
    required = ["TRAY_API_ADDRESS", "TRAY_CONSUMER_KEY", "TRAY_CONSUMER_SECRET", "TRAY_CODE"]
    missing = [key for key in required if not env.get(key)]
    if missing:
        print(f"Variaveis ausentes: {', '.join(missing)}", file=sys.stderr)
        return 2
    api_address = normalize_api_address(env["TRAY_API_ADDRESS"])

    status, payload = request_json(
        "POST",
        f"{api_address}/auth",
        {
            "consumer_key": env["TRAY_CONSUMER_KEY"],
            "consumer_secret": env["TRAY_CONSUMER_SECRET"],
            "code": env["TRAY_CODE"],
        },
    )
    print(f"HTTP {status}")
    print_token_result(payload, reveal=reveal)
    if status in (200, 201):
        persist_env(env_path, env, payload)
    return 0 if status in (200, 201) else 1


def cmd_refresh(env: dict[str, str], reveal: bool, env_path: Path) -> int:
    if not env.get("TRAY_API_ADDRESS"):
        print("TRAY_API_ADDRESS ausente.", file=sys.stderr)
        return 2
    api_address = normalize_api_address(env["TRAY_API_ADDRESS"])
    refresh_token = env.get("TRAY_REFRESH_TOKEN", "")
    if not refresh_token:
        print("TRAY_REFRESH_TOKEN ausente.", file=sys.stderr)
        return 2

    query = parse.urlencode({"refresh_token": refresh_token})
    status, payload = request_json("GET", f"{api_address}/auth?{query}")
    print(f"HTTP {status}")
    print_token_result(payload, reveal=reveal)
    if status in (200, 201):
        persist_env(env_path, env, payload)
    return 0 if status in (200, 201) else 1


def cmd_smoke(env: dict[str, str]) -> int:
    if not env.get("TRAY_API_ADDRESS"):
        print("TRAY_API_ADDRESS ausente.", file=sys.stderr)
        return 2
    api_address = normalize_api_address(env["TRAY_API_ADDRESS"])
    access_token = env.get("TRAY_ACCESS_TOKEN", "")
    if not access_token:
        print("TRAY_ACCESS_TOKEN ausente.", file=sys.stderr)
        return 2

    endpoints = [
        ("customers", {"limit": "1"}),
        ("orders", {"limit": "1"}),
        ("products", {"limit": "1"}),
    ]
    ok = True
    for resource, params in endpoints:
        query = {"access_token": access_token, **params}
        url = f"{api_address}/{resource}?{parse.urlencode(query)}"
        status, payload = request_json("GET", url)
        ok = ok and status in (200, 201)
        summary = {
            "resource": resource,
            "http_status": status,
            "api_code": payload.get("code"),
            "paging": payload.get("paging"),
            "top_level_keys": sorted(payload.keys())[:12],
        }
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if ok else 1


def cmd_auth_url(env: dict[str, str]) -> int:
    store_host = env.get("TRAY_STORE_HOST", "").strip().rstrip("/")
    consumer_key = env.get("TRAY_CONSUMER_KEY", "").strip()
    callback = env.get("TRAY_CALLBACK_URL", "").strip()
    missing = [name for name, value in {
        "TRAY_STORE_HOST": store_host,
        "TRAY_CONSUMER_KEY": consumer_key,
        "TRAY_CALLBACK_URL": callback,
    }.items() if not value]
    if missing:
        print(f"Variaveis ausentes: {', '.join(missing)}", file=sys.stderr)
        return 2
    query = parse.urlencode({
        "response_type": "code",
        "consumer_key": consumer_key,
        "callback": callback,
    })
    print(f"{store_host}/auth.php?{query}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Valida credenciais e tokens da API Tray.")
    parser.add_argument("--env", default=str(DEFAULT_ENV_PATH), help="Arquivo .env.tray ignorado pelo git.")
    parser.add_argument("--reveal", action="store_true", help="Mostra tokens completos no stdout.")

    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("auth-url", help="Gera URL de autorizacao para obter code.")
    sub.add_parser("auth", help="Troca code por access_token e refresh_token.")
    sub.add_parser("refresh", help="Atualiza access_token usando refresh_token.")
    sub.add_parser("smoke", help="Testa customers, orders e products com limit=1.")

    args = parser.parse_args()
    env_path = Path(args.env)
    env = load_env(env_path)

    if args.command == "auth-url":
        return cmd_auth_url(env)
    if args.command == "auth":
        return cmd_auth(env, args.reveal, env_path)
    if args.command == "refresh":
        return cmd_refresh(env, args.reveal, env_path)
    if args.command == "smoke":
        return cmd_smoke(env)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
