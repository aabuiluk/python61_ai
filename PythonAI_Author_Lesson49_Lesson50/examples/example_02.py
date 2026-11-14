"""Check that a specific corpus marker is retrievable; no LLM call."""
import argparse
import json
from urllib.parse import urlencode, urlsplit
from urllib.request import urlopen


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url")
    parser.add_argument("--marker", default="СОНЯХ-61")
    args = parser.parse_args()
    try:
        parsed = urlsplit(args.url)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc or parsed.username:
            raise ValueError("Use a site URL without credentials")
        if not args.marker.strip():
            raise ValueError("Marker cannot be empty")
        url = args.url.rstrip("/") + "/api/search?" + urlencode({"q": args.marker})
        with urlopen(url, timeout=20) as response:
            data = json.load(response)
        matches = [r for r in data.get("results", []) if args.marker.casefold() in r.get("text", "").casefold()]
        if not matches:
            raise ValueError("Marker not found. Check deploy, index rebuild and uploaded overrides.")
    except (OSError, ValueError, TypeError) as exc:
        parser.exit(1, f"FAIL: {exc}\n")
    for result in matches:
        print(json.dumps({k: result.get(k) for k in ("id", "path", "score")}, ensure_ascii=False))
    print("PASS: marker found in retrieved passage. This is not a full RAG evaluation.")


if __name__ == "__main__":
    main()
