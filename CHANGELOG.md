# Changelog

All notable changes to this project will be documented in this file

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.2] -

### Fixed

- `config.example.py` now has correct string examples

## [0.0.1] - 2021-01-17

### Added

- Backup
  - Daily full backups
  - Weekly full backups with daily diffs
  - Monthly full backups with weekly and daily diffs
  - MySQL daily backups
- Remove old backups
- Mail user if backups failed
- Mail user if backup disk drive is almost full
- Force a full backup with `--full-backup`
