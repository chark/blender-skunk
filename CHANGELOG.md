# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v0.0.11](https://github.com/chark/blender-skunk/compare/v0.0.10...v0.0.11) - 2024-09-28

### Changed

- Bulk Export feature to work with armatures.

## [v0.0.10](https://github.com/chark/blender-skunk/compare/v0.0.9...v0.0.10) - 2024-08-14

### Added

- Object distribution will sort objects by name before distributing.

### Fixed

- Distance not being used in object distribution.

## [v0.0.9](https://github.com/chark/blender-skunk/compare/v0.0.8...v0.0.9) - 2024-08-05

### Changed

- Increased UV quality.

## [v0.0.8](https://github.com/chark/blender-skunk/compare/v0.0.7...v0.0.8) - 2024-08-05

### Added

- Operator to sort mesh faces by material.

## [v0.0.7](https://github.com/chark/blender-skunk/compare/v0.0.6...v0.0.7) - 2024-08-05

### Fixed

- Smart UV project not selecting all quads.

## [v0.0.6](https://github.com/chark/blender-skunk/compare/v0.0.5...v0.0.6) - 2024-08-05

### Added

- Operator to delete LODs.

## [v0.0.5](https://github.com/chark/blender-skunk/compare/v0.0.4...v0.0.5) - 2024-08-05

### Fixed

- Parenting function is not applying a child's name.
- Data blocks not being removed when deleting LODs.

## [v0.0.4](https://github.com/chark/blender-skunk/compare/v0.0.3...v0.0.4) - 2024-08-01

### Changed

- Changed lightmap pack to smart UV project as lightmap pack causes leaks.

## [v0.0.3](https://github.com/chark/blender-skunk/compare/v0.0.2...v0.0.3) - 2024-07-31

### Changed

- Default lightmap UV margin to `0.5`.

## [v0.0.2](https://github.com/chark/blender-skunk/compare/v0.0.1...v0.0.2) - 2024-07-31

### Added

- Option to create UVs with lightmap UV1.

## [v0.0.1](https://github.com/chark/blender-skunk/compare/v0.0.1) - 2024-07-30

### Added

- Distribute operator.
- Empty parent operator.
- Mesh name fixer/matcher operator.
- LOD creation operator.
- Bulk FBX export operator.
