#!/usr/bin/env python3
"""Pin both Homebrew packages to verified assets from a published GitHub release."""

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile

REPOSITORY = "LunarisApp/lunaris"
ROOT = Path(__file__).resolve().parents[1]
PACKAGES = {
    "Formula/lunaris.rb": "lunaris-cli-{version}-universal-apple-darwin{suffix}.zip",
    "Casks/lunaris.rb": "Lunaris-desktop-{version}-universal{suffix}.dmg",
}


def gh(*args):
    return subprocess.check_output(["gh", *args], text=True)


def version_tuple(version):
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        raise ValueError(f"Expected a stable version, got {version!r}")
    return tuple(map(int, version.split(".")))


def render(current, version, checksum, adhoc, formula):
    old_version = re.search(r'^  version "([^"]+)"$', current, re.MULTILINE)
    if old_version is None and formula:
        old_version = re.search(r"releases/download/v(\d+\.\d+\.\d+)/", current)
    if old_version is None:
        raise ValueError("Missing package version")
    if version_tuple(version) < version_tuple(old_version[1]):
        raise ValueError(f"Refusing downgrade from {old_version[1]} to {version}")
    current = current.replace(old_version[1], version)
    result = re.sub(r'^  version "[^"]+"$', f'  version "{version}"', current, flags=re.MULTILINE)
    result = re.sub(r'^  sha256 "[a-f0-9]{64}"$', f'  sha256 "{checksum}"', result, flags=re.MULTILINE)
    result = re.sub(r"(?:-adhoc)?\.(zip|dmg)\"", lambda m: ("-adhoc" if adhoc else "") + f'.{m[1]}"', result)
    # Signing can change between releases; keep caveats consistent with the selected asset.
    result = re.sub(r"\n  def caveats\n.*?\n  end\n", "", result, flags=re.DOTALL)
    result = re.sub(r"\n  caveats <<~EOS\n.*?\n  EOS\n", "", result, flags=re.DOTALL)
    if adhoc:
        if formula:
            caveat = '''  def caveats
    <<~EOS
      This preview build uses ad-hoc code signing. macOS may require explicit
      approval in System Settings > Privacy & Security before first use.
    EOS
  end

'''
            result = result.replace("  test do\n", caveat + "  test do\n")
        else:
            caveat = '''
  caveats <<~EOS
    This preview build uses ad-hoc code signing. macOS may require explicit
    approval in System Settings > Privacy & Security before first launch.
  EOS
'''
            result = result.removesuffix("end\n") + caveat + "end\n"
    return result


def update(tag=None, root=ROOT):
    release = json.loads(gh("release", "view", *([tag] if tag else []), "--repo", REPOSITORY,
                            "--json", "tagName,isDraft,isPrerelease,assets"))
    if release["isDraft"] or release["isPrerelease"]:
        raise ValueError("Only published stable releases can update the tap")
    tag = release["tagName"]
    if not tag.startswith("v"):
        raise ValueError(f"Unexpected release tag: {tag}")
    version = tag[1:]
    version_tuple(version)
    assets = {asset["name"] for asset in release["assets"]}
    selected = []
    for path, pattern in PACKAGES.items():
        signed = pattern.format(version=version, suffix="")
        adhoc = pattern.format(version=version, suffix="-adhoc")
        name = signed if signed in assets else adhoc
        if name not in assets:
            raise ValueError(f"Missing release asset: {signed} or {adhoc}")
        selected.append((path, name, name == adhoc))
    pending = {}
    with tempfile.TemporaryDirectory() as directory:
        gh("release", "download", tag, "--repo", REPOSITORY, "--dir", directory,
           "--pattern", "SHA256SUMS", *[arg for _, name, _ in selected for arg in ("--pattern", name)])
        checksums = {}
        for line in (Path(directory) / "SHA256SUMS").read_text().splitlines():
            checksum, name = line.split(maxsplit=1)
            name = name.lstrip("*")
            if not re.fullmatch(r"[a-f0-9]{64}", checksum) or name in checksums:
                raise ValueError("Invalid or duplicate checksum entry")
            checksums[name] = checksum
        for path, name, adhoc in selected:
            with (Path(directory) / name).open("rb") as artifact:
                checksum = hashlib.file_digest(artifact, "sha256").hexdigest()
            if checksums.get(name) != checksum:
                raise ValueError(f"Checksum mismatch: {name}")
            pending[path] = render((root / path).read_text(), version, checksum, adhoc, path.startswith("Formula/"))
    # Prepare and validate both definitions before changing either file.
    for path, content in pending.items():
        (root / path).write_text(content)
    print(f"Updated CLI and desktop to {tag}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tag", nargs="?", help="Published vX.Y.Z tag (default: latest stable release)")
    update(parser.parse_args().tag)
