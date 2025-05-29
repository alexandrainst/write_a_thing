# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).


## [Unreleased]
### Changed
- Updated prompt to encourage more clarifying questions.


## [v0.3.0] - 2025-05-28
### Added
- Added option for the agent to open the generated Word documents.
- Added ability to broadcast messages to the user.


## [v0.2.0] - 2025-05-26
### Added
- Now automatically stores documents in version-indexed files, when the file already
  exists.
- Added extra tools related to counting the length of the generated text.
- Added `--temperature` option to control the randomness of the generated text. This now
  defaults to 0.0.

### Changed
- Prompt improvements.

### Fixed
- Correctly detects location of `.env` file in the current working directory.
- Disables logging from other packages to avoid cluttering the output.


## [v0.1.0] - 2025-05-26
### Added
- Initial release of the project.
