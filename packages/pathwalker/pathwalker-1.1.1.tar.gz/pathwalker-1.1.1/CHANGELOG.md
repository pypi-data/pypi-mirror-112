# Changelog
This changelog is inspired by [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).


## [1.1.1] - 2021-07-13
### Fixed
- Fixed links related to renaming the *master* branch to *release*.

## [1.1.0] - 2021-07-13
### Added
- Added function *path_is_relative_to* as substitute for the 
  *pathlib.Path.is_relative_to()* in Python 3.9. If python 3.9 is used than the 
  pathlib.Path.is_relative_to() method will be used.

- Added function *keep_root_paths* which will keep the unique root paths within a list
  of paths.
  
- Added tests.

## [1.0.0] - unreleased
Start of pathwalker.
