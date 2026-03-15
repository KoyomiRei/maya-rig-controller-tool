\
import os
import maya.cmds as cmds
import maya.mel as mel

TOOL_LABEL = "Maya RCT"
TOOL_ANNOTATION = "Launch Maya Rig Controller Tool"
TOOL_PACKAGE = "maya_rct"


def _project_root():
    return os.path.dirname(os.path.abspath(__file__))


def _package_root():
    return os.path.join(_project_root(), TOOL_PACKAGE)


def _icon_path():
    path = os.path.join(_package_root(), "icons", "maya_rct.png")
    return path if os.path.exists(path) else ""


def _launch_command():
    repo_path = _project_root().replace("\\", "/")
    return """import sys\nimport importlib\nrepo_path = r'{repo_path}'\nif repo_path not in sys.path:\n    sys.path.append(repo_path)\nfrom maya_rct import maya_rct\nimportlib.reload(maya_rct)\nmaya_rct.launch_ui()""".format(repo_path=repo_path)


def _current_shelf():
    shelf_top = mel.eval('$tmp = $gShelfTopLevel')
    return cmds.tabLayout(shelf_top, query=True, selectTab=True)


def _remove_existing_button(shelf_name):
    children = cmds.shelfLayout(shelf_name, query=True, childArray=True) or []
    for child in children:
        try:
            label = cmds.shelfButton(child, query=True, label=True)
            annotation = cmds.shelfButton(child, query=True, annotation=True)
        except Exception:
            continue
        if label == TOOL_LABEL or annotation == TOOL_ANNOTATION:
            cmds.deleteUI(child)


def install_to_current_shelf(*_):
    package_root = _package_root()
    if not os.path.isdir(package_root):
        cmds.confirmDialog(title="Maya RCT Installer", message="Could not find the maya_rct package next to the installer.", button=["OK"])
        return

    shelf_name = _current_shelf()
    if not shelf_name:
        cmds.confirmDialog(title="Maya RCT Installer", message="Could not find the current Maya shelf.", button=["OK"])
        return

    _remove_existing_button(shelf_name)

    kwargs = dict(
        parent=shelf_name,
        label=TOOL_LABEL,
        annotation=TOOL_ANNOTATION,
        command=_launch_command(),
        sourceType="Python",
        imageOverlayLabel="RCT",
    )
    icon_path = _icon_path()
    if icon_path:
        kwargs["image"] = icon_path.replace("\\", "/")

    cmds.shelfButton(**kwargs)
    cmds.inViewMessage(amg='Maya RCT installed to shelf: <hl>{}</hl>'.format(shelf_name), pos='midCenterTop', fade=True)


def onMayaDroppedPythonFile(*args):
    install_to_current_shelf()


if __name__ == "__main__":
    install_to_current_shelf()
