# Changelog

All notable changes to **Maya Rig Controller Tool (Maya RCT)** are documented in this file.

---

## [2.31]
### Added
- Single-step undo for:
  - controller creation
  - shape replacement
  - text controller creation
  - template save/update operations
- Selected controller editing:
  - `Scale Selected Shapes`
  - `Apply Line Width`

### Changed
- Renamed the template section from **Template Helper** to **Template Tools**
- Renamed template actions to clearer labels:
  - `Save Template From Selected`
  - `Update Existing Template`

### Fixed
- Improved undo behavior for multi-curve shapes so `Ctrl+Z` removes the full created controller instead of undoing internal steps one by one

---

## [2.3]
### Added
- GitHub-ready project packaging
- Final project naming:
  - **Maya Rig Controller Tool**
  - **Maya RCT**
- Drag-and-drop Maya installer: `install_maya_rct.py`
- `help.md` loaded from an external file
- Shelf icon support
- Project structure for public release:
  - `maya_rct/maya_rct.py`
  - `maya_rct/help.md`
  - `maya_rct/templates/`
  - `maya_rct/icons/`
  - `install_maya_rct.py`

### Changed
- Main file renamed to `maya_rct.py`
- Version naming switched to dotted public version format

### Fixed
- Removed the non-working title-bar help question mark
- Improved Help button placement
- Preinstalled shapes displayed correctly in the standard shapes section

---

## [2.24]
### Added
- Template Library manager in Settings
- Ability to move templates between:
  - **Standard**
  - **Custom**

### Changed
- Returned to the stable built-in + custom template workflow
- Abandoned the separate built-in JSON package experiment

---

## [2.23]
### Changed
- Experimental external built-in JSON package branch

### Fixed
- Attempted to separate built-in extra shapes from code

### Notes
- This branch was superseded by the `2.24` workflow and is not the final public structure

---

## [2.22]
### Added
- User preinstalled JSON controller shapes as built-in standard shapes:
  - `2_way_arc_arrow`
  - `Corner_Brackets`
  - `cross_arrow_01`
  - `cross_arrow_02`
  - `cylinder`
  - `softCross`
  - `Spherical_Cross_Arrow`

### Notes
- This approach was later replaced by a cleaner template separation workflow

---

## [2.21]
### Changed
- Removed built-in `Cylinder`
- Removed built-in `Cross`
- Reworked `Gear` to a smoother, more gear-like silhouette

---

## [2.20]
### Changed
- Attempted to improve `Cylinder` with top and bottom detail

### Notes
- This version was later replaced because the cylinder shape was not satisfactory

---

## [2.19]
### Added
- New built-in shapes:
  - `Cylinder`
  - `Pyramid`
- Default window height now opens at roughly 70% of screen height

---

## [2.18]
### Changed
- Increased default window height
- Reorganized **Create Options** into a more compact layout
- Put related controls on shared rows:
  - `Direction` + `Up Vector`
  - `Shape Scale` + `Line Width`

### Fixed
- Disabled accidental mouse-wheel edits on settings sliders

---

## [2.17]
### Added
- Vertical scrolling for the main UI

### Fixed
- `Restore Saved Palettes` restored palette data more reliably
- Improved usability on smaller screens

---

## [2.16]
### Fixed
- Corrected text creation orientation so text follows `Direction + Up Vector` more predictably
- Changed `Pick RGB Color` to use a colored border instead of filling the full button

---

## [2.15]
### Added
- Separate palette save file
- `Shape Scale`
- `Line Width`

### Changed
- Palette saving moved to a separate JSON file so palettes can survive factory resets

---

## [2.14]
### Added
- `Save Color Palettes`
- `Restore Saved Palettes`

### Changed
- Default icon size set to `72`
- Default color swatch size set to `48`
- `Current Color` redesigned as a separate visual element

---

## [2.13]
### Added
- Adjustable `Color Swatch Size`
- Adaptive color palette layout
- Slider + value controls for:
  - icon spacing
  - swatch spacing

### Changed
- Color UI layout cleaned up
- Color palettes made denser and more balanced visually

---

## [2.12]
### Changed
- Icon size control upgraded from plain numeric input to slider + value box
- Minimum icon size reduced to `16`
- Color swatches enlarged
- Color block layout redesigned

---

## [2.11]
### Added
- `Preset Palette`
- `Custom Palette`
- `Recent Colors`
- Palette management actions:
  - `Add Current`
  - `Replace Selected`
  - `Remove Selected`

