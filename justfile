[windows]
init:
    winget install Microsoft.VisualStudio.2022.BuildTools
    winget install --id Rustlang.Rustup
    winget install OpenJS.NodeJS
    winget install pnpm.pnpm
    winget install astral-sh.uv
    cargo install killport
    pnpm install

[macos]
init:
    xcode-select --install
    curl --proto '=https' --tlsv1.2 https://sh.rustup.rs -sSf | sh
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    brew install node
    brew install pnpm
    brew install uv
    brew install killport
    pnpm install

dev:
    -killport 1420 5100
    -rm -rf ./api/.venv
    pnpm run tauri dev

build:
    -killport 1420 5100
    -rm -rf ./api/.venv
    pnpm run tauri build

api:
    cd api; uv run fastapi dev --port 5100

api-format:
    cd api; ruff format .