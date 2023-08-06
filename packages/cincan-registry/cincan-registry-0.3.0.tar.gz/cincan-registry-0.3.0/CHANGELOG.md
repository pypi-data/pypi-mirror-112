# Changelog

All notable changes in project will be documented in here.

## [0.3.0]

### Changed

  * Major change - use SQLite3 database instead of cache files for all storage
  * Version history is tracked now
  * Performance improvements

## [0.2.0]

### Added

  * Added support for Quay Registry
  * Added support for V2 manifest specification. Used as default
  * Use time to measure validity of cached meta files
  * Namespace of registry is "dynamic". It is easier to add possible new registries

### Changed

  * Use Quay Registry as default instead of Docker Hub. Docker Hub remains optional and supported
  * Structure of the code revamped for more modular
  * Listing uses only the name of the tool instead of full image name including registry path
  * Configuration file uses yaml format

### Removed

  * Manifest V1 support

## [0.1.2]

### Changed

  * Changes related to structure change of 'tools' repository. Index file is used now for tools path. README and metafiles are used now correctly.

## [0.1.1]

### Changed

  - Default stable tag is now 'latest' instead of 'latest-stable'

## [0.1.0]

### Changed

 * GitLab utils reworked to use official Python API Client
 * Many bug fixes
### Added

 * Less error prone cache
 * Many tests

## [0.1.0-rc6]

### Changed

 * Bugfixes
 * Registry fetch optimized - only required tools

## [0.1.0-rc5]

### Changed

   * Many bugfixes

## [0.1.0-rc4]

### Added
 * Added feature to automatically update READMEs of Docker Hub tools based on GitLab
 * Optimized caching and downloading of metafiles from GitLab
 * Better structure for importing tool as module
## [0.1.0-rc3]

### Changed
- Using master branch of tools' repository now

## [0.1.0-rc2]

### Added

- Works as external module now without main function 
- Option to refresh cache manually

## [0.1.0-rc1]

### Added
- First release candidate


