"""Graphory CLI - login, status, logout.

This is step 2 of the 2-step user flow. Step 1 is signup at https://graphory.io.
After signing up and creating an org, users run `graphory login` to save their
API key locally so Python scripts can do `Graphory.from_config()`.

Commands:
    graphory login     Prompt for API key + org_id, validate, save to config.
    graphory status    Show current logged-in user + live graph stats.
    graphory logout    Delete the local config file.
    graphory --version Print SDK version.
"""

from __future__ import annotations

import argparse
import getpass
import json
import os
import stat
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import httpx

DEFAULT_BASE_URL = "https://api.graphory.io"
CONFIG_DIR = Path.home() / ".graphory"
CONFIG_PATH = CONFIG_DIR / "config.json"


def _get_version() -> str:
    try:
        from importlib.metadata import version, PackageNotFoundError
        try:
            return version("graphory")
        except PackageNotFoundError:
            return "0.0.0+local"
    except Exception:
        return "unknown"


def _load_config() -> Optional[dict]:
    if not CONFIG_PATH.exists():
        return None
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        print(f"error: failed to read {CONFIG_PATH}: {e}", file=sys.stderr)
        return None


def _save_config(config: dict) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    # Best-effort dir perms on POSIX.
    try:
        os.chmod(CONFIG_DIR, stat.S_IRWXU)
    except OSError:
        pass

    tmp = CONFIG_PATH.with_suffix(".json.tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)
    os.replace(tmp, CONFIG_PATH)

    # chmod 600 - on Windows this is a no-op but won't error.
    try:
        os.chmod(CONFIG_PATH, stat.S_IRUSR | stat.S_IWUSR)
    except OSError:
        pass


def _validate_key(base_url: str, api_key: str, org_id: str) -> tuple[bool, str]:
    """Hit /org/{org_id}/stats with the key. Returns (ok, message)."""
    url = f"{base_url.rstrip('/')}/org/{org_id}/stats"
    try:
        resp = httpx.get(
            url,
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=15.0,
        )
    except httpx.HTTPError as e:
        return False, f"could not reach {url}: {e}"

    if resp.status_code == 200:
        try:
            data = resp.json()
            total_nodes = data.get("total_nodes", "?")
            total_edges = data.get("total_edges", "?")
            return True, f"{total_nodes} nodes, {total_edges} edges"
        except Exception:
            return True, "ok"
    if resp.status_code in (401, 403):
        return False, f"auth rejected ({resp.status_code}): check API key and org_id"
    return False, f"API returned {resp.status_code}: {resp.text[:200]}"


# -- Commands ----------------------------------------------------------------

def cmd_login(args: argparse.Namespace) -> int:
    base_url = args.base_url or os.environ.get("GRAPHORY_BASE_URL", DEFAULT_BASE_URL)
    print(f"Graphory login ({base_url})")
    print("Step 1: sign up at https://graphory.io and create an API key.")
    print("Step 2: paste your credentials below.\n")

    existing = _load_config()
    if existing:
        print(f"note: existing config at {CONFIG_PATH} will be overwritten.\n")

    try:
        api_key = getpass.getpass("API key (gs_ak_...): ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\naborted.")
        return 1

    if not api_key:
        print("error: no API key provided.", file=sys.stderr)
        return 1
    if not api_key.startswith("gs_ak_"):
        print("warning: key does not start with 'gs_ak_' - continuing anyway.")

    try:
        org_id = input("Org ID (org_01...): ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\naborted.")
        return 1

    if not org_id:
        print("error: org_id is required (the stats endpoint is org-scoped).", file=sys.stderr)
        return 1

    print("\nValidating credentials...")
    ok, msg = _validate_key(base_url, api_key, org_id)
    if not ok:
        print(f"error: {msg}", file=sys.stderr)
        print("config not saved.", file=sys.stderr)
        return 1

    config = {
        "api_key": api_key,
        "org_id": org_id,
        "base_url": base_url,
        "logged_in_at": datetime.now(timezone.utc).isoformat(),
    }
    _save_config(config)
    print(f"ok: {msg}")
    print(f"saved to {CONFIG_PATH}")
    print("\nYou can now use `from graphory import Graphory; g = Graphory.from_config()`")
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    config = _load_config()
    if not config:
        print(f"not logged in (no {CONFIG_PATH}).")
        print("run `graphory login` to get started.")
        return 1

    print(f"config:       {CONFIG_PATH}")
    print(f"org_id:       {config.get('org_id', '?')}")
    print(f"base_url:     {config.get('base_url', '?')}")
    api_key = config.get("api_key", "")
    masked = f"{api_key[:9]}...{api_key[-4:]}" if len(api_key) > 13 else "***"
    print(f"api_key:      {masked}")
    print(f"logged_in_at: {config.get('logged_in_at', '?')}")

    print("\nQuerying /stats...")
    ok, msg = _validate_key(
        config.get("base_url", DEFAULT_BASE_URL),
        config.get("api_key", ""),
        config.get("org_id", ""),
    )
    if ok:
        print(f"graph:        {msg}")
        return 0
    print(f"error: {msg}", file=sys.stderr)
    return 1


def cmd_logout(args: argparse.Namespace) -> int:
    if not CONFIG_PATH.exists():
        print("already logged out.")
        return 0

    if not args.yes:
        try:
            resp = input(f"delete {CONFIG_PATH}? [y/N]: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\naborted.")
            return 1
        if resp not in ("y", "yes"):
            print("aborted.")
            return 1

    try:
        CONFIG_PATH.unlink()
    except OSError as e:
        print(f"error: could not delete {CONFIG_PATH}: {e}", file=sys.stderr)
        return 1
    print(f"deleted {CONFIG_PATH}")
    return 0


# -- Entrypoint --------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="graphory",
        description="Graphory CLI - manage local credentials for the Graphory API.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"graphory {_get_version()}",
    )

    sub = parser.add_subparsers(dest="command")

    p_login = sub.add_parser("login", help="Save your API key locally.")
    p_login.add_argument(
        "--base-url",
        default=None,
        help=f"API base URL (default: {DEFAULT_BASE_URL} or $GRAPHORY_BASE_URL).",
    )
    p_login.set_defaults(func=cmd_login)

    p_status = sub.add_parser("status", help="Show current login + graph stats.")
    p_status.set_defaults(func=cmd_status)

    p_logout = sub.add_parser("logout", help="Delete the local config file.")
    p_logout.add_argument("-y", "--yes", action="store_true", help="Skip confirmation.")
    p_logout.set_defaults(func=cmd_logout)

    return parser


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not getattr(args, "command", None):
        parser.print_help()
        return 1
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
