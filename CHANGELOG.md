# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog][keepachangelog] and this project
adheres to [Semantic Versioning][semver].

## [Unreleased][unreleased]

## [v0.11.0][v0.11.0] - 2018-02-16
### Added
- Made redirect URI, token file name and token path configurable via
  environment variables. (#14)
- Added Monzo Pots API endpoint - thanks @Sheaffy! (#13)

### Changed
- Renamed `config.PYMONZO_REDIRECT_URI` to `config.REDIRECT_URI`.

## [v0.10.3][v0.10.3] - 2017-10-15
### Fixed
- Fixed saving token file to disk. (#9)

## [v0.10.2][v0.10.2] - 2017-10-05
### Fixed
- Fixed automatic token refreshing - thanks @bartonp! (#5)

### Changed
- `MonzoAPI()._refresh_oath_token()` now doesn't return anything, replaces
  current token and raises `CantRefreshTokenError` when token couldn't be
  refreshed.
- Client secret is now saved in token file JSON file.
- Cleaned up exceptions.

## [v0.10.1][v0.10.1] - 2017-09-24
### Fixed
- Try to refresh token if API request returned HTTP 401 (which could mean that
  the token is expired). (#6)

## [v0.10.0][v0.10.0] - 2017-09-22
### Changed
 - Changed token file format from `shelve` to JSON. Because of that the file
   will need to be regenerated. (#3)
 - Updated `six` library to version 1.11.0.

## [v0.9.1][v0.9.1] - 2017-09-21
### Deprecated
 - Added deprecation warning about changing token file format from `shelve`
   to JSON in next release. Because of that the file will need to be
   regenerated. (#4)

## [v0.9.0][v0.9.0] - 2017-09-17
### Added
- Started keeping a changelog.

### Changed
- Major test suite overhaul.
- Code cleanup.


[keepachangelog]: http://keepachangelog.com/en/1.0.0/
[semver]: http://semver.org/spec/v2.0.0.html
[unreleased]: https://github.com/pawelad/pymonzo/compare/v0.11.0...HEAD
[v0.9.0]: https://github.com/pawelad/pymonzo/releases/tag/v0.9.0
[v0.9.1]: https://github.com/pawelad/pymonzo/releases/tag/v0.9.1
[v0.10.0]: https://github.com/pawelad/pymonzo/releases/tag/v0.10.0
[v0.10.1]: https://github.com/pawelad/pymonzo/releases/tag/v0.10.1
[v0.10.2]: https://github.com/pawelad/pymonzo/releases/tag/v0.10.2
[v0.10.3]: https://github.com/pawelad/pymonzo/releases/tag/v0.10.3
[v0.11.0]: https://github.com/pawelad/pymonzo/releases/tag/v0.11.0
