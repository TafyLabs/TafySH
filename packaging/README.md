# TafySH Packaging & Distribution

This directory contains packaging configurations for distributing TafySH across various platforms and package managers.

## Quick Install

### Universal (curl/wget)

```bash
# curl
curl -fsSL https://get.tafysh.dev | bash

# wget
wget -qO- https://get.tafysh.dev | bash

# With options
curl -fsSL https://get.tafysh.dev | TAFYSH_VERSION=0.1.0 bash
curl -fsSL https://get.tafysh.dev | TAFYSH_SET_DEFAULT_SHELL=1 bash
```

### macOS (Homebrew)

```bash
brew tap tafysh/tap
brew install tafysh
```

### Debian/Ubuntu (APT)

```bash
curl -fsSL https://pkg.tafysh.dev/gpg.key | sudo gpg --dearmor -o /usr/share/keyrings/tafysh-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/tafysh-archive-keyring.gpg] https://pkg.tafysh.dev/apt stable main" | sudo tee /etc/apt/sources.list.d/tafysh.list
sudo apt update
sudo apt install tafysh
```

### Fedora/RHEL (DNF)

```bash
sudo curl -fsSL https://pkg.tafysh.dev/rpm/tafysh.repo -o /etc/yum.repos.d/tafysh.repo
sudo dnf install tafysh
```

### Arch Linux (AUR)

```bash
# Via yay
yay -S tafysh

# Via paru
paru -S tafysh

# Manual
git clone https://aur.archlinux.org/tafysh.git
cd tafysh
makepkg -si
```

### Alpine Linux

```bash
# Add repository
echo "https://pkg.tafysh.dev/alpine/edge/main" >> /etc/apk/repositories
apk update
apk add tafysh
```

### Python (pip/pipx/uv)

```bash
# pip (system)
pip install tafysh

# pipx (isolated)
pipx install tafysh

# uv (fastest)
uv tool install tafysh
```

### Docker

```bash
# Standard image
docker run -it --rm -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY ghcr.io/tafysh/tafysh

# Alpine (minimal)
docker run -it --rm -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY ghcr.io/tafysh/tafysh:alpine

# With Ollama (local LLM)
docker-compose up -d ollama tafysh-local
```

### Windows (PowerShell)

```powershell
irm https://get.tafysh.dev/windows | iex
```

## Package Contents

### `homebrew/`
- `tafysh.rb` - Homebrew formula for macOS

### `debian/`
- `control` - Package metadata
- `rules` - Build rules
- `changelog` - Version history
- `copyright` - License information
- `postinst` - Post-installation script (adds to /etc/shells)
- `postrm` - Post-removal script (removes from /etc/shells)

### `rpm/`
- `tafysh.spec` - RPM spec file for Fedora/RHEL/CentOS

### `arch/`
- `PKGBUILD` - Arch Linux build script
- `tafysh.install` - Install hooks

### `alpine/`
- `APKBUILD` - Alpine Linux build script

### `docker/`
- `Dockerfile` - Standard Debian-based image
- `Dockerfile.alpine` - Minimal Alpine image
- `Dockerfile.dev` - Development image
- `docker-compose.yml` - Multi-container setup with Ollama
- `docker-entrypoint.sh` - Container entrypoint

### `windows/`
- `install.ps1` - PowerShell installer
- `README.md` - Windows-specific instructions

## Building Packages

### Debian Package

```bash
# Install build dependencies
sudo apt install debhelper dh-python python3-all python3-setuptools

# Build
dpkg-buildpackage -us -uc -b
```

### RPM Package

```bash
# Install build dependencies
sudo dnf install rpm-build python3-devel python3-setuptools

# Build
rpmbuild -ba packaging/rpm/tafysh.spec
```

### Arch Package

```bash
cd packaging/arch
makepkg -s
```

### Docker Images

```bash
cd packaging/docker
docker build -t tafysh:latest -f Dockerfile ../..
docker build -t tafysh:alpine -f Dockerfile.alpine ../..
```

## Shell Completions

Shell completion scripts are installed automatically by package managers. For manual installation:

```bash
# Bash
cp completions/tafysh.bash /usr/share/bash-completion/completions/tafysh

# Zsh
cp completions/tafysh.zsh /usr/share/zsh/site-functions/_tafysh

# Fish
cp completions/tafysh.fish ~/.config/fish/completions/tafysh.fish
```

## Setting as Default Shell

After installation, TafySH can be set as your default login shell:

```bash
# Add to /etc/shells (done automatically by packages)
echo "$(which tafysh)" | sudo tee -a /etc/shells

# Set as default
chsh -s $(which tafysh)
```

## Release Process

1. Update version in `pyproject.toml`
2. Update `packaging/debian/changelog`
3. Update `packaging/rpm/tafysh.spec` version
4. Update `packaging/arch/PKGBUILD` version
5. Update `packaging/alpine/APKBUILD` version
6. Build and test packages
7. Push to PyPI: `python -m build && twine upload dist/*`
8. Create GitHub release
9. Push to package repositories

## Infrastructure

For production deployment, set up:

1. **Package hosting** (pkg.tafysh.dev)
   - APT repository with GPG signing
   - RPM repository
   - Alpine repository

2. **Installer hosting** (get.tafysh.dev)
   - Redirect to `scripts/install.sh`
   - `/windows` redirect to `packaging/windows/install.ps1`

3. **Docker registry** (ghcr.io/tafysh/tafysh)
   - Multi-arch builds (amd64, arm64)
   - Tags: latest, alpine, dev, version numbers

4. **Homebrew tap** (github.com/tafysh/homebrew-tap)
   - Formula auto-updated on release
