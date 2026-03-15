# Maya Rig Controller Tool

**Maya Rig Controller Tool** (**Maya RCT**) is a controller shape tool for Autodesk Maya.

Release: **v_2.3**

## Features
- Create and replace controller shapes
- Built-in shapes and JSON templates
- Direction and Up Vector controls
- RGB palettes, custom palette, and recent colors
- Text controller tools
- Shape Scale and Line Width controls
- Promote / demote templates between Custom and Standard
- In-app Help panel

## Installation

### Recommended: drag-and-drop installer
1. Download or clone this repository.
2. Keep the folder where you want it to live.
3. Drag **`install_maya_rct.py`** into a Maya viewport or Script Editor.
4. The installer creates a shelf button named **Maya RCT**.

> If you move the project folder later, run the installer again so the shelf button can update its path.

### Manual launch
```python
import sys
import importlib

repo_path = r"C:/path/to/maya-rig-controller-tool_v_2.3"
if repo_path not in sys.path:
    sys.path.append(repo_path)

from maya_rct import maya_rct
importlib.reload(maya_rct)
maya_rct.launch_ui()
```

## Shelf icon
The default shelf icon is:
`maya_rct/icons/maya_rct.png`

Replace that file if you want to use your own icon.

## Templates
Custom template JSON files live in:
`maya_rct/templates`

## Help
The in-app **Help** button loads text from:
`maya_rct/help.md`

## License
MIT
