class Lunaris < Formula
  desc "Native Lunaris control plane CLI and MCP server"
  homepage "https://lunaris.app/"
  url "https://github.com/LunarisApp/lunaris/releases/download/v0.0.7/" \
      "lunaris-cli-0.0.7-universal-apple-darwin.zip"
  sha256 "df2baec7cc89924fdb23ba6391ca23b8d343e8259d9073a88cc46017b420b729"
  license "MIT"

  depends_on macos: :ventura

  def install
    bin.install "lunaris"
    pkgshare.install "LICENSE", "THIRD-PARTY-LICENSES.txt"
  end

  test do
    assert_match version.to_s, shell_output("#{bin}/lunaris --version")
  end
end
