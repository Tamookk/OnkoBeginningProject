# Changelog
## 2021-05-31
### Added
* Image window UI.


## 2021-05-30
### Added
* Ability to convert RT Image data and view this image inside the program.


## 2021-05-29
### Added
* Program can now discover if a DICOM file set has RT Struct, CT Image, RT Dose, or RT Plan elements. The presence of each is printed to the command line. The program can also determine which of these each individual DICOM file contains.


## 2021-05-28
### Added
* Program can now find all DICOM files inside the program's default directory.


## 2021-05-24
### Added
* Select Patient Window.

### Changed
* Renamed Model folder to View.


## 2021-05-21
### Added
* Ability to open SQLite configuration file if it exists.
* Program creates SQLite configuration file and writes default directory to it.
* Program can read settings from configuration file.

### Changed
* Moved First Time Window GUI into own file.

### Fixed
* Some bugs concerning filepaths:
  * If filepath doesn't exist, it is set to the user's home directory.
  * If filepath input field is empty when folder is created, it is created in user's home directory.
  * Tree folder view now reflects input field file path, is set to user's home if filepath is invalid.


## 2021-05-19
### Added
* GUI based on first-time startup wireframe.

### Fixed
* Bug where creating `.OnkoDICOM` folder without first picking a loction via the file dialog would create the folder in the root directory.


## 2021-05-14
### Added
* Basic PyQt window.
* Ability to get and display the user's home directory on button click.


## 2021-05-13
### Added
* Initial project files.