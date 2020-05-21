{ pkgs ? import <nixpkgs> {} }:
with pkgs;

stdenv.mkDerivation rec {
  name = "env";
  env = buildEnv { name = name; paths = buildInputs; };
  buildInputs = [
    # python
    (python35.withPackages (ps: with ps; [ virtualenv pip pytest future ]))
  ];
}
