## [1.1.1] - 2025-03-07
### Added
- 

### Changed
- Lua extracting now using recursion to be able to handle nested inputs
- Lua generation now using recursion to be able to generate nested lua dicts

### Fixed
- Patched the bug where sneding a nested lua object the ineer values are not returned correctly

### Removed
- 


## [1.1.0] - 2025-03-07
### Added
- Added support for LUA files.
- Added new module in tools "lua_tools" to contain the functions for handling lua files.
- Automated gitflow 

### Changed
- API call changed, both JSON and LUA files are axpected in forms.
- Removed hardcoded values for "file_type" in system prompt.
- file_type is hardcoded in the Flask App.
- File type is automatically detected from API call and processed with the corresponding steps.
- New requirement was added "lupa" this handles the LUA files.
- Updated README with the corresponding changes.
- Updated .gitignore to ignore notebooks

### Fixed
- Flask app loggign now works as intended, the mounted folder in the Dockerfile was fixed.

### Removed
- Removed the option to call the API with raw JSON as body
- Removed unnecessary screenshots from README


## [1.0.0] - 2025-02-27
### Added
- Added first version of the translation logic
- Added support for JSON.
- Added README.
- Added Docker-compose.

### Changed
- 

### Fixed
- 

### Removed
- 
