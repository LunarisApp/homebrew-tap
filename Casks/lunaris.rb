cask "lunaris" do
  version "0.0.6"
  sha256 "abe20f8f7898425e13109463c45ee7a6823abb8d95382652ceb7c829534d4f62"

  url "https://github.com/LunarisApp/lunaris/releases/download/v#{version}/" \
      "Lunaris-desktop-#{version}-universal.dmg"
  name "Lunaris"
  desc "Offline-first collaborative word processor"
  homepage "https://lunaris.app/"

  depends_on macos: :ventura

  app "Lunaris.app"
end
