#!/usr/bin/env python3
"""Download the official scikit-learn figures used by the time-series deck.

Run from the repository root:
    python3 .agents/scripts/download_series_tiempo_assets.py

The downloaded PNGs are unchanged upstream figures, not local experiments.
Source: scikit-learn, Time-related feature engineering (BSD-3-Clause).
The presentation includes the upstream copyright and license in its notes.
Only this preparation step needs network access; rendering the deck does not.
"""

import argparse
import hashlib
from pathlib import Path
import sys
from urllib.error import URLError
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "quarto" / "series_tiempo" / "figures"
BASE = "https://scikit-learn.org/stable/_images/"
FIGURES = {
    "weekly_demand.png": (
        "sphx_glr_plot_cyclical_feature_engineering_001.png",
        "446848e66e96d4078ef03b72a36dcbc4a38c858dcb225b2b91eac59f5c0e3ddb",
    ),
    "hour_circle.png": (
        "sphx_glr_plot_cyclical_feature_engineering_004.png",
        "54d23e1a717cecf1d7e1671f492eb382cf8800a48a6cd18350e8c87f10bb66b5",
    ),
    "periodic_splines.png": (
        "sphx_glr_plot_cyclical_feature_engineering_005.png",
        "b90da364bdab6949e81c2962fee53bb42b261a019b2b9571c9d680c9f53b1090",
    ),
    "linear_predictions.png": (
        "sphx_glr_plot_cyclical_feature_engineering_006.png",
        "4ae380b05ee8ba8649be9367014d029206d5a5a22c7fcc902f575957ae338db7",
    ),
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Verify local files without network")
    args = parser.parse_args()
    if not args.check:
        OUTPUT.mkdir(parents=True, exist_ok=True)
    try:
        for name, (remote, expected) in FIGURES.items():
            target = OUTPUT / name
            if args.check:
                data = target.read_bytes()
            else:
                request = Request(BASE + remote, headers={"User-Agent": "course-slides-assets/1.0"})
                with urlopen(request, timeout=45) as response:
                    data = response.read()
            if not data.startswith(b"\x89PNG\r\n\x1a\n"):
                raise ValueError(f"{name}: the response is not a PNG")
            digest = hashlib.sha256(data).hexdigest()
            if expected and digest != expected:
                raise ValueError(f"{name}: SHA-256 mismatch; inspect upstream before updating the pin")
            if not args.check:
                temporary = target.with_suffix(".download")
                temporary.write_bytes(data)
                temporary.replace(target)
            print(f"{name}: {len(data)} bytes, sha256={digest}")
    except (OSError, URLError, ValueError) as error:
        print(f"Asset preparation failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
