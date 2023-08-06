# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).


## [0.1.0-alpha.6] - 2021-07-08

### Changed

- Compatibility with Python 3.9 and Django 3.2


## [0.1.0-alpha.5] - 2021-01-25

### Added

- ESI error hardening

### Changed

- Fleet table on dashboard is now loaded via ajax and refreshed every 30 seconds


## [0.1.0-alpha.4] - 2021-01-12

### Removed

- Django 2 support


## [0.1.0-alpha.3] - 2021-01-05

### Fixed

- Permission to create fleets


## [0.1.0-alpha.2] - 2021-01-05

### Changed

- Datatables in fleet details view set up properly
- UI in fleet details view re-done
- Fleet details are nor refreshed every 15 seconds via Datatables reload


## [0.1.0-alpha.1] - 2020-12-30

App forked from [Dreadbomb/aa-fleet](https://github.com/Dreadbomb/aa-fleet)

### Fixed

- HTML errors
- Datatable erors
- Import order
- Code issues cleaned up
- General model and permissions

### Changed

- Fleet commander transformed into EveCharacter model
- Automatic page reload in fleet details view deactivated (was causing troubles)
- Datatable for dashboard configured properly
- Migrations reset
