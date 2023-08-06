# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0](https://pypi.org/project/myst/0.0.1/) - PRERELEASE

### Added

- New API routes and endpoints for deletion
- API routes and endpoints for policies and project results

### Changed

- Re-factored client generation to be compatible with python packaging

## [0.0.1](https://pypi.org/project/myst/0.0.1/) - 2021-07-07

This is the initial `myst-alpha` release.

### Added

- Authentication via Google credentials
- Interact with [Myst's](https://myst.ai) `v1aphla2` API via auto-generated OpenAPI client
- Initial (concealed) CLI via `typer`
- Tested using `pytest` and matrix tests via Github Actions
