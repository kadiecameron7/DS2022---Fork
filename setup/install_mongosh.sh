#!/usr/bin/env bash
# Install mongosh into ~/.local/bin (no sudo). Used by Option C in setup/mongodb.md.
set -euo pipefail

MONGOSH_VERSION="${MONGOSH_VERSION:-2.12.0}"
BIN_DIR="${HOME}/.local/bin"
LIB_DIR="${HOME}/.local/lib"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

arch="$(uname -m)"
case "$arch" in
  x86_64|amd64) asset="mongosh-${MONGOSH_VERSION}-linux-x64.tgz" ;;
  aarch64|arm64) asset="mongosh-${MONGOSH_VERSION}-linux-arm64.tgz" ;;
  *)
    echo "Unsupported CPU architecture: $arch" >&2
    exit 1
    ;;
esac

url="https://github.com/mongodb-js/mongosh/releases/download/v${MONGOSH_VERSION}/${asset}"
echo "Downloading ${asset} ..."
curl -fsSL -o "${TMP_DIR}/mongosh.tgz" "$url"
tar -xzf "${TMP_DIR}/mongosh.tgz" -C "$TMP_DIR"

extracted="$(find "$TMP_DIR" -maxdepth 1 -type d -name "mongosh-${MONGOSH_VERSION}-linux-*" | head -n 1)"
if [ -z "$extracted" ] || [ ! -x "${extracted}/bin/mongosh" ]; then
  echo "Could not find mongosh binary in the download." >&2
  exit 1
fi

mkdir -p "$BIN_DIR" "$LIB_DIR"
install -m 0755 "${extracted}/bin/mongosh" "${BIN_DIR}/mongosh"
if [ -f "${extracted}/bin/mongosh_crypt_v1.so" ]; then
  install -m 0644 "${extracted}/bin/mongosh_crypt_v1.so" "${LIB_DIR}/mongosh_crypt_v1.so"
fi

path_line='export PATH="$HOME/.local/bin:$PATH"'
bashrc="${HOME}/.bashrc"
if [ -f "$bashrc" ] && grep -Fqx "$path_line" "$bashrc"; then
  :
elif [ -f "$bashrc" ]; then
  {
    echo ""
    echo "# mongosh (DS2022 setup/install_mongosh.sh)"
    echo "$path_line"
  } >> "$bashrc"
  echo "Added ~/.local/bin to PATH in ~/.bashrc"
else
  {
    echo "# mongosh (DS2022 setup/install_mongosh.sh)"
    echo "$path_line"
  } > "$bashrc"
  echo "Created ~/.bashrc and added ~/.local/bin to PATH"
fi

export PATH="${BIN_DIR}:$PATH"
echo "Installed: $(command -v mongosh)"
mongosh --version
echo
echo "Next (this terminal): source ~/.bashrc"
echo "Or open a new terminal, then run: mongosh --version"
