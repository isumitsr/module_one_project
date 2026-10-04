"""Download and verify the M5 competition files from Kaggle.

Run this script from the repository root:

    python scripts/download_data.py

Kaggle requires a user account, acceptance of the competition rules, and an
API token for this competition. See setup.md for the authentication steps.
"""

from __future__ import annotations

import hashlib
import shutil
import tempfile
from pathlib import Path


COMPETITION_SLUG = "m5-forecasting-accuracy"
COMPETITION_URL = "https://www.kaggle.com/competitions/m5-forecasting-accuracy/data"

# These hashes let us detect incomplete or corrupted downloads.
REQUIRED_FILE_HASHES = {
    "calendar.csv": "3ffeab2991b0c8e861d008b39ea4c95c",
    "sales_train_evaluation.csv": "b806dfc9f30a745102b708c09951f6aa",
    "sales_train_validation.csv": "26a366a25beb57b0a8f4c7b148758f94",
    "sample_submission.csv": "c281a69d7c011274899d92020a66e25b",
    "sell_prices.csv": "08c591caa99e55daf3e0ccac913f7c85",
}


def calculate_md5(file_path: Path) -> str:
    """Calculate an MD5 checksum without loading an entire file into memory."""

    checksum = hashlib.md5()
    with file_path.open("rb") as file_handle:
        for block in iter(lambda: file_handle.read(1024 * 1024), b""):
            checksum.update(block)
    return checksum.hexdigest()


def invalid_files(raw_data_dir: Path) -> list[str]:
    """Return required files that are missing, empty, or have the wrong hash."""

    invalid = []
    for file_name, expected_hash in REQUIRED_FILE_HASHES.items():
        file_path = raw_data_dir / file_name
        if not file_path.is_file() or file_path.stat().st_size == 0:
            invalid.append(file_name)
        elif calculate_md5(file_path) != expected_hash:
            invalid.append(file_name)
    return invalid


def ensure_m5_data(raw_data_dir: Path | None = None) -> Path:
    """Ensure verified M5 CSV files exist locally, downloading when necessary."""

    project_root = Path(__file__).resolve().parents[1]
    destination = raw_data_dir or project_root / "data" / "raw"
    destination.mkdir(parents=True, exist_ok=True)

    files_to_download = invalid_files(destination)
    if not files_to_download:
        print("All five M5 files are present and their checksums are valid.")
        return destination

    print("The following M5 files are missing or invalid:")
    for file_name in files_to_download:
        print(f"- {file_name}")
    print(f"Downloading the official competition data from {COMPETITION_URL}")

    try:
        import kagglehub
    except ImportError as error:
        raise RuntimeError(
            "kagglehub is not installed. Run: python -m pip install -r requirements.txt"
        ) from error

    # Download to a temporary directory first so a failed transfer cannot
    # replace a valid file or remove data/raw/README.md.
    try:
        with tempfile.TemporaryDirectory(prefix="m5-kaggle-") as temporary_directory:
            download_directory = Path(temporary_directory)
            kagglehub.competition_download(
                COMPETITION_SLUG,
                output_dir=str(download_directory),
            )

            for file_name, expected_hash in REQUIRED_FILE_HASHES.items():
                matches = list(download_directory.rglob(file_name))
                if len(matches) != 1:
                    raise RuntimeError(
                        f"Expected one downloaded copy of {file_name}, found {len(matches)}."
                    )
                if calculate_md5(matches[0]) != expected_hash:
                    raise RuntimeError(f"Checksum verification failed for {file_name}.")

            for file_name in REQUIRED_FILE_HASHES:
                source_path = next(download_directory.rglob(file_name))
                shutil.copy2(source_path, destination / file_name)
    except Exception as error:
        raise RuntimeError(
            "Kaggle could not download the M5 data. Confirm that you accepted the "
            "competition rules and configured a Kaggle API token as described in setup.md."
        ) from error

    remaining_invalid_files = invalid_files(destination)
    if remaining_invalid_files:
        raise RuntimeError(
            "Download completed, but these files failed verification: "
            + ", ".join(remaining_invalid_files)
        )

    print(f"Download complete. Verified files are available in {destination}")
    return destination


if __name__ == "__main__":
    ensure_m5_data()
