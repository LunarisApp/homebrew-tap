cask "lunaris" do
  version "0.0.7"
  sha256 "63efaedb258107e78d2d4cbc499c404bac4a241e59fcf749dac9412f61c91eff"

  url "https://github.com/LunarisApp/lunaris/releases/download/v#{version}/" \
      "Lunaris-desktop-#{version}-universal.dmg"
  name "Lunaris"
  desc "Offline-first collaborative word processor"
  homepage "https://lunaris.app/"

  depends_on macos: :ventura

  app "Lunaris.app"
end
