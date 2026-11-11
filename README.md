# LunarisApp Tap

Homebrew Formula and Cask definitions maintained by LunarisApp.

## Installation

Tap and trust the repository:

```sh
brew tap LunarisApp/tap
brew trust --tap LunarisApp/tap
```

Install Lunaris CLI:

```sh
brew install LunarisApp/tap/lunaris
```

Install Lunaris Desktop:

```sh
brew install --cask LunarisApp/tap/lunaris
```

Upgrade either package:

```sh
brew upgrade LunarisApp/tap/lunaris
brew upgrade --cask LunarisApp/tap/lunaris
```

Uninstall either package:

```sh
brew uninstall LunarisApp/tap/lunaris
brew uninstall --cask LunarisApp/tap/lunaris
```

In a `Brewfile`:

```ruby
tap "LunarisApp/tap"
brew "LunarisApp/tap/lunaris"
cask "LunarisApp/tap/lunaris"
```

## Releases

Both packages download directly from [Lunaris GitHub Releases](https://github.com/LunarisApp/lunaris/releases).
The CLI formula installs the prebuilt universal macOS binary; the desktop cask
installs `Lunaris.app` from the universal DMG. Both support Apple Silicon and Intel
Macs running macOS Ventura or newer. No local compilation is required.

`Formula/lunaris.rb` and `Casks/lunaris.rb` pin the release version and SHA-256.
The update workflow checks the latest published stable release every six hours
and opens a pull request updating both definitions. Drafts and prereleases are
excluded. Signed assets are preferred, with ad-hoc assets used when necessary.
Each download is verified against the release's `SHA256SUMS` before either
definition is changed. CI runs formula checks and verifies the cask download.

### Enable automatic updates

Add the `HOMEBREW_TAP_TOKEN` repository secret with **Contents: read/write** and
**Pull requests: read/write** access to this tap, plus read access to the public
Lunaris releases. The workflow uses this token so its pull requests trigger CI.
Merge successful update pull requests to publish them to Homebrew users.

Configure this secret on **LunarisApp/homebrew-tap** only. Keep the older
Lunaris-side Homebrew publisher disabled by leaving `HOMEBREW_TAP_TOKEN` unset
on **LunarisApp/lunaris**. Its stable release workflow enables that publisher
when the secret exists; it currently generates website download URLs and would
compete with the GitHub-based definitions maintained here.

To update locally with Python 3.11+ and an authenticated GitHub CLI:

```sh
python3 scripts/update-release.py          # latest published stable release
python3 scripts/update-release.py v0.0.3   # a specific release; downgrades refused
```

The **Update Lunaris release** workflow also accepts an optional release tag
through **Run workflow**. Both macOS artifacts and `SHA256SUMS` must exist on the
selected release.

Preview releases may use ad-hoc Apple code signing. Their Formula or Cask
prints a warning because macOS may require explicit approval in
**System Settings > Privacy & Security** before first use.
