class Lunaris < Formula
  desc "Native Lunaris control plane CLI and MCP server"
  homepage "https://lunaris.app/"
  url "https://github.com/LunarisApp/lunaris/releases/download/v0.0.3/" \
      "lunaris-cli-0.0.3-universal-apple-darwin-adhoc.zip"
  sha256 "7eb8b80bf71b12b34fbd12eb3fd59b87119008336a6f6c4f6227a0daf6df63b3"
  license "MIT"

  depends_on macos: :ventura

  def install
    bin.install "lunaris"
    pkgshare.install "LICENSE", "THIRD-PARTY-LICENSES.txt"
  end

  def caveats
    <<~EOS
      This preview build uses ad-hoc code signing. macOS may require explicit
      approval in System Settings > Privacy & Security before first use.
    EOS
  end

  test do
    assert_match version.to_s, shell_output("#{bin}/lunaris --version")
  end
end
