# Atlas Orchestration Team

This folder currently acts as a **distribution metadata shell** for the Atlas orchestration pack.

## Current Status

- The default-active runtime for this clone is `.github/agents`.
- This folder does **not** currently ship an `agents/` directory.
- As a result, this pack is **not** an activatable standalone source in the current checkout.

## What Atlas Runtime Means Here

The live orchestration surface in this clone is rooted in `.github/agents` and currently centers on:

- `Atlas`
- `Prometheus`
- `Hermes-subagent`
- `Oracle-subagent`
- `Sisyphus-subagent`
- `Afrodita-subagent`
- `Themis Subagent`
- `Argus - QA Testing Subagent`
- `HEPHAESTUS`

Optional governance lanes such as `Atenea`, `Ariadna`, and `Clio` remain shipped as root agent definitions, but they are not required for the stable default path.

## Purpose Of This Folder

- retain repository structure for future plugin/distribution work
- document the intended Atlas orchestration pack boundary
- provide a stable place for pack-level README/marketplace metadata

## Contributor Guidance

For this clone, edit `.github/agents` when changing live Atlas behavior.

If a real plugin copy of the Atlas pack is reintroduced later, this folder can become the sync source again — but that is **not** the current state.
