# Changelog
This changelog is inspired by [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [0.3] - 2021-07-14
### Removed
- Removed function *docopt_parsable* and *doctopt* dependency.
- Removed functions *repr_posix_path* and *strip_for_doctest* as being tranfered to
  *doctestprinter*.
  
### Added
- Additional tests
- *overlap_dict_branches* removing the dependency to *dicthandling*

### Fixed
- *overlap_dict_branches* for not raising an error upon non-dictionary entries.
- *load_yaml_file_content* not returning the default dict, if content is 'None'.

## [0.2b3] - 2021-04-22 
### Deprecated
- *docopt_parsable* will be removed in the next release
  as I prioritize *click* for a cli.
  
### Fixed
- Fixed missing requirements

### Added
- __email__ and __author__

## [0.2b2] - 2020-10-10 
### Fixed
- Missing *get_piped_command_line_arguments* in __all__

## [0.2b1] - 2020-20-16
### Fixed
- Bug in which *get_sys_argv_with_piped_args* didn't removed empty 
  strings as intended.

## [0.2b0] - 2020-20-15
### Added
- Method *get_sys_argv_with_piped_args*

### Changed
- Changed project status to beta; tests and docstrings are placed.

## [0.1a1.post4] - 2020-20-14
### Fixed
- Minor bugs related to wrong references and a working read-the-docs 
  configuration.

## [0.1a1] - 2020-10-09
### Changed
- Docstring in remove_tree
- Documentation
- Method *remove_tree* renamed to *remove_path_or_tree*

## [0.1a0] - 2020-10-08 - not released
### Added
- Method *remove_tree* removing a whole path tree (or single file) using 
  pathlib.

## [0.0a1] - 2020-10-07 - not released
### Added
- Pushing `myminions` on gitlab.com