### Changed
- Default window width set to `900`
- Settings now focused more on icon size than window width
- Reworked color workflow to make custom and recent colors visible in the main UI

---

## [2.10]
### Added
- Settings panel
- Editable color presets
- Save current UI state as user defaults
- Restore factory defaults
- Adjustable:
  - icon spacing
  - swatch spacing
  - window width

### Notes
- This version introduced the first full settings system, later refined in `2.11+`

---

## [2.08]
### Changed
- Increased default window width to reduce empty space caused by icon wrapping

---

## [2.07]
### Changed
- Auto-expand window height when opening collapsible sections like:
  - Text Tools
  - Template Helper

---

## [2.06]
### Fixed
- Proper wrapping behavior for both icon and text views
- Prevented overlap when the window becomes narrow

---

## [2.05]
### Fixed
- Text view now uses adaptive column logic instead of a fixed narrow layout

---

## [2.04]
### Fixed
- Icon view now adapts to window width
- Removed hard-coded four-column layout

---

## [2.03]
### Fixed
- Horizontal icon spacing adjusted
- Grid no longer wastes as much horizontal space

---

## [2.02]
### Added
- `Template View` mode toggle:
  - `Icons`
  - `Text`
- `Text Tools` moved into a collapsible section

### Changed
- Shape names removed from under icons
- Names shown through hover/tooltip instead

---

## [2.01]
### Changed
- Flat shapes now generate top-view style auto-icons
- Volumetric shapes keep angled pseudo-3D auto-icons

---

## [2.00]
### Added
- First major UI refresh
- Auto-generated shape icons for:
  - built-in shapes
  - custom templates

### Changed
- Unified dark UI style
- Standard and custom shapes visually aligned
- Shape buttons now display icon-based previews

---

## [1.08]
### Changed
- Custom Templates moved higher in the UI
- Template Helper turned into a collapsible panel

---

## [1.07]
### Added
- Template creation functionality merged into the main tool
- Save template from selected shapes directly inside the tool
- Replace existing template inside the tool

---

## [1.06]
### Added
- `Create Offset Group` option
- Offset group enabled by default
- Optional no-group workflow for controller creation

---

## [1.05]
### Fixed
- Standard shapes no longer create unwanted groups when created without a target selection

---

## [1.04]
### Changed
- Custom templates created more cleanly as shapes under the target transform
- Reduced extra grouping behavior in the JSON template workflow

---

## [1.10]
### Added
- JSON-based template workflow
- New helper to save selected curve data as JSON templates
- Main tool support for loading custom JSON templates

### Changed
- Replaced older `.ma`-based template export/import workflow with JSON curve data storage

---

## [1.02]
### Fixed
- Helper rotation handling bug during template export

---

## [1.01]
### Fixed
- Helper export selection logic
- Reduced duplicate selection and parent warnings during template export

---

## [1.00]
### Added
- First standalone template helper
- Support for saving and loading custom controller templates

### Notes
- Early 1.x template branch was experimental and later evolved into the JSON workflow

---

## [0.08]
### Added
- Separate `Direction` and `Up Vector` controls
- Default orientation updated to:
  - `Direction = X`
  - `Up Vector = Y`

---

## [0.07]
### Changed
- Replaced the earlier up-vector-only orientation workflow with a proper `Direction` control
- Direction now controls where the shape points

---

## [0.06]
### Added
- `Up Vector` selection
- Text offset behavior tied to the chosen up vector

---

## [0.05]
### Added
- Orientation selection by plane:
  - `XY`
  - `XZ`
  - `YZ`

### Changed
- Removed the earlier `Apply Color To Selected` button

---

## [0.04]
### Fixed
- `launch_ui()` object name handling bug in Maya / Qt integration

---

## [0.03]
### Added
- Checkbox to enable or disable adding text during controller creation

### Changed
- Text creation centered more correctly
- Color application became more direct
- Font name input removed in favor of simpler text handling

---

## [0.02]
### Added
- Reset UI settings
- Visual color swatches instead of a plain color dropdown

### Fixed
- Text creation no longer stacks all letters in the same position

---

## [0.01]
### Added
- Initial working prototype
- Built-in controller shape library
- Create / Change Shape modes
- Multi-selection controller creation
- RGB color support
- Text controller creation
- Shape + text controller creation
- Offset-group workflow
- Constraint-based creation options

---

## Notes
- Versions in the `1.x` range were internal development milestones while the template workflow was being designed
- Public GitHub-ready packaging started in the `2.3` range