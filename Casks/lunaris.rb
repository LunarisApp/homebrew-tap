cask "lunaris" do
  version "0.0.3"
  sha256 "1a35837f690917a93fbc74373dae62c1cedad887f32ae92a07cb5dfe3ea54489"

  url "https://github.com/LunarisApp/lunaris/releases/download/v#{version}/" \
      "Lunaris-desktop-#{version}-universal-adhoc.dmg"
  name "Lunaris"
  desc "Offline-first collaborative word processor"
  homepage "https://lunaris.app/"

  depends_on macos: :ventura

  app "Lunaris.app"

  caveats <<~EOS
    This preview build uses ad-hoc code signing. macOS may require explicit
    approval in System Settings > Privacy & Security before first launch.
  EOS
end
