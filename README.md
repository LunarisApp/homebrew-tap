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

Lunaris release automation updates `Formula/lunaris.rb` and
`Casks/lunaris.rb`. Each update is tested by `brew test-bot` before merge.
Versioned downloads and SHA-256 checksums are pinned to the matching Lunaris
release.

Preview releases may use ad-hoc Apple code signing. Their Formula or Cask
prints a warning because macOS may require explicit approval in
**System Settings > Privacy & Security** before first use.
