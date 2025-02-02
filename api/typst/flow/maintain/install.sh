#!/usr/bin/env nix-shell
#!nix-shell -i bash -p bash tomlq
set -eu
source `dirname $0`/common

target="$HOME/.local/share/typst/packages/${1:-local}/flow/$version"

mkdir -p `dirname "$target"`
rm -rf "$target"
cp -r "$repo" "$target"
