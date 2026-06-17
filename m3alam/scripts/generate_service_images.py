from __future__ import annotations

import argparse
import base64
import json
import sys
from pathlib import Path
from urllib import error, request

ROOT_DIR = Path(__file__).resolve().parents[2]
APP_DIR = Path(__file__).resolve().parents[1]
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))
DEFAULT_ENV_PATH = ROOT_DIR / ".env"
DEFAULT_OUTPUT_DIR = Path(__file__).resolve().parents[1] / "static" / "images" / "services"
DEFAULT_DEPLOYMENT = "gpt-image-2"
DEFAULT_API_VERSION = "2024-02-01"
SAMPLE_SERVICES = ["ascenseurs", "carrelage", "clim-et-froid", "plomberie", "vitrerie-aluminium"]


def load_dotenv(env_path: Path) -> dict[str, str]:
    if not env_path.exists():
        raise FileNotFoundError(f".env not found: {env_path}")
    values: dict[str, str] = {}
    for raw in env_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip("'\"")
    return values


def parse_services_selection(selection: str, available: set[str]) -> list[str]:
    if selection == "sample":
        return SAMPLE_SERVICES
    if selection == "all":
        return sorted(available)
    selected = [part.strip() for part in selection.split(",") if part.strip()]
    unknown = [item for item in selected if item not in available]
    if unknown:
        raise ValueError(f"Unknown services: {unknown}")
    return selected


def build_prompt(slug: str, label: str) -> str:
    return (
        "3D isometric professional illustration for a premium home-services marketplace card. "
        "Square composition 1024x1024, centered subject with safe margins, clean light background, "
        "no text, modern realistic materials and lighting. "
        f"Service to depict: {label} (slug: {slug})."
    )


def request_image(endpoint: str, api_key: str, deployment: str, api_version: str, prompt: str) -> dict[str, object]:
    url = f"{endpoint.rstrip('/')}/openai/deployments/{deployment}/images/generations?api-version={api_version}"
    payload = {
        "prompt": prompt,
        "size": "1024x1024",
        "quality": "medium",
        "output_format": "png",
        "output_compression": 100,
        "n": 1,
    }
    req = request.Request(
        url=url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "api-key": api_key},
        method="POST",
    )
    with request.urlopen(req, timeout=300) as response:
        return json.loads(response.read().decode("utf-8"))


def decode_image(response_json: dict[str, object]) -> bytes:
    data = response_json.get("data")
    if not isinstance(data, list) or not data:
        raise ValueError("Invalid image API response: missing data")
    item = data[0]
    if not isinstance(item, dict) or "b64_json" not in item:
        raise ValueError("Invalid image API response: missing b64_json")
    return base64.b64decode(item["b64_json"])


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate M3alam service images via GPT-Image-2.")
    parser.add_argument("--env-file", default=str(DEFAULT_ENV_PATH))
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    parser.add_argument("--services", default="sample", help="sample | all | comma-separated slugs")
    parser.add_argument("--deployment", default=DEFAULT_DEPLOYMENT)
    parser.add_argument("--api-version", default=DEFAULT_API_VERSION)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def main() -> int:
    from jobs.service_catalog import SERVICE_CATEGORIES

    args = parse_args()
    env = load_dotenv(Path(args.env_file))
    endpoint = env.get("AZURE_OPENAI_ENDPOINT", "").strip()
    api_key = env.get("AZURE_OPENAI_API_KEY", "").strip()
    if not endpoint or not api_key:
        raise ValueError("AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_API_KEY are required in .env")

    catalog = dict(SERVICE_CATEGORIES)
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    selected = parse_services_selection(args.services, set(catalog.keys()))
    manifest: list[dict[str, str]] = []

    for slug in selected:
        label = catalog[slug]
        prompt = build_prompt(slug, label)
        image_path = output_dir / f"{slug}.png"
        prompt_path = output_dir / f"{slug}.prompt.txt"
        metadata_path = output_dir / f"{slug}.json"

        if image_path.exists() and not args.overwrite:
            manifest.append({"service": slug, "status": "skipped", "image_path": str(image_path)})
            continue

        prompt_path.write_text(prompt, encoding="utf-8")
        if args.dry_run:
            manifest.append({"service": slug, "status": "dry-run", "image_path": str(image_path)})
            continue

        try:
            response = request_image(endpoint, api_key, args.deployment, args.api_version, prompt)
            image_bytes = decode_image(response)
            image_path.write_bytes(image_bytes)
            metadata_path.write_text(json.dumps(response, indent=2), encoding="utf-8")
            manifest.append({"service": slug, "status": "generated", "image_path": str(image_path)})
            print(f"Generated: {slug}")
        except (error.HTTPError, error.URLError, ValueError) as exc:
            manifest.append({"service": slug, "status": "error", "error": str(exc)})
            print(f"ERROR {slug}: {exc}", file=sys.stderr)

    (output_dir / "manifest.json").write_text(json.dumps({"results": manifest}, indent=2), encoding="utf-8")
    return 0 if all(item["status"] != "error" for item in manifest) else 1


if __name__ == "__main__":
    raise SystemExit(main())
