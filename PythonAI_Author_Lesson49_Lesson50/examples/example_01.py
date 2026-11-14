"""Check a deployed public health endpoint; never invokes an LLM."""
import argparse
import json
from urllib.parse import urlsplit
from urllib.request import urlopen


def read_json(base, route):
    parsed = urlsplit(base)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc or parsed.username:
        raise ValueError("Use a site URL without credentials")
    with urlopen(base.rstrip("/") + route, timeout=20) as response:
        return json.load(response)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url", help="Your own site, e.g. https://USER.pythonanywhere.com")
    args = parser.parse_args()
    try:
        data = read_json(args.url, "/api/health")
        if data.get("ok") is not True or not isinstance(data.get("chunks"), int) or data["chunks"] <= 0:
            raise ValueError("Health must have ok=true and chunks > 0")
    except (OSError, ValueError) as exc:
        parser.exit(1, f"FAIL: {exc}\n")
    print(json.dumps({k: data.get(k) for k in ("ok", "chunks", "llm_enabled")}, ensure_ascii=False))
    print("PASS: available index; answer quality is not measured by this check.")


if __name__ == "__main__":
    main()
