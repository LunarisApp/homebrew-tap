class Lunaris < Formula
  desc "Native Lunaris control plane CLI and MCP server"
  homepage "https://lunaris.app/"
  url "https://github.com/LunarisApp/lunaris/releases/download/v0.0.6/" \
      "lunaris-cli-0.0.6-universal-apple-darwin.zip"
  sha256 "404da00e5a2cecfe09cc6b577e739df61aca39e2d37766af64bd127a85126419"
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
