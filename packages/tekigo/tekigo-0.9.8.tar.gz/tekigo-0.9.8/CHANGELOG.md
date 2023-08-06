# Changelog

All notable changes to this project will be documented in this file.
The format is based on Keep a Changelog,
and this project adheres to Semantic Versioning.

## [0.9.8] 2021 / 7 / 12

### Added

- render tekigo compatible with python 3.6 and hdfdict related version

### Changed

- VERSION for release
- update LICENCE
- Periodic adaptation deactivated by default

### Fixed

- Adapted different examples with latest tekigo capabilities

### Deprecated

[ - ]


## [0.9.7] 2021 / 6 / 2

### Added

- pytest front add success checks in log output test raw
- pytest front add success check in log output test refine
- hdfdict requirement in setup.py

### Changed

- Allow refinement to work in 2D with triangular cells

### Fixed

- Fixing problem in dealing with "Adapt" group if already present
- adapt test front to periodic adaptation default deactivation

### Deprecated

[ - ]

## [0.9.6] 2021 / 2 / 16

### Added
 
 - add option to deactivate periodic adaptation

### Changed

 - updated README.md (and docs) to incorporate more info on the different options
 - updated tests to periodic adaptation option

### Fixed

 [ - ]

### Deprecated

 [ - ]


## [0.9.5] 2021 / 1 / 18

### Added
 
 - add freeze bc patch option through frozen_patch_list

### Changed

 - hausdorff_distance = None instead of []
 - update tests
 - update setup.py

### Fixed

 - updated missing keyword frozen_patch_list in test_hipster 

### Deprecated

 [ - ]


## [0.9.4] 2021 / 1 / 15

### Added
 
 [ - ]

### Changed

 - hip executables updated to v20.12.1
 - set default periodic_adaptation = True

### Fixed

 - adapt regression test to hip v20.12.1

### Deprecated

 [ - ]


## [0.9.3] 2020 / 12 / 22

### Added
 
 [ - ]

### Changed

 - rendering passing of hausdorff distance to hip optional

### Fixed

 [ - ]

### Deprecated

 [ - ]

## [0.9.2] 2020 / 12 / 3

### Added
 
 - periodic_adaptation option (default False) in hip_refine to be compatible with latest hip version

### Changed

 - hip executables updated to v20.07.1

### Fixed

 - adapt regression test to hip v20.07.1

### Deprecated

 [ - ]


## [0.9.1] 2020 / 09 / 25

### Added
 
 [ - ]

### Changed

 [ - ]

### Fixed

 - Future edge field in dry_run mode for both of tekigo run modes, raw_adapt now has a dry_run

### Deprecated

 [ - ]


## [0.9.0] 2020 / 07 / 10

### Added
 
 - Future edge field in dry_run mode for both of tekigo run modes
 - Adapt group in final solution
 - hip hausdorf distance is now editable

### Changed

 - Log now with more verbose, more readable, cells numbers added, version added.

### Fixed

 - min edge values.

### Deprecated

 - max number of nodes -> max number of cells
 - min node volume -> min edge


## [0.8.0] 2020 / 06 / 17

### Added
 
 [ - ]

### Changed

 - Log now with much more verbose, more readable.

### Fixed

 - tests are using h5_same.

### Deprecated

[ - ]


## [0.7.2] 2020 / 06 / 09

### Added
 
 [ - ]

### Changed

 - recommon mark is now used for documentation

### Fixed

 - bugfix on folders emptied by mistake.

### Deprecated

[ - ]


## [0.7.1] 2020 / 03 / 27

### Added
 
 - reading of both average and instntaneous solution files, output of an instantaneous file.

### Changed

 - nob version 0.4.1 is now used.

### Fixed

 - bugfix for average/instantaneous files reading

### Deprecated

[ - ]


## [0.6.3] 2020 / 02 / 06

### Added
 
[ - ]

### Changed

[ - ]

### Fixed

 - compatibility with nob versions older than 0.4
 - tekigo solution files now with 8 numbers.

### Deprecated

[ - ]


## [0.6.2] 2020 / 02 / 05

### Added
 
 - An option in **TekigoSolution** forces removal of results dir

### Changed

 - Coarsening is now optional (in **refine**)

### Fixed

[ - ]

### Deprecated

[ - ]


## [0.6.0] 2020 / 02 / 03

### Added
 
 - Several examples (more or less complex)
 - **raw_adapt** function to make a single loop metric-based adaption (can replace **refine**)
 - **GatherScatter** a tool to morph criterions/monitor_functions:
 	- can do a smoothing
 	- can do morphings (erode, dilate, open, close)
 	- can compute approximative maximum gradient magnitude
 - tools to move from volume at node to approx. volume at cells or edge size (and vice-versa)

### Changed
 - small refactoring:
   - methods reorganization, some set internal, some changed levels

### Fixed
 - CI
   - lint (10.0)
   - test (84%)

### Deprecated
- the *min_vol* target for tekigo can now be replaced by a *min_edge* target


## [0.5.0] 2020 / 01 / 09

### Added
 
 - Documentation
 - Example with edges and temperature criteria

### Changed
 - small refactoring:
   - methods reorganization, some set internal, some changed levels

### Fixed
 - CI
   - lint (10.0)
   - test (20%) 
 - CHANGELOG.md 

### Deprecated
 [ - ] 


## [0.4.0] 2020 / 01 / 08

### Added
 - Corasening function


### Changed
 - README.md

### Fixed
 [ - ] 

### Deprecated
 [ - ] 


## [0.3.0] 2020 / 09 / 10

### Added
 - interface between and tekigo ("hipster")
 - interruption criteria

### Changed
 - major refactoring, division to low-mid-high level 
 - Criteria to stop iteration
 
### Fixed
 [ - ] 

### Deprecated
 [ - ] 