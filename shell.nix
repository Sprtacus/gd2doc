# shell.nix
{ pkgs ? import <nixpkgs> {} }:
pkgs.mkShell {
  # System-Pakete und Python-Pakete für die Entwickler-Umgebung
  buildInputs = with pkgs; [
    python39
    python39Packages.click
    python39Packages.jinja2
    python39Packages.pytest
    # Weitere Tools nach Bedarf
    git
  ];

  # Optionale Umgebungs-Variablen
  shellHook = ''
    export LANG="en_US.UTF-8"
    export PIP_CACHE_DIR="$HOME/.cache/pip"
  '';
}