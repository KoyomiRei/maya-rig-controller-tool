import copy
import json
import math
import os

import maya.cmds as cmds
import maya.api.OpenMaya as om2
import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance
from PySide2 import QtWidgets, QtCore, QtGui

WINDOW_OBJECT = "MayaRCTUI"
WINDOW_TITLE = "Maya Rig Controller Tool"
VERSION = "2.3"
DEFAULT_TEXT_SCALE = 0.35
DEFAULT_TEXT_OFFSET = 1.35
DEFAULT_COLOR_NAME = "Yellow"
DEFAULT_TEXT_ENABLED = False
DEFAULT_DIRECTION = "X"
DEFAULT_UP_VECTOR = "Y"
DEFAULT_CREATE_OFFSET_GROUP = True
DEFAULT_SHAPE_SCALE = 1.0
DEFAULT_LINE_WIDTH = 1.0
DEFAULT_SHAPE_DISPLAY_MODE = "Icons"
FACTORY_ICON_BUTTON_SIZE = 72
FACTORY_ICON_DRAW_RATIO = 0.89
SHAPE_GRID_SPACING = 4
ICON_MIN_COLUMNS = 2
FACTORY_TEXT_BUTTON_MIN_WIDTH = 148
TEMPLATE_DIR_NAME = "templates"
PREINSTALLED_TEMPLATE_DIR_NAME = "preinstalled"
CUSTOM_TEMPLATE_DIR_NAME = "custom"
TEMPLATE_EXTENSION = ".json"
PREINSTALLED_TEMPLATE_NAMES = [
    "2_way_arc_arrow",
    "Corner_Brackets",
    "cross_arrow_01",
    "cross_arrow_02",
    "cylinder",
    "softCross",
    "spherical_Cross_Arrow",
]
RECENT_COLOR_LIMIT = 10
CUSTOM_PALETTE_LIMIT = 16

COLOR_PRESETS = {
    "Yellow": (1.0, 1.0, 0.0),
    "Red": (1.0, 0.25, 0.25),
    "Blue": (0.30, 0.60, 1.0),
    "Green": (0.35, 1.0, 0.45),
    "Purple": (0.75, 0.45, 1.0),
    "Cyan": (0.2, 1.0, 1.0),
    "Orange": (1.0, 0.55, 0.15),
    "Pink": (1.0, 0.45, 0.75),
    "White": (1.0, 1.0, 1.0),
    "Black": (0.0, 0.0, 0.0),
}

FACTORY_COLOR_PRESETS = copy.deepcopy(COLOR_PRESETS)
SETTINGS_FILE_NAME = "maya_rct_settings.json"
PALETTES_FILE_NAME = "maya_rct_palettes.json"
HELP_FILE_NAME = "help.md"
FACTORY_SWATCH_SPACING = 4
FACTORY_SWATCH_SIZE = 48
FACTORY_WINDOW_WIDTH = 900
FACTORY_WINDOW_HEIGHT = 940

BUILTIN_SHAPE_NAMES = [
    "Circle",
    "Square",
    "Triangle",
    "Cube",
    "Sphere",
    "Pyramid",
    "Arrow",
    "Diamond",
    "Gear",
]

AXIS_VECTORS = {
    "X": (1.0, 0.0, 0.0),
    "-X": (-1.0, 0.0, 0.0),
    "Y": (0.0, 1.0, 0.0),
    "-Y": (0.0, -1.0, 0.0),
    "Z": (0.0, 0.0, 1.0),
    "-Z": (0.0, 0.0, -1.0),
}
AXIS_DISPLAY_ORDER = ["-X", "X", "-Y", "Y", "-Z", "Z"]


def maya_main_window():
    ptr = omui.MQtUtil.mainWindow()
    if ptr is None:
        return None
    return wrapInstance(int(ptr), QtWidgets.QWidget)


def default_window_height():
    app = QtWidgets.QApplication.instance()
    screen = app.primaryScreen() if app else None
    available_height = screen.availableGeometry().height() if screen else 1200
    return max(760, int(available_height * 0.70))


class NoWheelSlider(QtWidgets.QSlider):
    def wheelEvent(self, event):
        event.ignore()



def script_root_directory():
    module_file = globals().get("__file__")
    if module_file:
        return os.path.dirname(os.path.abspath(module_file))
    scripts_dir = cmds.internalVar(userScriptDir=True)
    return os.path.abspath(scripts_dir)


def settings_file_path():
    return os.path.join(script_root_directory(), SETTINGS_FILE_NAME)


def palettes_file_path():
    return os.path.join(script_root_directory(), PALETTES_FILE_NAME)


def help_file_path():
    return os.path.join(script_root_directory(), HELP_FILE_NAME)


def default_help_text():
    return """# Maya Rig Controller Tool

## 1. Basic Workflow
- Use **Create** to make new controllers.
- Use **Change Shape** to replace the shape on an existing controller.
- Create on a selection to align the controller to that object.
- Create with nothing selected to place a controller directly in the scene.

## 2. Orientation
- **Direction** controls where the controller points.
- **Up Vector** controls which side is treated as the top.

## 3. Color
- Click a color swatch to use that color.
- Use **Pick RGB Color** for any custom color.
- Save useful colors to **Custom Palette**.
- **Recent Colors** keeps the last colors you used.

## 4. Text Tools
- Enable text to add a label when creating a controller.
- Use **Create Text Only** for a standalone text controller.
- **Text Scale** changes text size.
- **Text Offset** moves the text away from the main shape.

## 5. Shape Controls
- **Shape Scale** changes the size of the curve shape.
- **Line Width** changes viewport display thickness.
- **Create Offset Group** adds a zero group above the controller.

## 6. Templates
- Save selected curves as custom templates.
- Custom templates appear in **Custom Templates**.
- Use **Settings > Template Library** to move templates between **Custom** and **Standard**.

## 7. More Information
More docs, screenshots, and updates: GitHub page coming soon.
"""


def load_help_text():
    path = help_file_path()
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as handle:
                text = handle.read().strip()
                if text:
                    return text
        except Exception:
            pass
    return default_help_text()


def factory_settings_data():
    return {
        "display_settings": {
            "shape_grid_spacing": SHAPE_GRID_SPACING,
            "swatch_spacing": FACTORY_SWATCH_SPACING,
            "icon_button_size": FACTORY_ICON_BUTTON_SIZE,
            "swatch_button_size": FACTORY_SWATCH_SIZE,
            "window_height": FACTORY_WINDOW_HEIGHT,
        },
        "user_defaults": {
            "constraint": False,
            "create_offset_group": DEFAULT_CREATE_OFFSET_GROUP,
            "direction": DEFAULT_DIRECTION,
            "up_vector": DEFAULT_UP_VECTOR,
            "shape_display_mode": DEFAULT_SHAPE_DISPLAY_MODE,
            "shape_scale": DEFAULT_SHAPE_SCALE,
            "line_width": DEFAULT_LINE_WIDTH,
            "text_enabled": DEFAULT_TEXT_ENABLED,
            "text_scale": DEFAULT_TEXT_SCALE,
            "text_offset": DEFAULT_TEXT_OFFSET,
            "rgb": list(FACTORY_COLOR_PRESETS[DEFAULT_COLOR_NAME]),
        },
        "template_manager": {
            "promoted_templates": [],
        },
    }


def factory_palette_data():
    return {
        "color_presets": copy.deepcopy(FACTORY_COLOR_PRESETS),
        "custom_palette": [],
        "recent_colors": [],
        "saved_color_state": {
            "color_presets": copy.deepcopy(FACTORY_COLOR_PRESETS),
            "custom_palette": [],
            "recent_colors": [],
        },
    }



def _normalize_settings_data(raw_data):
    data = factory_settings_data()
    if not isinstance(raw_data, dict):
        return data

    display = raw_data.get("display_settings")
    if isinstance(display, dict):
        for key in data["display_settings"].keys():
            value = display.get(key)
            if isinstance(value, (int, float)):
                data["display_settings"][key] = int(value)

    user_defaults = raw_data.get("user_defaults")
    if isinstance(user_defaults, dict):
        for key in data["user_defaults"].keys():
            if key == "rgb":
                value = user_defaults.get("rgb")
                if isinstance(value, (list, tuple)) and len(value) == 3:
                    data["user_defaults"]["rgb"] = [float(value[0]), float(value[1]), float(value[2])]
            elif key in {"constraint", "create_offset_group", "text_enabled"}:
                if key in user_defaults:
                    data["user_defaults"][key] = bool(user_defaults.get(key))
            elif key in {"text_scale", "text_offset", "shape_scale", "line_width"}:
                if isinstance(user_defaults.get(key), (int, float)):
                    data["user_defaults"][key] = float(user_defaults.get(key))
            else:
                value = user_defaults.get(key)
                if isinstance(value, str) and value:
                    data["user_defaults"][key] = value

    template_manager = raw_data.get("template_manager")
    if isinstance(template_manager, dict):
        names = template_manager.get("promoted_templates")
        if isinstance(names, list):
            cleaned = []
            for name in names:
                if not isinstance(name, str):
                    continue
                safe_name = sanitize_template_name(name)
                if safe_name and safe_name not in BUILTIN_SHAPE_NAMES and safe_name not in cleaned:
                    cleaned.append(safe_name)
            data["template_manager"]["promoted_templates"] = cleaned

    return data


def _normalize_palette_data(raw_data):
    data = factory_palette_data()
    if not isinstance(raw_data, dict):
        return data

    color_presets = raw_data.get("color_presets")
    if isinstance(color_presets, dict) and color_presets:
        normalized = {}
        for name, rgb in color_presets.items():
            if not isinstance(name, str):
                continue
            if not isinstance(rgb, (list, tuple)) or len(rgb) != 3:
                continue
            clean_name = name.strip()
            if not clean_name:
                continue
            normalized[clean_name] = (float(rgb[0]), float(rgb[1]), float(rgb[2]))
        if normalized:
            data["color_presets"] = normalized

    for palette_key in ("custom_palette", "recent_colors"):
        palette = raw_data.get(palette_key)
        if isinstance(palette, list):
            cleaned = []
            for rgb in palette:
                if not isinstance(rgb, (list, tuple)) or len(rgb) != 3:
                    continue
                cleaned.append((float(rgb[0]), float(rgb[1]), float(rgb[2])))
            data[palette_key] = cleaned

    saved_color_state = raw_data.get("saved_color_state")
    if isinstance(saved_color_state, dict):
        normalized_saved = {
            "color_presets": copy.deepcopy(data["color_presets"]),
            "custom_palette": list(data["custom_palette"]),
            "recent_colors": list(data["recent_colors"]),
        }
        palettes = saved_color_state.get("color_presets")
        if isinstance(palettes, dict) and palettes:
            clean_presets = {}
            for name, rgb in palettes.items():
                if not isinstance(name, str):
                    continue
                if not isinstance(rgb, (list, tuple)) or len(rgb) != 3:
                    continue
                clean_name = name.strip()
                if not clean_name:
                    continue
                clean_presets[clean_name] = (float(rgb[0]), float(rgb[1]), float(rgb[2]))
            if clean_presets:
                normalized_saved["color_presets"] = clean_presets
        for palette_key in ("custom_palette", "recent_colors"):
            palette = saved_color_state.get(palette_key)
            if isinstance(palette, list):
                cleaned = []
                for rgb in palette:
                    if not isinstance(rgb, (list, tuple)) or len(rgb) != 3:
                        continue
                    cleaned.append((float(rgb[0]), float(rgb[1]), float(rgb[2])))
                normalized_saved[palette_key] = cleaned
        data["saved_color_state"] = normalized_saved

    return data


def load_tool_settings():
    path = settings_file_path()
    if not os.path.exists(path):
        return factory_settings_data()
    try:
        with open(path, "r") as handle:
            raw_data = json.load(handle)
    except Exception:
        return factory_settings_data()
    return _normalize_settings_data(raw_data)


def save_tool_settings(settings_data):
    normalized = _normalize_settings_data(settings_data)
    path = settings_file_path()
    with open(path, "w") as handle:
        json.dump(normalized, handle, indent=4, sort_keys=False)
    return normalized


def load_palette_data():
    path = palettes_file_path()
    if os.path.exists(path):
        try:
            with open(path, "r") as handle:
                raw_data = json.load(handle)
            return _normalize_palette_data(raw_data)
        except Exception:
            pass

    legacy_path = settings_file_path()
    if os.path.exists(legacy_path):
        try:
            with open(legacy_path, "r") as handle:
                raw_data = json.load(handle)
            legacy_palette_data = {
                "color_presets": raw_data.get("color_presets", FACTORY_COLOR_PRESETS),
                "custom_palette": raw_data.get("custom_palette", []),
                "recent_colors": raw_data.get("recent_colors", []),
                "saved_color_state": raw_data.get("saved_color_state", factory_palette_data()["saved_color_state"]),
            }
            normalized = _normalize_palette_data(legacy_palette_data)
            save_palette_data(normalized)
            return normalized
        except Exception:
            pass

    return factory_palette_data()


def save_palette_data(palette_data):
    normalized = _normalize_palette_data(palette_data)
    path = palettes_file_path()
    with open(path, "w") as handle:
        json.dump(normalized, handle, indent=4, sort_keys=False)
    return normalized


def template_root_directory():
    path = os.path.join(script_root_directory(), TEMPLATE_DIR_NAME)
    if not os.path.isdir(path):
        os.makedirs(path)
    return path


def template_directory():
    return custom_template_directory()


def preinstalled_template_directory():
    path = os.path.join(template_root_directory(), PREINSTALLED_TEMPLATE_DIR_NAME)
    if not os.path.isdir(path):
        os.makedirs(path)
    return path


def custom_template_directory():
    path = os.path.join(template_root_directory(), CUSTOM_TEMPLATE_DIR_NAME)
    if not os.path.isdir(path):
        os.makedirs(path)
    return path


def legacy_template_directory():
    return template_root_directory()


def sanitize_template_name(name):
    cleaned = "".join(char if char.isalnum() or char == "_" else "_" for char in (name or "").strip())
    while "__" in cleaned:
        cleaned = cleaned.replace("__", "_")
    return cleaned.strip("_")


def _directory_template_names(directory):
    names = []
    if not os.path.isdir(directory):
        return names
    for file_name in os.listdir(directory):
        if not file_name.lower().endswith(TEMPLATE_EXTENSION):
            continue
        name = os.path.splitext(file_name)[0]
        if name not in BUILTIN_SHAPE_NAMES:
            names.append(name)
    return names


def preinstalled_template_names():
    names = set(_directory_template_names(preinstalled_template_directory()))
    legacy_names = set(_directory_template_names(legacy_template_directory()))
    for name in PREINSTALLED_TEMPLATE_NAMES:
        if name in legacy_names:
            names.add(name)
    return sorted(names, key=lambda value: value.lower())


def custom_template_names():
    names = set(_directory_template_names(custom_template_directory()))
    legacy_names = set(_directory_template_names(legacy_template_directory()))
    for name in legacy_names:
        if name not in PREINSTALLED_TEMPLATE_NAMES:
            names.add(name)
    return sorted(names, key=lambda value: value.lower())


def template_names():
    names = set(preinstalled_template_names())
    names.update(custom_template_names())
    return sorted(names, key=lambda value: value.lower())


def template_file_path(template_name):
    safe_name = sanitize_template_name(template_name)
    return os.path.join(custom_template_directory(), "{0}{1}".format(safe_name, TEMPLATE_EXTENSION))


def locate_template_file_path(template_name):
    safe_name = sanitize_template_name(template_name)
    candidate_paths = [
        os.path.join(custom_template_directory(), "{0}{1}".format(safe_name, TEMPLATE_EXTENSION)),
        os.path.join(preinstalled_template_directory(), "{0}{1}".format(safe_name, TEMPLATE_EXTENSION)),
        os.path.join(legacy_template_directory(), "{0}{1}".format(safe_name, TEMPLATE_EXTENSION)),
    ]
    for path in candidate_paths:
        if os.path.exists(path):
            return path
    return candidate_paths[0]


def load_template_data(template_name):
    path = locate_template_file_path(template_name)
    if not os.path.exists(path):
        raise RuntimeError("Template file not found: {0}".format(path))
    with open(path, "r") as handle:
        data = json.load(handle)
    curves = data.get("curves") or []
    if not curves:
        raise RuntimeError("Template has no curve data: {0}".format(template_name))
    return data


def save_template_data(template_name, data):
    path = template_file_path(template_name)
    with open(path, "w") as handle:
        json.dump(data, handle, indent=4, sort_keys=False)
    return path


def unique_name(name):
    if not cmds.objExists(name):
        return name
    index = 1
    while cmds.objExists("{0}_{1:02d}".format(name, index)):
        index += 1
    return "{0}_{1:02d}".format(name, index)


def short_name(node):
    if not node:
        return "Controller"
    return node.split("|")[-1].split(":")[-1]


def ctrl_name_from_target(target):
    return unique_name("{0}_CTRL".format(short_name(target)))


def offset_name_from_ctrl(ctrl_name):
    return unique_name("{0}_GRP".format(ctrl_name))


def get_shapes(node):
    return cmds.listRelatives(node, shapes=True, noIntermediate=True, fullPath=True) or []


def get_transforms_with_shapes(root):
    transforms = []
    if cmds.objExists(root) and cmds.nodeType(root) == "transform" and get_shapes(root):
        transforms.append(root)
    descendants = cmds.listRelatives(root, allDescendents=True, type="transform", fullPath=True) or []
    for item in descendants:
        if get_shapes(item):
            transforms.append(item)
    return transforms


def parent_shapes(source_transform, target_transform):
    shapes = get_shapes(source_transform)
    for shape in shapes:
        cmds.parent(shape, target_transform, add=True, shape=True, relative=True)


def curve_components(node):
    components = []
    for shape in get_shapes(node):
        if cmds.nodeType(shape) == "nurbsCurve":
            components.append(shape + ".cv[*]")
    return components


def apply_rgb_color(node, rgb):
    shapes = []
    if cmds.nodeType(node) == "transform":
        shapes = get_shapes(node)
    elif cmds.nodeType(node) == "nurbsCurve":
        shapes = [node]

    for shape in shapes:
        cmds.setAttr(shape + ".overrideEnabled", 1)
        cmds.setAttr(shape + ".overrideRGBColors", 1)
        cmds.setAttr(shape + ".overrideColorRGB", rgb[0], rgb[1], rgb[2], type="double3")


def apply_line_width(node, line_width):
    shapes = []
    if cmds.nodeType(node) == "transform":
        shapes = get_shapes(node)
    elif cmds.nodeType(node) == "nurbsCurve":
        shapes = [node]

    value = max(1.0, float(line_width))
    for shape in shapes:
        if cmds.attributeQuery("lineWidth", node=shape, exists=True):
            try:
                cmds.setAttr(shape + ".lineWidth", value)
            except Exception:
                pass


def scale_curve_shapes(node, scale_value):
    value = float(scale_value)
    if abs(value - 1.0) < 0.0001:
        return
    components = curve_components(node)
    if not components:
        return
    try:
        cmds.scale(value, value, value, components, relative=True, objectSpace=True, pivot=(0.0, 0.0, 0.0))
    except Exception:
        cmds.scale(value, value, value, components, relative=True, pivot=(0.0, 0.0, 0.0))


def get_shape_color(node):
    shapes = get_shapes(node)
    for shape in shapes:
        if cmds.getAttr(shape + ".overrideEnabled"):
            if cmds.attributeQuery("overrideRGBColors", node=shape, exists=True) and cmds.getAttr(shape + ".overrideRGBColors"):
                value = cmds.getAttr(shape + ".overrideColorRGB")[0]
                return tuple(value)
    return None


def delete_shapes(node):
    shapes = get_shapes(node)
    if shapes:
        cmds.delete(shapes)


def match_transform(source, target):
    temp = cmds.parentConstraint(source, target, mo=False)
    cmds.delete(temp)


def freeze_transform(node):
    cmds.makeIdentity(node, apply=True, translate=True, rotate=True, scale=True, normal=False)


def normalize_axis_name(value, default_value):
    normalized = (value or default_value).strip().upper()
    if normalized in {"+X", "X+"}:
        return "X"
    if normalized in {"+Y", "Y+"}:
        return "Y"
    if normalized in {"+Z", "Z+"}:
        return "Z"
    return normalized if normalized in AXIS_VECTORS else default_value


def normalize_direction_name(direction):
    return normalize_axis_name(direction, DEFAULT_DIRECTION)


def normalize_up_vector_name(up_vector):
    return normalize_axis_name(up_vector, DEFAULT_UP_VECTOR)


def dot_product(vector_a, vector_b):
    return vector_a[0] * vector_b[0] + vector_a[1] * vector_b[1] + vector_a[2] * vector_b[2]


def vector_length(vector_value):
    return math.sqrt(dot_product(vector_value, vector_value))


def normalize_vector(vector_value):
    length = vector_length(vector_value)
    if length < 1e-8:
        return (0.0, 0.0, 0.0)
    return (vector_value[0] / length, vector_value[1] / length, vector_value[2] / length)


def cross_product(vector_a, vector_b):
    return (
        vector_a[1] * vector_b[2] - vector_a[2] * vector_b[1],
        vector_a[2] * vector_b[0] - vector_a[0] * vector_b[2],
        vector_a[0] * vector_b[1] - vector_a[1] * vector_b[0],
    )


def vectors_parallel(vector_a, vector_b, tolerance=0.9999):
    vector_a = normalize_vector(vector_a)
    vector_b = normalize_vector(vector_b)
    return abs(dot_product(vector_a, vector_b)) >= tolerance


def fallback_up_vector(direction):
    direction = normalize_direction_name(direction)
    direction_vector = AXIS_VECTORS[direction]
    for candidate in (DEFAULT_UP_VECTOR, "Z", "X", "-Y", "-Z", "-X"):
        candidate_name = normalize_up_vector_name(candidate)
        if not vectors_parallel(direction_vector, AXIS_VECTORS[candidate_name]):
            return candidate_name
    return "Y"


def resolve_direction_and_up(direction, up_vector):
    direction_name = normalize_direction_name(direction)
    up_name = normalize_up_vector_name(up_vector)
    if vectors_parallel(AXIS_VECTORS[direction_name], AXIS_VECTORS[up_name]):
        up_name = fallback_up_vector(direction_name)
    return direction_name, up_name


def vector_to_axis_name(vector_value):
    normalized = normalize_vector(vector_value)
    best_name = None
    best_dot = -1.0
    for axis_name, axis_vector in AXIS_VECTORS.items():
        current_dot = dot_product(normalized, normalize_vector(axis_vector))
        if current_dot > best_dot:
            best_dot = current_dot
            best_name = axis_name
    return best_name or DEFAULT_DIRECTION


def orientation_basis(direction, up_vector):
    direction_name, up_name = resolve_direction_and_up(direction, up_vector)
    z_axis = normalize_vector(AXIS_VECTORS[direction_name])
    up_axis = normalize_vector(AXIS_VECTORS[up_name])
    x_axis = normalize_vector(cross_product(up_axis, z_axis))
    y_axis = normalize_vector(cross_product(z_axis, x_axis))
    return x_axis, y_axis, z_axis


def orient_transform(node, direction, up_vector=DEFAULT_UP_VECTOR):
    direction_name, up_name = resolve_direction_and_up(direction, up_vector)
    direction_vector = AXIS_VECTORS[direction_name]
    up_world_vector = AXIS_VECTORS[up_name]

    target_locator = cmds.spaceLocator(name=unique_name("__aimTarget"))[0]
    cmds.xform(target_locator, worldSpace=True, translation=direction_vector)

    constraint = cmds.aimConstraint(
        target_locator,
        node,
        aimVector=(0.0, 0.0, 1.0),
        upVector=(0.0, 1.0, 0.0),
        worldUpType="vector",
        worldUpVector=up_world_vector,
        maintainOffset=False,
    )[0]

    cmds.delete(constraint)
    cmds.delete(target_locator)


def get_dag_path(node_name):
    selection = om2.MSelectionList()
    selection.add(node_name)
    return selection.getDagPath(0)


def curve_form_to_string(form_value):
    if form_value == om2.MFnNurbsCurve.kClosed:
        return "closed"
    if form_value == om2.MFnNurbsCurve.kPeriodic:
        return "periodic"
    return "open"


def canonical_coordinates_from_world(point, pivot, direction, up_vector):
    x_axis, y_axis, z_axis = orientation_basis(direction, up_vector)
    offset = (
        point.x - pivot[0],
        point.y - pivot[1],
        point.z - pivot[2],
    )
    return [
        dot_product(offset, x_axis),
        dot_product(offset, y_axis),
        dot_product(offset, z_axis),
        point.w,
    ]


def selected_root_transforms():
    selection = cmds.ls(selection=True, long=True) or []
    roots = []
    for node in selection:
        if not cmds.objExists(node):
            continue
        node_type = cmds.nodeType(node)
        if node_type == "transform":
            roots.append(node)
        elif node_type == "nurbsCurve":
            parents = cmds.listRelatives(node, parent=True, fullPath=True) or []
            roots.extend(parents)
    unique_roots = []
    seen = set()
    for root in roots:
        if root in seen:
            continue
        seen.add(root)
        unique_roots.append(root)
    return unique_roots


def gather_curve_shapes(roots):
    shapes = []
    seen = set()
    for root in roots:
        if not cmds.objExists(root):
            continue
        current_shapes = []
        if cmds.nodeType(root) == "transform":
            current_shapes.extend(get_shapes(root))
        descendants = cmds.listRelatives(root, allDescendents=True, type="nurbsCurve", noIntermediate=True, fullPath=True) or []
        current_shapes.extend(descendants)
        for shape in current_shapes:
            if not cmds.objExists(shape):
                continue
            if cmds.nodeType(shape) != "nurbsCurve":
                continue
            if shape in seen:
                continue
            seen.add(shape)
            shapes.append(shape)
    return shapes


def collect_template_data_from_selection(template_name, direction, up_vector):
    roots = selected_root_transforms()
    if not roots:
        raise RuntimeError("Select at least one curve control transform to save as a template.")

    shapes = gather_curve_shapes(roots)
    if not shapes:
        raise RuntimeError("The current selection does not contain any usable nurbsCurve shapes.")

    pivot = cmds.xform(roots[0], query=True, worldSpace=True, rotatePivot=True)
    curves = []

    for shape in shapes:
        dag_path = get_dag_path(shape)
        curve_fn = om2.MFnNurbsCurve(dag_path)
        curve_points = curve_fn.cvPositions(om2.MSpace.kWorld)
        point_data = [canonical_coordinates_from_world(point, pivot, direction, up_vector) for point in curve_points]
        rational = any(abs(point.w - 1.0) > 1e-6 for point in curve_points)
        curves.append({
            "degree": int(curve_fn.degree),
            "form": curve_form_to_string(curve_fn.form),
            "rational": rational,
            "knots": [float(value) for value in curve_fn.knots()],
            "points": point_data,
        })

    return {
        "template_name": template_name,
        "template_version": 1,
        "base_direction": direction,
        "base_up_vector": up_vector,
        "curve_count": len(curves),
        "curves": curves,
    }


def get_mobject(node_name):
    selection = om2.MSelectionList()
    selection.add(node_name)
    return selection.getDependNode(0)


def curve_form_from_string(form_name):
    value = (form_name or "open").lower()
    if value == "closed":
        return om2.MFnNurbsCurve.kClosed
    if value == "periodic":
        return om2.MFnNurbsCurve.kPeriodic
    return om2.MFnNurbsCurve.kOpen


def point_from_canonical(point_data, direction, up_vector):
    x_axis, y_axis, z_axis = orientation_basis(direction, up_vector)
    x_value = float(point_data[0])
    y_value = float(point_data[1])
    z_value = float(point_data[2])
    w_value = float(point_data[3]) if len(point_data) > 3 else 1.0

    world_x = x_axis[0] * x_value + y_axis[0] * y_value + z_axis[0] * z_value
    world_y = x_axis[1] * x_value + y_axis[1] * y_value + z_axis[1] * z_value
    world_z = x_axis[2] * x_value + y_axis[2] * y_value + z_axis[2] * z_value
    return om2.MPoint(world_x, world_y, world_z, w_value)


def create_curve_shape_from_data(parent_transform, curve_data, direction, up_vector):
    curve_fn = om2.MFnNurbsCurve()
    points = [point_from_canonical(point, direction, up_vector) for point in (curve_data.get("points") or [])]
    knots = [float(value) for value in (curve_data.get("knots") or [])]
    degree = int(curve_data.get("degree", 1))
    form = curve_form_from_string(curve_data.get("form", "open"))
    rational = bool(curve_data.get("rational", False))

    if not points or not knots:
        raise RuntimeError("Template curve data is missing points or knots.")

    created_object = curve_fn.create(points, knots, degree, form, False, rational)
    created_path = om2.MDagPath.getAPathTo(created_object).fullPathName()

    if cmds.nodeType(created_path) == "transform":
        temp_transform = created_path
    else:
        parents = cmds.listRelatives(created_path, parent=True, fullPath=True) or []
        temp_transform = parents[0] if parents else created_path

    temp_shapes = get_shapes(temp_transform)
    if not temp_shapes:
        if cmds.objExists(temp_transform):
            cmds.delete(temp_transform)
        raise RuntimeError("Template curve did not create usable shapes.")

    for shape in temp_shapes:
        cmds.parent(shape, parent_transform, relative=True, shape=True)

    if cmds.objExists(temp_transform):
        cmds.delete(temp_transform)


def create_template_root(name, template_name, direction=DEFAULT_DIRECTION, up_vector=DEFAULT_UP_VECTOR):
    template_data = load_template_data(template_name)
    root = cmds.createNode("transform", name=name)
    curves = template_data.get("curves") or []
    for curve_data in curves:
        create_curve_shape_from_data(root, curve_data, direction, up_vector)
    if not get_shapes(root):
        if cmds.objExists(root):
            cmds.delete(root)
        raise RuntimeError("Template did not create any shapes: {0}".format(template_name))
    return root


class ShapeFactory(object):
    @staticmethod
    def create_circle(name):
        return cmds.circle(name=name, normal=(0, 1, 0), radius=1.0, sections=16, constructionHistory=False)[0]

    @staticmethod
    def create_square(name):
        points = [
            (-1.0, 0.0, -1.0),
            (1.0, 0.0, -1.0),
            (1.0, 0.0, 1.0),
            (-1.0, 0.0, 1.0),
            (-1.0, 0.0, -1.0),
        ]
        return cmds.curve(name=name, degree=1, point=points)

    @staticmethod
    def create_triangle(name):
        points = [
            (0.0, 0.0, 1.15),
            (-1.0, 0.0, -0.75),
            (1.0, 0.0, -0.75),
            (0.0, 0.0, 1.15),
        ]
        return cmds.curve(name=name, degree=1, point=points)

    @staticmethod
    def create_cube(name):
        points = [
            (-1, -1, -1), (1, -1, -1), (1, -1, 1), (-1, -1, 1), (-1, -1, -1),
            (-1, 1, -1), (1, 1, -1), (1, -1, -1), (1, 1, -1), (1, 1, 1),
            (1, -1, 1), (1, 1, 1), (-1, 1, 1), (-1, -1, 1), (-1, 1, 1),
            (-1, 1, -1)
        ]
        return cmds.curve(name=name, degree=1, point=points)

    @staticmethod
    def create_sphere(name):
        parent = cmds.createNode("transform", name=name)
        ring_a = cmds.circle(normal=(1, 0, 0), radius=1.0, sections=16, constructionHistory=False)[0]
        ring_b = cmds.circle(normal=(0, 1, 0), radius=1.0, sections=16, constructionHistory=False)[0]
        ring_c = cmds.circle(normal=(0, 0, 1), radius=1.0, sections=16, constructionHistory=False)[0]
        for ring in (ring_a, ring_b, ring_c):
            parent_shapes(ring, parent)
            cmds.delete(ring)
        return parent

    @staticmethod
    def create_cylinder(name):
        parent = cmds.createNode("transform", name=name)
        radius = 0.9
        half_height = 0.85

        top_ring = cmds.circle(normal=(0, 1, 0), radius=radius, sections=18, constructionHistory=False)[0]
        bottom_ring = cmds.circle(normal=(0, 1, 0), radius=radius, sections=18, constructionHistory=False)[0]
        cmds.move(0, half_height, 0, top_ring, absolute=True)
        cmds.move(0, -half_height, 0, bottom_ring, absolute=True)

        side_a = cmds.curve(degree=1, point=[(radius, -half_height, 0.0), (radius, half_height, 0.0)])
        side_b = cmds.curve(degree=1, point=[(-radius, -half_height, 0.0), (-radius, half_height, 0.0)])
        side_c = cmds.curve(degree=1, point=[(0.0, -half_height, radius), (0.0, half_height, radius)])
        side_d = cmds.curve(degree=1, point=[(0.0, -half_height, -radius), (0.0, half_height, -radius)])

        top_cap_a = cmds.curve(degree=1, point=[(-radius, half_height, 0.0), (radius, half_height, 0.0)])
        top_cap_b = cmds.curve(degree=1, point=[(0.0, half_height, -radius), (0.0, half_height, radius)])
        bottom_cap_a = cmds.curve(degree=1, point=[(-radius, -half_height, 0.0), (radius, -half_height, 0.0)])
        bottom_cap_b = cmds.curve(degree=1, point=[(0.0, -half_height, -radius), (0.0, -half_height, radius)])

        for item in (
            top_ring,
            bottom_ring,
            side_a,
            side_b,
            side_c,
            side_d,
            top_cap_a,
            top_cap_b,
            bottom_cap_a,
            bottom_cap_b,
        ):
            parent_shapes(item, parent)
            cmds.delete(item)
        return parent

    @staticmethod
    def create_pyramid(name):
        points = [
            (0.0, 1.2, 0.0),
            (-1.0, -1.0, 1.0),
            (1.0, -1.0, 1.0),
            (0.0, 1.2, 0.0),
            (1.0, -1.0, -1.0),
            (-1.0, -1.0, -1.0),
            (0.0, 1.2, 0.0),
            (-1.0, -1.0, 1.0),
            (-1.0, -1.0, -1.0),
            (1.0, -1.0, -1.0),
            (1.0, -1.0, 1.0),
            (-1.0, -1.0, 1.0),
        ]
        return cmds.curve(name=name, degree=1, point=points)

    @staticmethod
    def create_arrow(name):
        points = [
            (0.0, 0.0, 1.6),
            (-0.7, 0.0, 0.55),
            (-0.3, 0.0, 0.55),
            (-0.3, 0.0, -1.2),
            (0.3, 0.0, -1.2),
            (0.3, 0.0, 0.55),
            (0.7, 0.0, 0.55),
            (0.0, 0.0, 1.6),
        ]
        return cmds.curve(name=name, degree=1, point=points)

    @staticmethod
    def create_diamond(name):
        points = [
            (0, 1.2, 0), (0.8, 0, 0), (0, -1.2, 0), (-0.8, 0, 0), (0, 1.2, 0),
            (0, 0, 0.8), (0, -1.2, 0), (0, 0, -0.8), (0, 1.2, 0), (0, 0, 0.8),
            (0.8, 0, 0), (0, 0, -0.8), (-0.8, 0, 0), (0, 0, 0.8)
        ]
        return cmds.curve(name=name, degree=1, point=points)

    @staticmethod
    def create_cross(name):
        points = [
            (-0.35, 0.0, 1.0), (0.35, 0.0, 1.0), (0.35, 0.0, 0.35), (1.0, 0.0, 0.35),
            (1.0, 0.0, -0.35), (0.35, 0.0, -0.35), (0.35, 0.0, -1.0), (-0.35, 0.0, -1.0),
            (-0.35, 0.0, -0.35), (-1.0, 0.0, -0.35), (-1.0, 0.0, 0.35), (-0.35, 0.0, 0.35),
            (-0.35, 0.0, 1.0)
        ]
        return cmds.curve(name=name, degree=1, point=points)

    @staticmethod
    def create_gear(name):
        parent = cmds.createNode("transform", name=name)
        outer_points = []
        tooth_count = 10
        root_radius = 0.74
        shoulder_radius = 0.88
        tip_radius = 1.0
        tooth_half_width = 0.10
        shoulder_width = 0.22

        for tooth_index in range(tooth_count):
            center_angle = (math.pi * 2.0) * (float(tooth_index) / float(tooth_count))
            angles_and_radii = [
                (center_angle - shoulder_width, root_radius),
                (center_angle - tooth_half_width, shoulder_radius),
                (center_angle, tip_radius),
                (center_angle + tooth_half_width, shoulder_radius),
                (center_angle + shoulder_width, root_radius),
            ]
            for angle, radius in angles_and_radii:
                outer_points.append((math.cos(angle) * radius, 0.0, math.sin(angle) * radius))

        outer_curve = cmds.curve(degree=3, point=outer_points, name="{0}_outerTmp".format(name))
        outer_curve = cmds.closeCurve(
            outer_curve,
            constructionHistory=False,
            preserveShape=True,
            replaceOriginal=True,
        )[0]

        inner_curve = cmds.circle(
            normal=(0, 1, 0),
            radius=0.34,
            sections=20,
            constructionHistory=False,
            name="{0}_innerTmp".format(name),
        )[0]

        for curve in (outer_curve, inner_curve):
            parent_shapes(curve, parent)
            cmds.delete(curve)
        return parent


SHAPE_BUILDERS = {
    "Circle": ShapeFactory.create_circle,
    "Square": ShapeFactory.create_square,
    "Triangle": ShapeFactory.create_triangle,
    "Cube": ShapeFactory.create_cube,
    "Sphere": ShapeFactory.create_sphere,
    "Pyramid": ShapeFactory.create_pyramid,
    "Arrow": ShapeFactory.create_arrow,
    "Diamond": ShapeFactory.create_diamond,
    "Gear": ShapeFactory.create_gear,
}


class ControllerBuilder(object):
    def __init__(self, rgb_color):
        self.rgb_color = rgb_color

    def create_controller(self, shape_name, target=None, text="", add_text=False,
                          text_scale=DEFAULT_TEXT_SCALE, text_offset=DEFAULT_TEXT_OFFSET,
                          constrain_target=False, direction=DEFAULT_DIRECTION, up_vector=DEFAULT_UP_VECTOR,
                          create_offset_group=DEFAULT_CREATE_OFFSET_GROUP, shape_scale=DEFAULT_SHAPE_SCALE,
                          line_width=DEFAULT_LINE_WIDTH):
        ctrl_name = ctrl_name_from_target(target) if target else unique_name("{0}_CTRL".format(shape_name))
        ctrl = cmds.createNode("transform", name=ctrl_name)
        offset = None

        if create_offset_group:
            offset = cmds.createNode("transform", name=offset_name_from_ctrl(ctrl_name))
            cmds.parent(ctrl, offset)

        self.add_shape(ctrl, shape_name, direction=direction, up_vector=up_vector, shape_scale=shape_scale)

        if add_text and text:
            self.add_text(ctrl, text, scale=text_scale, offset_y=text_offset, direction=direction, up_vector=up_vector)

        apply_rgb_color(ctrl, self.rgb_color)
        apply_line_width(ctrl, line_width)

        if target:
            if offset:
                match_transform(target, offset)
            else:
                match_transform(target, ctrl)
                freeze_transform(ctrl)
            if constrain_target:
                cmds.parentConstraint(ctrl, target, mo=True)
                cmds.scaleConstraint(ctrl, target, mo=True)

        return ctrl, offset

    def add_shape(self, target_ctrl, shape_name, direction=DEFAULT_DIRECTION, up_vector=DEFAULT_UP_VECTOR,
                  shape_scale=DEFAULT_SHAPE_SCALE):
        if shape_name in SHAPE_BUILDERS:
            temp = SHAPE_BUILDERS[shape_name](unique_name("__tempShape"))
            orient_transform(temp, direction, up_vector)
            scale_curve_shapes(temp, shape_scale)
            freeze_transform(temp)
            parent_shapes(temp, target_ctrl)
            cmds.delete(temp)
            return

        if shape_name in template_names():
            temp = create_template_root(unique_name("__tempTemplate"), shape_name, direction=direction, up_vector=up_vector)
            scale_curve_shapes(temp, shape_scale)
            freeze_transform(temp)
            parent_shapes(temp, target_ctrl)
            cmds.delete(temp)
            return

        raise RuntimeError("Unsupported shape: {0}".format(shape_name))

    def create_text_only(self, text, scale=DEFAULT_TEXT_SCALE, offset_y=0.0,
                         target=None, constrain_target=False, direction=DEFAULT_DIRECTION, up_vector=DEFAULT_UP_VECTOR,
                         create_offset_group=DEFAULT_CREATE_OFFSET_GROUP, line_width=DEFAULT_LINE_WIDTH):
        base_name = short_name(target) if target else "Text"
        ctrl_name = unique_name("{0}_CTRL".format(base_name))
        ctrl = cmds.createNode("transform", name=ctrl_name)
        offset = None

        if create_offset_group:
            offset = cmds.createNode("transform", name=offset_name_from_ctrl(ctrl_name))
            cmds.parent(ctrl, offset)

        self.add_text(ctrl, text, scale=scale, offset_y=offset_y, direction=direction, up_vector=up_vector)
        apply_rgb_color(ctrl, self.rgb_color)
        apply_line_width(ctrl, line_width)

        if target:
            if offset:
                match_transform(target, offset)
            else:
                match_transform(target, ctrl)
                freeze_transform(ctrl)
            if constrain_target:
                cmds.parentConstraint(ctrl, target, mo=True)
                cmds.scaleConstraint(ctrl, target, mo=True)

        return ctrl, offset

    def add_text(self, target_ctrl, text, scale=DEFAULT_TEXT_SCALE, offset_y=DEFAULT_TEXT_OFFSET,
                 direction=DEFAULT_DIRECTION, up_vector=DEFAULT_UP_VECTOR):
        text = text.strip()
        if not text:
            return

        result = cmds.textCurves(text=text)
        if not result:
            raise RuntimeError("Could not create text curves.")

        text_root = result[0] if isinstance(result, (list, tuple)) else result
        transforms = get_transforms_with_shapes(text_root)

        if not transforms:
            if cmds.objExists(text_root):
                cmds.delete(text_root)
            raise RuntimeError("No text curve shapes were generated.")

        temp_parent = cmds.createNode("transform", name=unique_name("__tempText"))

        for transform in transforms:
            if not cmds.objExists(transform):
                continue
            try:
                duplicate = cmds.duplicate(transform, rr=True)[0]
                duplicate = cmds.parent(duplicate, world=True)[0]
                cmds.delete(duplicate, constructionHistory=True)
                freeze_transform(duplicate)
                parent_shapes(duplicate, temp_parent)
                cmds.delete(duplicate)
            except Exception:
                continue

        if not get_shapes(temp_parent):
            if cmds.objExists(text_root):
                cmds.delete(text_root)
            if cmds.objExists(temp_parent):
                cmds.delete(temp_parent)
            raise RuntimeError("Text curves could not be rebuilt.")

        components = curve_components(temp_parent)
        if not components:
            if cmds.objExists(text_root):
                cmds.delete(text_root)
            if cmds.objExists(temp_parent):
                cmds.delete(temp_parent)
            raise RuntimeError("Text curves do not contain valid curve shapes.")

        bbox = cmds.exactWorldBoundingBox(temp_parent)
        center_x = (bbox[0] + bbox[3]) * 0.5
        center_y = (bbox[1] + bbox[4]) * 0.5
        center_z = (bbox[2] + bbox[5]) * 0.5

        cmds.move(-center_x, -center_y, -center_z, components, relative=True, worldSpace=True)
        cmds.scale(scale, scale, scale, components, relative=True, pivot=(0.0, 0.0, 0.0))

        resolved_direction, resolved_up = resolve_direction_and_up(direction, up_vector)
        plane_normal = cross_product(AXIS_VECTORS[resolved_direction], AXIS_VECTORS[resolved_up])
        if sum(abs(value) for value in plane_normal) < 0.0001:
            text_direction = resolved_direction
        else:
            text_direction = vector_to_axis_name(plane_normal)

        orient_transform(temp_parent, text_direction, resolved_up)
        if offset_y:
            cmds.move(0.0, offset_y, 0.0, temp_parent, relative=True, objectSpace=True)
        freeze_transform(temp_parent)

        parent_shapes(temp_parent, target_ctrl)

        if cmds.objExists(text_root):
            cmds.delete(text_root)
        if cmds.objExists(temp_parent):
            cmds.delete(temp_parent)

    def replace_shape(self, targets, shape_name, text="", add_text=False,
                      text_scale=DEFAULT_TEXT_SCALE, text_offset=DEFAULT_TEXT_OFFSET,
                      direction=DEFAULT_DIRECTION, up_vector=DEFAULT_UP_VECTOR,
                      shape_scale=DEFAULT_SHAPE_SCALE, line_width=DEFAULT_LINE_WIDTH):
        for target in targets:
            existing_color = get_shape_color(target) or self.rgb_color
            delete_shapes(target)
            self.add_shape(target, shape_name, direction=direction, up_vector=up_vector, shape_scale=shape_scale)
            if add_text and text:
                self.add_text(target, text, scale=text_scale, offset_y=text_offset, direction=direction, up_vector=up_vector)
            apply_rgb_color(target, existing_color)
            apply_line_width(target, line_width)

    def recolor_targets(self, targets):
        for target in targets:
            apply_rgb_color(target, self.rgb_color)



class ControllerToolUI(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(ControllerToolUI, self).__init__(parent)
        self.settings_data = load_tool_settings()
        self.palette_data = load_palette_data()
        self.color_presets = copy.deepcopy(self.palette_data.get("color_presets", FACTORY_COLOR_PRESETS))
        self.user_defaults = copy.deepcopy(self.settings_data.get("user_defaults", factory_settings_data()["user_defaults"]))
        self.display_settings = copy.deepcopy(self.settings_data.get("display_settings", factory_settings_data()["display_settings"]))
        self.template_manager = copy.deepcopy(self.settings_data.get("template_manager", factory_settings_data()["template_manager"]))
        self.promoted_templates = self.sanitized_promoted_templates(self.template_manager.get("promoted_templates", []))
        self.shape_grid_spacing = int(self.display_settings.get("shape_grid_spacing", SHAPE_GRID_SPACING))
        self.swatch_spacing = int(self.display_settings.get("swatch_spacing", FACTORY_SWATCH_SPACING))
        self.icon_button_size = int(self.display_settings.get("icon_button_size", FACTORY_ICON_BUTTON_SIZE))
        self.icon_draw_size = max(24, int(self.icon_button_size * FACTORY_ICON_DRAW_RATIO))
        self.text_button_min_width = max(120, int(self.icon_button_size * 2.05))
        self.swatch_button_size = int(self.display_settings.get("swatch_button_size", FACTORY_SWATCH_SIZE))
        self.current_color_swatch_size = max(20, min(28, int(self.swatch_button_size * 0.55)))
        self.window_width_default = FACTORY_WINDOW_WIDTH
        self.window_height_default = max(int(self.display_settings.get("window_height", FACTORY_WINDOW_HEIGHT)), default_window_height())
        self.custom_palette = [tuple(rgb) for rgb in self.palette_data.get("custom_palette", [])]
        self.recent_colors = [tuple(rgb) for rgb in self.palette_data.get("recent_colors", [])]
        saved_color_state = self.palette_data.get("saved_color_state", {})
        self.saved_color_state = {
            "color_presets": copy.deepcopy(saved_color_state.get("color_presets", self.color_presets)),
            "custom_palette": [tuple(rgb) for rgb in saved_color_state.get("custom_palette", self.custom_palette)],
            "recent_colors": [tuple(rgb) for rgb in saved_color_state.get("recent_colors", self.recent_colors)],
        }
        self.selected_custom_palette_index = -1

        self.setObjectName(WINDOW_OBJECT)
        self.setWindowTitle("{} {}".format(WINDOW_TITLE, VERSION))
        self.setMinimumSize(720, 600)
        self.resize(self.window_width_default, self.window_height_default)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)

        default_rgb = tuple(self.user_defaults.get("rgb", FACTORY_COLOR_PRESETS[DEFAULT_COLOR_NAME]))
        self.current_rgb = default_rgb
        self.builder = ControllerBuilder(self.current_rgb)
        self.shape_buttons = {}
        self.custom_shape_buttons = {}
        self.color_preset_buttons = {}
        self.custom_palette_buttons = {}
        self.recent_color_buttons = {}
        self.icon_cache = {}

        self.build_ui()
        self.apply_styles()
        self.populate_builtin_shape_buttons()
        self.rebuild_custom_shape_buttons()
        self.refresh_template_library_lists()
        self.reset_defaults(silent=True)
        self._last_shape_grid_state = self.current_shape_grid_state()
        self._last_swatch_grid_state = self.current_swatch_grid_state()

    def apply_styles(self):
        self.setStyleSheet("""
            QDialog {
                background-color: #23262d;
                color: #e8ecf3;
            }
            QGroupBox {
                font-weight: 600;
                border: 1px solid #3b414d;
                border-radius: 10px;
                margin-top: 10px;
                padding-top: 12px;
                background-color: #2a2f38;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                top: 2px;
                padding: 0 4px 0 4px;
                color: #f3f6fb;
            }
            QLabel {
                color: #d7dce6;
            }
            QLineEdit, QComboBox, QDoubleSpinBox, QSpinBox {
                background-color: #1f232a;
                border: 1px solid #434b59;
                border-radius: 6px;
                min-height: 26px;
                padding: 4px 8px;
                color: #eef2f7;
            }
            QLineEdit:focus, QComboBox:focus, QDoubleSpinBox:focus, QSpinBox:focus {
                border: 1px solid #6f8cff;
            }
            QPushButton {
                background-color: #394152;
                border: 1px solid #505a6d;
                border-radius: 8px;
                min-height: 28px;
                padding: 5px 10px;
                color: #f3f6fb;
            }
            QPushButton:hover {
                background-color: #455066;
            }
            QPushButton:pressed {
                background-color: #53607b;
            }
            QRadioButton, QCheckBox {
                spacing: 6px;
            }
            QToolButton#shapeButton {
                background-color: #1e2229;
                border: 1px solid #434b59;
                border-radius: 10px;
                padding: 6px;
                color: #e8ecf3;
            }
            QToolButton#shapeButton:hover {
                background-color: #2a303b;
                border: 1px solid #64718a;
            }
            QToolButton#shapeButton:pressed {
                background-color: #323949;
            }
            QToolButton#sectionToggle {
                background-color: transparent;
                border: none;
                color: #f1f5fb;
                font-weight: 600;
                padding: 2px 4px;
            }
            QToolButton#sectionToggle:hover {
                color: #ffffff;
            }
            QPushButton#shapeTextButton {
                text-align: left;
                padding-left: 10px;
            }
            QLabel#sectionSubLabel {
                color: #aab4c4;
                font-size: 11px;
                font-weight: 600;
                letter-spacing: 0.2px;
            }
            QLabel#helperTextLabel {
                color: #98a2b3;
                font-size: 11px;
            }
            QFrame#currentColorSwatch {
                border: none;
                border-radius: 999px;
                background-color: #101318;
            }
            QPushButton#paletteActionButton {
                min-height: 26px;
                padding: 4px 10px;
                border-radius: 7px;
                background-color: #333a47;
                border: 1px solid #4d5667;
            }
            QPushButton#paletteActionButton:hover {
                background-color: #414a5b;
            }
            QSlider::groove:horizontal {
                height: 6px;
                background: #1b1f26;
                border: 1px solid #3a4352;
                border-radius: 3px;
            }
            QSlider::sub-page:horizontal {
                background: #6f8cff;
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                width: 16px;
                margin: -6px 0;
                background: #d9e3ff;
                border: 1px solid #7f93d8;
                border-radius: 8px;
            }
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QWidget#mainScrollWidget {
                background-color: transparent;
            }
        """)

    def build_ui(self):
        outer_layout = QtWidgets.QVBoxLayout(self)
        outer_layout.setSpacing(0)
        outer_layout.setContentsMargins(12, 12, 12, 12)

        self.main_scroll = QtWidgets.QScrollArea()
        self.main_scroll.setWidgetResizable(True)
        self.main_scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.main_scroll.setFrameShape(QtWidgets.QFrame.NoFrame)
        outer_layout.addWidget(self.main_scroll)

        self.main_scroll_widget = QtWidgets.QWidget()
        self.main_scroll_widget.setObjectName("mainScrollWidget")
        self.main_scroll.setWidget(self.main_scroll_widget)

        main_layout = QtWidgets.QVBoxLayout(self.main_scroll_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(0, 0, 0, 0)

        mode_group = QtWidgets.QGroupBox("Mode")
        mode_layout = QtWidgets.QHBoxLayout(mode_group)
        self.create_radio = QtWidgets.QRadioButton("Create")
        self.change_shape_radio = QtWidgets.QRadioButton("Change Shape")
        self.create_radio.setChecked(True)
        mode_layout.addWidget(self.create_radio)
        mode_layout.addWidget(self.change_shape_radio)
        mode_layout.addStretch()
        mode_layout.addWidget(QtWidgets.QLabel("Template View"))
        self.template_view_combo = QtWidgets.QComboBox()
        self.template_view_combo.addItems(["Icons", "Text"])
        self.template_view_combo.currentTextChanged.connect(self.update_shape_view_mode)
        mode_layout.addWidget(self.template_view_combo)
        main_layout.addWidget(mode_group)

        options_group = QtWidgets.QGroupBox("Create Options")
        options_layout = QtWidgets.QGridLayout(options_group)
        options_layout.setContentsMargins(10, 10, 10, 10)
        options_layout.setHorizontalSpacing(8)
        options_layout.setVerticalSpacing(6)
        options_layout.setColumnStretch(1, 1)
        options_layout.setColumnStretch(3, 1)

        self.constraint_checkbox = QtWidgets.QCheckBox("Parent + Scale constrain selected")
        self.constraint_checkbox.setChecked(False)
        options_layout.addWidget(self.constraint_checkbox, 0, 0, 1, 2)

        self.create_offset_checkbox = QtWidgets.QCheckBox("Create Offset Group")
        self.create_offset_checkbox.setChecked(DEFAULT_CREATE_OFFSET_GROUP)
        options_layout.addWidget(self.create_offset_checkbox, 0, 2, 1, 2)

        options_layout.addWidget(QtWidgets.QLabel("Direction"), 1, 0)
        self.direction_combo = QtWidgets.QComboBox()
        self.direction_combo.addItems(AXIS_DISPLAY_ORDER)
        self.direction_combo.setCurrentText(DEFAULT_DIRECTION)
        self.direction_combo.currentTextChanged.connect(self.ensure_valid_orientation_selection)
        options_layout.addWidget(self.direction_combo, 1, 1)

        options_layout.addWidget(QtWidgets.QLabel("Up Vector"), 1, 2)
        self.up_vector_combo = QtWidgets.QComboBox()
        self.up_vector_combo.addItems(AXIS_DISPLAY_ORDER)
        self.up_vector_combo.setCurrentText(DEFAULT_UP_VECTOR)
        self.up_vector_combo.currentTextChanged.connect(self.ensure_valid_orientation_selection)
        options_layout.addWidget(self.up_vector_combo, 1, 3)

        options_layout.addWidget(QtWidgets.QLabel("Shape Scale"), 2, 0)
        self.shape_scale_spin = QtWidgets.QDoubleSpinBox()
        self.shape_scale_spin.setRange(0.05, 100.0)
        self.shape_scale_spin.setSingleStep(0.05)
        self.shape_scale_spin.setDecimals(2)
        self.shape_scale_spin.setValue(DEFAULT_SHAPE_SCALE)
        options_layout.addWidget(self.shape_scale_spin, 2, 1)

        options_layout.addWidget(QtWidgets.QLabel("Line Width"), 2, 2)
        self.line_width_spin = QtWidgets.QDoubleSpinBox()
        self.line_width_spin.setRange(1.0, 10.0)
        self.line_width_spin.setSingleStep(0.1)
        self.line_width_spin.setDecimals(2)
        self.line_width_spin.setValue(DEFAULT_LINE_WIDTH)
        options_layout.addWidget(self.line_width_spin, 2, 3)

        self.reset_button = QtWidgets.QPushButton("Reset UI Settings")
        self.reset_button.clicked.connect(self.reset_defaults)
        options_layout.addWidget(self.reset_button, 3, 2, 1, 2)

        main_layout.addWidget(options_group)

        text_group = QtWidgets.QGroupBox("Text")
        text_group_layout = QtWidgets.QVBoxLayout(text_group)
        text_group_layout.setContentsMargins(10, 8, 10, 10)
        text_group_layout.setSpacing(6)

        text_header_layout = QtWidgets.QHBoxLayout()
        self.text_tools_toggle = QtWidgets.QToolButton()
        self.text_tools_toggle.setObjectName("sectionToggle")
        self.text_tools_toggle.setText("Text Tools")
        self.text_tools_toggle.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.text_tools_toggle.setArrowType(QtCore.Qt.RightArrow)
        self.text_tools_toggle.setCheckable(True)
        self.text_tools_toggle.setChecked(False)
        self.text_tools_toggle.clicked.connect(self.toggle_text_tools_panel)
        text_header_layout.addWidget(self.text_tools_toggle)
        text_header_layout.addStretch()
        text_group_layout.addLayout(text_header_layout)

        self.text_tools_panel = QtWidgets.QWidget()
        text_panel_layout = QtWidgets.QGridLayout(self.text_tools_panel)
        text_panel_layout.setContentsMargins(0, 0, 0, 0)
        text_panel_layout.setHorizontalSpacing(8)
        text_panel_layout.setVerticalSpacing(6)

        self.enable_text_checkbox = QtWidgets.QCheckBox("Add text to shape creation")
        self.enable_text_checkbox.setChecked(DEFAULT_TEXT_ENABLED)
        self.enable_text_checkbox.toggled.connect(self.update_text_controls_enabled)
        text_panel_layout.addWidget(self.enable_text_checkbox, 0, 0, 1, 2)

        text_panel_layout.addWidget(QtWidgets.QLabel("Text"), 1, 0)
        self.text_field = QtWidgets.QLineEdit()
        self.text_field.setPlaceholderText("Optional label")
        text_panel_layout.addWidget(self.text_field, 1, 1)

        text_panel_layout.addWidget(QtWidgets.QLabel("Text Scale"), 2, 0)
        self.text_scale_spin = QtWidgets.QDoubleSpinBox()
        self.text_scale_spin.setRange(0.01, 10.0)
        self.text_scale_spin.setSingleStep(0.05)
        self.text_scale_spin.setValue(DEFAULT_TEXT_SCALE)
        text_panel_layout.addWidget(self.text_scale_spin, 2, 1)

        text_panel_layout.addWidget(QtWidgets.QLabel("Text Offset"), 3, 0)
        self.text_offset_spin = QtWidgets.QDoubleSpinBox()
        self.text_offset_spin.setRange(-100.0, 100.0)
        self.text_offset_spin.setSingleStep(0.1)
        self.text_offset_spin.setValue(DEFAULT_TEXT_OFFSET)
        text_panel_layout.addWidget(self.text_offset_spin, 3, 1)

        self.text_only_button = QtWidgets.QPushButton("Create Text Only")
        self.text_only_button.clicked.connect(self.create_text_only)
        text_panel_layout.addWidget(self.text_only_button, 4, 0, 1, 2)

        self.text_tools_panel.setVisible(False)
        text_group_layout.addWidget(self.text_tools_panel)
        main_layout.addWidget(text_group)

        color_group = QtWidgets.QGroupBox("Color")
        color_layout = QtWidgets.QVBoxLayout(color_group)
        color_layout.setContentsMargins(10, 10, 10, 10)
        color_layout.setSpacing(8)

        color_top_row = QtWidgets.QHBoxLayout()
        color_top_row.setContentsMargins(0, 0, 0, 0)
        color_top_row.setSpacing(8)

        self.current_color_swatch = QtWidgets.QFrame()
        self.current_color_swatch.setObjectName("currentColorSwatch")
        self.current_color_swatch.setFixedSize(self.current_color_swatch_size, self.current_color_swatch_size)
        color_top_row.addWidget(self.current_color_swatch, 0, QtCore.Qt.AlignVCenter)

        current_color_info = QtWidgets.QVBoxLayout()
        current_color_info.setContentsMargins(0, 0, 0, 0)
        current_color_info.setSpacing(2)
        current_color_title = QtWidgets.QLabel("Current Color")
        current_color_title.setObjectName("sectionSubLabel")
        current_color_info.addWidget(current_color_title)
        self.current_color_label = QtWidgets.QLabel("")
        self.current_color_label.setStyleSheet("font-size: 13px; font-weight: 600; color: #ffffff;")
        current_color_info.addWidget(self.current_color_label)
        color_top_row.addLayout(current_color_info, 1)

        self.color_button = QtWidgets.QPushButton("Pick RGB Color")
        self.color_button.clicked.connect(self.pick_color)
        self.color_button.setMinimumHeight(34)
        color_top_row.addWidget(self.color_button, 0, QtCore.Qt.AlignVCenter)
        color_layout.addLayout(color_top_row)

        preset_label = QtWidgets.QLabel("Preset Palette")
        preset_label.setObjectName("sectionSubLabel")
        color_layout.addWidget(preset_label)
        self.preset_swatches_container = QtWidgets.QWidget()
        self.swatch_layout = QtWidgets.QGridLayout(self.preset_swatches_container)
        self.swatch_layout.setContentsMargins(0, 0, 0, 0)
        self.swatch_layout.setHorizontalSpacing(self.swatch_spacing)
        self.swatch_layout.setVerticalSpacing(self.swatch_spacing)
        self.swatch_layout.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        color_layout.addWidget(self.preset_swatches_container)

        custom_label = QtWidgets.QLabel("Custom Palette")
        custom_label.setObjectName("sectionSubLabel")
        color_layout.addWidget(custom_label)
        self.custom_palette_container = QtWidgets.QWidget()
        self.custom_palette_layout = QtWidgets.QGridLayout(self.custom_palette_container)
        self.custom_palette_layout.setContentsMargins(0, 0, 0, 0)
        self.custom_palette_layout.setHorizontalSpacing(self.swatch_spacing)
        self.custom_palette_layout.setVerticalSpacing(self.swatch_spacing)
        self.custom_palette_layout.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        color_layout.addWidget(self.custom_palette_container)

        custom_actions_row = QtWidgets.QHBoxLayout()
        custom_actions_row.setContentsMargins(0, 0, 0, 0)
        custom_actions_row.setSpacing(6)
        self.custom_add_button = QtWidgets.QPushButton("Add Current")
        self.custom_add_button.setObjectName("paletteActionButton")
        self.custom_add_button.clicked.connect(self.add_current_to_custom_palette)
        custom_actions_row.addWidget(self.custom_add_button)
        self.custom_replace_button = QtWidgets.QPushButton("Replace Selected")
        self.custom_replace_button.setObjectName("paletteActionButton")
        self.custom_replace_button.clicked.connect(self.replace_selected_custom_palette_color)
        custom_actions_row.addWidget(self.custom_replace_button)
        self.custom_remove_button = QtWidgets.QPushButton("Remove Selected")
        self.custom_remove_button.setObjectName("paletteActionButton")
        self.custom_remove_button.clicked.connect(self.remove_selected_custom_palette_color)
        custom_actions_row.addWidget(self.custom_remove_button)
        custom_actions_row.addStretch()
        color_layout.addLayout(custom_actions_row)

        recent_label = QtWidgets.QLabel("Recent Colors")
        recent_label.setObjectName("sectionSubLabel")
        color_layout.addWidget(recent_label)
        self.recent_colors_container = QtWidgets.QWidget()
        self.recent_colors_layout = QtWidgets.QGridLayout(self.recent_colors_container)
        self.recent_colors_layout.setContentsMargins(0, 0, 0, 0)
        self.recent_colors_layout.setHorizontalSpacing(self.swatch_spacing)
        self.recent_colors_layout.setVerticalSpacing(self.swatch_spacing)
        self.recent_colors_layout.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        color_layout.addWidget(self.recent_colors_container)
        self.rebuild_all_color_swatches()
        main_layout.addWidget(color_group)

        builtin_group = QtWidgets.QGroupBox("Built-in Shapes")
        builtin_layout = QtWidgets.QVBoxLayout(builtin_group)
        self.builtin_shapes_container = QtWidgets.QWidget()
        self.builtin_shapes_layout = QtWidgets.QGridLayout(self.builtin_shapes_container)
        self.builtin_shapes_layout.setContentsMargins(0, 0, 0, 0)
        self.builtin_shapes_layout.setHorizontalSpacing(self.shape_grid_spacing)
        self.builtin_shapes_layout.setVerticalSpacing(self.shape_grid_spacing)
        self.builtin_shapes_layout.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        builtin_layout.addWidget(self.builtin_shapes_container)
        main_layout.addWidget(builtin_group)

        custom_group = QtWidgets.QGroupBox("Custom Templates")
        custom_layout = QtWidgets.QVBoxLayout(custom_group)
        custom_layout.setSpacing(8)

        custom_header = QtWidgets.QHBoxLayout()
        self.template_count_label = QtWidgets.QLabel("0 templates")
        custom_header.addWidget(self.template_count_label)
        custom_header.addStretch()
        self.refresh_templates_button = QtWidgets.QPushButton("Refresh Templates")
        self.refresh_templates_button.clicked.connect(self.rebuild_custom_shape_buttons)
        custom_header.addWidget(self.refresh_templates_button)
        custom_layout.addLayout(custom_header)

        self.template_folder_label = QtWidgets.QLabel(template_directory())
        self.template_folder_label.setStyleSheet("color: #98a2b3;")
        self.template_folder_label.setWordWrap(True)
        custom_layout.addWidget(self.template_folder_label)

        self.custom_shapes_container = QtWidgets.QWidget()
        self.custom_shapes_layout = QtWidgets.QGridLayout(self.custom_shapes_container)
        self.custom_shapes_layout.setContentsMargins(0, 0, 0, 0)
        self.custom_shapes_layout.setHorizontalSpacing(self.shape_grid_spacing)
        self.custom_shapes_layout.setVerticalSpacing(self.shape_grid_spacing)
        self.custom_shapes_layout.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        custom_layout.addWidget(self.custom_shapes_container)
        main_layout.addWidget(custom_group)

        template_helper_group = QtWidgets.QGroupBox("Template Helper")
        template_helper_layout = QtWidgets.QVBoxLayout(template_helper_group)
        template_helper_layout.setContentsMargins(10, 8, 10, 10)
        template_helper_layout.setSpacing(6)

        helper_header_layout = QtWidgets.QHBoxLayout()
        self.template_helper_toggle = QtWidgets.QToolButton()
        self.template_helper_toggle.setObjectName("sectionToggle")
        self.template_helper_toggle.setText("Template Helper")
        self.template_helper_toggle.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.template_helper_toggle.setArrowType(QtCore.Qt.RightArrow)
        self.template_helper_toggle.setCheckable(True)
        self.template_helper_toggle.setChecked(False)
        self.template_helper_toggle.clicked.connect(self.toggle_template_helper_panel)
        helper_header_layout.addWidget(self.template_helper_toggle)
        helper_header_layout.addStretch()
        template_helper_layout.addLayout(helper_header_layout)

        self.template_helper_panel = QtWidgets.QWidget()
        template_admin_layout = QtWidgets.QGridLayout(self.template_helper_panel)
        template_admin_layout.setContentsMargins(0, 0, 0, 0)
        template_admin_layout.setHorizontalSpacing(8)
        template_admin_layout.setVerticalSpacing(6)

        template_admin_layout.addWidget(QtWidgets.QLabel("Template Name"), 0, 0)
        self.template_name_field = QtWidgets.QLineEdit()
        self.template_name_field.setPlaceholderText("New template name")
        template_admin_layout.addWidget(self.template_name_field, 0, 1)

        self.use_selection_name_button = QtWidgets.QPushButton("Use Selection Name")
        self.use_selection_name_button.clicked.connect(self.use_selection_name_for_template)
        template_admin_layout.addWidget(self.use_selection_name_button, 0, 2)

        template_admin_layout.addWidget(QtWidgets.QLabel("Replace Existing"), 1, 0)
        self.template_overwrite_combo = QtWidgets.QComboBox()
        template_admin_layout.addWidget(self.template_overwrite_combo, 1, 1, 1, 2)

        self.template_save_button = QtWidgets.QPushButton("Create Template From Selected")
        self.template_save_button.clicked.connect(self.create_template_from_selected)
        template_admin_layout.addWidget(self.template_save_button, 2, 0, 1, 2)

        self.template_overwrite_button = QtWidgets.QPushButton("Replace Selected Template")
        self.template_overwrite_button.clicked.connect(self.overwrite_selected_template)
        template_admin_layout.addWidget(self.template_overwrite_button, 2, 2)

        template_hint = QtWidgets.QLabel(
            "Uses the current Direction and Up Vector as the source orientation of the selected curve."
        )
        template_hint.setWordWrap(True)
        template_hint.setObjectName("helperTextLabel")
        template_admin_layout.addWidget(template_hint, 3, 0, 1, 3)

        self.template_helper_panel.setVisible(False)
        template_helper_layout.addWidget(self.template_helper_panel)
        main_layout.addWidget(template_helper_group)

        settings_group = QtWidgets.QGroupBox("Settings")
        settings_layout = QtWidgets.QVBoxLayout(settings_group)
        settings_layout.setContentsMargins(10, 8, 10, 10)
        settings_layout.setSpacing(6)

        settings_header_layout = QtWidgets.QHBoxLayout()
        self.settings_toggle = QtWidgets.QToolButton()
        self.settings_toggle.setObjectName("sectionToggle")
        self.settings_toggle.setText("Settings")
        self.settings_toggle.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.settings_toggle.setArrowType(QtCore.Qt.RightArrow)
        self.settings_toggle.setCheckable(True)
        self.settings_toggle.setChecked(False)
        self.settings_toggle.clicked.connect(self.toggle_settings_panel)
        settings_header_layout.addWidget(self.settings_toggle)
        settings_header_layout.addStretch()
        settings_layout.addLayout(settings_header_layout)

        self.settings_panel = QtWidgets.QWidget()
        settings_panel_layout = QtWidgets.QVBoxLayout(self.settings_panel)
        settings_panel_layout.setContentsMargins(0, 0, 0, 0)
        settings_panel_layout.setSpacing(10)

        display_settings_group = QtWidgets.QGroupBox("Display Settings")
        display_grid = QtWidgets.QGridLayout(display_settings_group)
        display_grid.setHorizontalSpacing(10)
        display_grid.setVerticalSpacing(8)

        display_grid.addWidget(QtWidgets.QLabel("Icon Size"), 0, 0)
        icon_size_row = QtWidgets.QHBoxLayout()
        icon_size_row.setSpacing(8)
        self.icon_size_slider = NoWheelSlider(QtCore.Qt.Horizontal)
        self.icon_size_slider.setRange(48, 128)
        self.icon_size_slider.setValue(self.icon_button_size)
        self.icon_size_slider.valueChanged.connect(self.on_icon_size_slider_changed)
        icon_size_row.addWidget(self.icon_size_slider, 1)
        self.icon_size_spin = QtWidgets.QSpinBox()
        self.icon_size_spin.setRange(48, 128)
        self.icon_size_spin.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.icon_size_spin.setFixedWidth(64)
        self.icon_size_spin.setAlignment(QtCore.Qt.AlignCenter)
        self.icon_size_spin.setValue(self.icon_button_size)
        self.icon_size_spin.valueChanged.connect(self.on_icon_size_spin_changed)
        icon_size_row.addWidget(self.icon_size_spin)
        display_grid.addLayout(icon_size_row, 0, 1)

        display_grid.addWidget(QtWidgets.QLabel("Icon Grid Spacing"), 1, 0)
        icon_spacing_row = QtWidgets.QHBoxLayout()
        icon_spacing_row.setSpacing(8)
        self.icon_spacing_slider = NoWheelSlider(QtCore.Qt.Horizontal)
        self.icon_spacing_slider.setRange(0, 24)
        self.icon_spacing_slider.setValue(self.shape_grid_spacing)
        self.icon_spacing_slider.valueChanged.connect(self.on_icon_spacing_slider_changed)
        icon_spacing_row.addWidget(self.icon_spacing_slider, 1)
        self.icon_spacing_spin = QtWidgets.QSpinBox()
        self.icon_spacing_spin.setRange(0, 24)
        self.icon_spacing_spin.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.icon_spacing_spin.setFixedWidth(64)
        self.icon_spacing_spin.setAlignment(QtCore.Qt.AlignCenter)
        self.icon_spacing_spin.setValue(self.shape_grid_spacing)
        self.icon_spacing_spin.valueChanged.connect(self.on_icon_spacing_spin_changed)
        icon_spacing_row.addWidget(self.icon_spacing_spin)
        display_grid.addLayout(icon_spacing_row, 1, 1)

        display_grid.addWidget(QtWidgets.QLabel("Color Swatch Size"), 2, 0)
        swatch_size_row = QtWidgets.QHBoxLayout()
        swatch_size_row.setSpacing(8)
        self.swatch_size_slider = NoWheelSlider(QtCore.Qt.Horizontal)
        self.swatch_size_slider.setRange(16, 72)
        self.swatch_size_slider.setValue(self.swatch_button_size)
        self.swatch_size_slider.valueChanged.connect(self.on_swatch_size_slider_changed)
        swatch_size_row.addWidget(self.swatch_size_slider, 1)
        self.swatch_size_spin = QtWidgets.QSpinBox()
        self.swatch_size_spin.setRange(16, 72)
        self.swatch_size_spin.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.swatch_size_spin.setFixedWidth(64)
        self.swatch_size_spin.setAlignment(QtCore.Qt.AlignCenter)
        self.swatch_size_spin.setValue(self.swatch_button_size)
        self.swatch_size_spin.valueChanged.connect(self.on_swatch_size_spin_changed)
        swatch_size_row.addWidget(self.swatch_size_spin)
        display_grid.addLayout(swatch_size_row, 2, 1)

        display_grid.addWidget(QtWidgets.QLabel("Color Swatch Spacing"), 3, 0)
        swatch_spacing_row = QtWidgets.QHBoxLayout()
        swatch_spacing_row.setSpacing(8)
        self.swatch_spacing_slider = NoWheelSlider(QtCore.Qt.Horizontal)
        self.swatch_spacing_slider.setRange(0, 20)
        self.swatch_spacing_slider.setValue(self.swatch_spacing)
        self.swatch_spacing_slider.valueChanged.connect(self.on_swatch_spacing_slider_changed)
        swatch_spacing_row.addWidget(self.swatch_spacing_slider, 1)
        self.swatch_spacing_spin = QtWidgets.QSpinBox()
        self.swatch_spacing_spin.setRange(0, 20)
        self.swatch_spacing_spin.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.swatch_spacing_spin.setFixedWidth(64)
        self.swatch_spacing_spin.setAlignment(QtCore.Qt.AlignCenter)
        self.swatch_spacing_spin.setValue(self.swatch_spacing)
        self.swatch_spacing_spin.valueChanged.connect(self.on_swatch_spacing_spin_changed)
        swatch_spacing_row.addWidget(self.swatch_spacing_spin)
        display_grid.addLayout(swatch_spacing_row, 3, 1)
        settings_panel_layout.addWidget(display_settings_group)

        palette_note = QtWidgets.QLabel("Add colors to Custom Palette in the Color section above. Save Color Palettes stores a snapshot of both Custom Palette and Recent Colors.")
        palette_note.setWordWrap(True)
        palette_note.setObjectName("helperTextLabel")
        settings_panel_layout.addWidget(palette_note)

        template_library_group = QtWidgets.QGroupBox("Template Library")
        template_library_layout = QtWidgets.QGridLayout(template_library_group)
        template_library_layout.setHorizontalSpacing(10)
        template_library_layout.setVerticalSpacing(6)
        template_library_layout.addWidget(QtWidgets.QLabel("Standard / Preinstalled"), 0, 0)
        template_library_layout.addWidget(QtWidgets.QLabel("Custom"), 0, 2)

        self.standard_templates_list = QtWidgets.QListWidget()
        self.standard_templates_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.standard_templates_list.setMinimumHeight(120)
        template_library_layout.addWidget(self.standard_templates_list, 1, 0)

        move_buttons_layout = QtWidgets.QVBoxLayout()
        move_buttons_layout.setSpacing(6)
        move_buttons_layout.addStretch()
        self.promote_template_button = QtWidgets.QPushButton("<< Promote")
        self.promote_template_button.clicked.connect(self.promote_selected_templates)
        move_buttons_layout.addWidget(self.promote_template_button)
        self.demote_template_button = QtWidgets.QPushButton("Demote >>")
        self.demote_template_button.clicked.connect(self.demote_selected_templates)
        move_buttons_layout.addWidget(self.demote_template_button)
        self.refresh_template_lists_button = QtWidgets.QPushButton("Refresh")
        self.refresh_template_lists_button.clicked.connect(self.refresh_template_library_lists)
        move_buttons_layout.addWidget(self.refresh_template_lists_button)
        move_buttons_layout.addStretch()
        template_library_layout.addLayout(move_buttons_layout, 1, 1)

        self.custom_templates_list = QtWidgets.QListWidget()
        self.custom_templates_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.custom_templates_list.setMinimumHeight(120)
        template_library_layout.addWidget(self.custom_templates_list, 1, 2)

        template_library_hint = QtWidgets.QLabel("Preinstalled templates always appear with Standard Shapes. Promoted custom templates also show there. Files stay in the custom template folder.")
        template_library_hint.setWordWrap(True)
        template_library_hint.setObjectName("helperTextLabel")
        template_library_layout.addWidget(template_library_hint, 2, 0, 1, 3)
        settings_panel_layout.addWidget(template_library_group)

        defaults_group = QtWidgets.QGroupBox("Defaults")
        defaults_layout = QtWidgets.QVBoxLayout(defaults_group)
        defaults_layout.setSpacing(6)
        self.save_defaults_button = QtWidgets.QPushButton("Save Current Settings As User Defaults")
        self.save_defaults_button.clicked.connect(self.save_current_settings_as_defaults)
        defaults_layout.addWidget(self.save_defaults_button)

        palette_defaults_row = QtWidgets.QHBoxLayout()
        palette_defaults_row.setContentsMargins(0, 0, 0, 0)
        palette_defaults_row.setSpacing(6)
        self.save_palette_defaults_button = QtWidgets.QPushButton("Save Color Palettes")
        self.save_palette_defaults_button.setObjectName("paletteActionButton")
        self.save_palette_defaults_button.clicked.connect(self.save_current_color_state)
        palette_defaults_row.addWidget(self.save_palette_defaults_button)
        self.restore_palette_defaults_button = QtWidgets.QPushButton("Restore Saved Palettes")
        self.restore_palette_defaults_button.setObjectName("paletteActionButton")
        self.restore_palette_defaults_button.clicked.connect(self.restore_saved_color_state)
        palette_defaults_row.addWidget(self.restore_palette_defaults_button)
        defaults_layout.addLayout(palette_defaults_row)

        self.factory_reset_button = QtWidgets.QPushButton("Restore Factory Defaults")
        self.factory_reset_button.clicked.connect(self.restore_factory_defaults)
        defaults_layout.addWidget(self.factory_reset_button)

        factory_note = QtWidgets.QLabel("Factory reset restores UI settings and active palettes. Saved palettes stay available. Custom templates stay untouched.")
        factory_note.setWordWrap(True)
        factory_note.setObjectName("helperTextLabel")
        defaults_layout.addWidget(factory_note)
        settings_panel_layout.addWidget(defaults_group)

        self.settings_panel.setVisible(False)
        settings_layout.addWidget(self.settings_panel)
        main_layout.addWidget(settings_group)

        footer = QtWidgets.QHBoxLayout()
        self.help_button = QtWidgets.QPushButton("Help")
        self.help_button.setMinimumWidth(72)
        self.help_button.clicked.connect(self.show_help_dialog)
        footer.addWidget(self.help_button)
        footer.addStretch()
        self.close_button = QtWidgets.QPushButton("Close")
        self.close_button.clicked.connect(self.close)
        footer.addWidget(self.close_button)
        main_layout.addLayout(footer)

    def expand_window_for_panel(self, panel_widget):
        self.layout().activate()
        QtWidgets.QApplication.processEvents()
        try:
            screen = QtWidgets.QApplication.screenAt(self.frameGeometry().center())
        except AttributeError:
            screen = QtWidgets.QApplication.primaryScreen()
        available_height = screen.availableGeometry().height() if screen else 1200
        max_height = max(available_height - 80, self.minimumHeight())
        target_height = min(self.sizeHint().height() + 8, max_height)
        if target_height > self.height():
            self.resize(self.width(), target_height)

    def toggle_template_helper_panel(self, checked):
        self.template_helper_panel.setVisible(checked)
        self.template_helper_toggle.setArrowType(QtCore.Qt.DownArrow if checked else QtCore.Qt.RightArrow)
        if checked:
            self.expand_window_for_panel(self.template_helper_panel)

    def toggle_text_tools_panel(self, checked):
        self.text_tools_panel.setVisible(checked)
        self.text_tools_toggle.setArrowType(QtCore.Qt.DownArrow if checked else QtCore.Qt.RightArrow)
        if checked:
            self.expand_window_for_panel(self.text_tools_panel)

    def shape_display_mode(self):
        return self.template_view_combo.currentText() if hasattr(self, "template_view_combo") else DEFAULT_SHAPE_DISPLAY_MODE

    def is_icon_display_mode(self):
        return self.shape_display_mode() == "Icons"

    def available_shape_grid_width(self, container):
        candidates = []
        for widget in (container, container.parentWidget() if container is not None else None, self):
            if widget is None:
                continue
            width = widget.width() if hasattr(widget, "width") else 0
            if width and width > 0:
                candidates.append(width)
            if hasattr(widget, "contentsRect"):
                rect = widget.contentsRect()
                if rect.width() > 0:
                    candidates.append(rect.width())
        width = min(candidates) if candidates else 0
        width -= 8
        return max(width, 1)

    def icon_grid_columns(self, container):
        available_width = self.available_shape_grid_width(container)
        step = self.icon_button_size + self.shape_grid_spacing
        columns = max(1, (available_width + self.shape_grid_spacing) // step)
        return max(1, int(columns))

    def text_grid_columns(self, container):
        available_width = self.available_shape_grid_width(container)
        step = self.text_button_min_width + self.shape_grid_spacing
        columns = max(1, (available_width + self.shape_grid_spacing) // step)
        return max(1, int(columns))

    def shape_grid_columns(self, container):
        return self.icon_grid_columns(container) if self.is_icon_display_mode() else self.text_grid_columns(container)

    def swatch_grid_columns(self, container):
        available_width = self.available_shape_grid_width(container)
        step = self.swatch_button_size + self.swatch_spacing
        columns = max(1, (available_width + self.swatch_spacing) // step)
        return max(1, int(columns))

    def current_swatch_grid_state(self):
        return (
            self.swatch_grid_columns(self.preset_swatches_container),
            self.swatch_grid_columns(self.custom_palette_container),
            self.swatch_grid_columns(self.recent_colors_container),
            self.swatch_button_size,
            self.swatch_spacing,
        )

    def update_shape_grid_metrics(self):
        for container in (self.builtin_shapes_container, self.custom_shapes_container):
            container.setMinimumWidth(0)
            container.setMaximumWidth(16777215)
            container.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)

    def current_shape_grid_state(self):
        return (
            self.shape_grid_columns(self.builtin_shapes_container),
            self.shape_grid_columns(self.custom_shapes_container),
            self.shape_display_mode(),
        )

    def sanitized_promoted_templates(self, names=None):
        source = names if names is not None else getattr(self, "promoted_templates", [])
        existing = set(template_names())
        cleaned = []
        for name in source:
            safe_name = sanitize_template_name(name)
            if not safe_name or safe_name in BUILTIN_SHAPE_NAMES or safe_name not in existing or safe_name in cleaned:
                continue
            cleaned.append(safe_name)
        return cleaned

    def standard_shape_names(self):
        names = list(BUILTIN_SHAPE_NAMES)
        names.extend(preinstalled_template_names())
        for name in self.sanitized_promoted_templates():
            if name not in names:
                names.append(name)
        return names

    def custom_shape_names(self):
        promoted = set(self.sanitized_promoted_templates())
        return [name for name in custom_template_names() if name not in promoted]


    def update_shape_view_mode(self, *args):
        self.update_shape_grid_metrics()
        self.populate_builtin_shape_buttons()
        self.rebuild_custom_shape_buttons()
        self._last_shape_grid_state = self.current_shape_grid_state()

    def resizeEvent(self, event):
        super(ControllerToolUI, self).resizeEvent(event)
        current_shape_state = self.current_shape_grid_state()
        current_swatch_state = self.current_swatch_grid_state()
        if getattr(self, "_last_shape_grid_state", None) != current_shape_state:
            self.update_shape_grid_metrics()
            self.populate_builtin_shape_buttons()
            self.rebuild_custom_shape_buttons()
            self._last_shape_grid_state = current_shape_state
        if getattr(self, "_last_swatch_grid_state", None) != current_swatch_state:
            self.rebuild_all_color_swatches()
            self._last_swatch_grid_state = current_swatch_state

    def make_shape_button(self, shape_name):
        if self.is_icon_display_mode():
            button = QtWidgets.QToolButton()
            button.setObjectName("shapeButton")
            button.setFixedSize(self.icon_button_size, self.icon_button_size)
            button.setIconSize(QtCore.QSize(self.icon_draw_size, self.icon_draw_size))
            button.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
            button.setToolTip(shape_name)
            button.setIcon(self.create_shape_icon(shape_name))
        else:
            button = QtWidgets.QPushButton(shape_name)
            button.setObjectName("shapeTextButton")
            button.setMinimumWidth(self.text_button_min_width)
            button.setMaximumWidth(16777215)
            button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
            button.setMinimumHeight(32)
            button.setToolTip(shape_name)
        button.clicked.connect(lambda checked=False, name=shape_name: self.handle_shape_click(name))
        return button

    def populate_builtin_shape_buttons(self):
        while self.builtin_shapes_layout.count():
            item = self.builtin_shapes_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        self.shape_buttons = {}

        row = 0
        column = 0
        for shape_name in self.standard_shape_names():
            button = self.make_shape_button(shape_name)
            self.shape_buttons[shape_name] = button
            self.builtin_shapes_layout.addWidget(button, row, column, QtCore.Qt.AlignLeft)
            column += 1
            if column >= self.shape_grid_columns(self.builtin_shapes_container):
                column = 0
                row += 1

    def rebuild_custom_shape_buttons(self):
        while self.custom_shapes_layout.count():
            item = self.custom_shapes_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        self.custom_shape_buttons = {}

        names = self.custom_shape_names()
        row = 0
        column = 0
        if not names:
            label = QtWidgets.QLabel("No custom templates found yet.")
            label.setObjectName("helperTextLabel")
            self.custom_shapes_layout.addWidget(label, 0, 0)
        else:
            for shape_name in names:
                button = self.make_shape_button(shape_name)
                self.custom_shape_buttons[shape_name] = button
                self.custom_shapes_layout.addWidget(button, row, column, QtCore.Qt.AlignLeft)
                column += 1
                if column >= self.shape_grid_columns(self.custom_shapes_container):
                    column = 0
                    row += 1

        template_count = len(names)
        self.template_count_label.setText("{0} template{1}".format(template_count, "" if template_count == 1 else "s"))
        self.template_folder_label.setText(template_directory())
        self.refresh_template_overwrite_combo(custom_template_names())
        if hasattr(self, "standard_templates_list"):
            self.refresh_template_library_lists()

    def rebuild_all_color_swatches(self):
        self.rebuild_preset_swatches()
        self.rebuild_custom_palette_swatches()
        self.rebuild_recent_color_swatches()
        self.refresh_color_ui(selected_name=self.matching_preset_name(self.current_rgb))

    def clear_layout_widgets(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def create_color_swatch_button(self, rgb, tooltip, callback):
        button = QtWidgets.QToolButton()
        button.setAutoRaise(False)
        button.setFixedSize(self.swatch_button_size, self.swatch_button_size)
        button.setToolTip(tooltip)
        button.clicked.connect(callback)
        return button

    def rebuild_preset_swatches(self):
        self.clear_layout_widgets(self.swatch_layout)
        self.color_preset_buttons = {}
        self.swatch_layout.setHorizontalSpacing(self.swatch_spacing)
        self.swatch_layout.setVerticalSpacing(self.swatch_spacing)
        columns = self.swatch_grid_columns(self.preset_swatches_container)
        row = 0
        column = 0
        for preset_name in self.color_presets.keys():
            button = self.create_color_swatch_button(
                self.color_presets[preset_name],
                preset_name,
                lambda checked=False, name=preset_name: self.set_preset_color(name, auto_apply=True),
            )
            self.color_preset_buttons[preset_name] = button
            self.swatch_layout.addWidget(button, row, column)
            column += 1
            if column >= columns:
                column = 0
                row += 1

    def rebuild_custom_palette_swatches(self):
        self.clear_layout_widgets(self.custom_palette_layout)
        self.custom_palette_buttons = {}
        self.custom_palette_layout.setHorizontalSpacing(self.swatch_spacing)
        self.custom_palette_layout.setVerticalSpacing(self.swatch_spacing)
        columns = self.swatch_grid_columns(self.custom_palette_container)
        row = 0
        column = 0
        for index, rgb in enumerate(self.custom_palette):
            tooltip = "Custom {0}: {1}".format(index + 1, self.color_to_hex(rgb))
            button = self.create_color_swatch_button(
                rgb,
                tooltip,
                lambda checked=False, idx=index: self.select_custom_palette_color(idx, auto_apply=True),
            )
            self.custom_palette_buttons[index] = button
            self.custom_palette_layout.addWidget(button, row, column)
            column += 1
            if column >= columns:
                column = 0
                row += 1
        if not self.custom_palette:
            label = QtWidgets.QLabel("No custom colors yet. Pick a color and press Add Current.")
            label.setObjectName("helperTextLabel")
            self.custom_palette_layout.addWidget(label, 0, 0, 1, max(1, columns))

    def rebuild_recent_color_swatches(self):
        self.clear_layout_widgets(self.recent_colors_layout)
        self.recent_color_buttons = {}
        self.recent_colors_layout.setHorizontalSpacing(self.swatch_spacing)
        self.recent_colors_layout.setVerticalSpacing(self.swatch_spacing)
        columns = self.swatch_grid_columns(self.recent_colors_container)
        row = 0
        column = 0
        for index, rgb in enumerate(self.recent_colors):
            tooltip = "Recent {0}: {1}".format(index + 1, self.color_to_hex(rgb))
            button = self.create_color_swatch_button(
                rgb,
                tooltip,
                lambda checked=False, idx=index: self.select_recent_color(idx, auto_apply=True),
            )
            self.recent_color_buttons[index] = button
            self.recent_colors_layout.addWidget(button, row, column)
            column += 1
            if column >= columns:
                column = 0
                row += 1
        if not self.recent_colors:
            label = QtWidgets.QLabel("Recent colors will appear here.")
            label.setObjectName("helperTextLabel")
            self.recent_colors_layout.addWidget(label, 0, 0, 1, max(1, columns))

    def matching_preset_name(self, rgb):
        for preset_name, preset_rgb in self.color_presets.items():
            if all(abs(a - b) < 0.0001 for a, b in zip(preset_rgb, rgb)):
                return preset_name
        return None

    def on_icon_size_slider_changed(self, value):
        if hasattr(self, "icon_size_spin") and self.icon_size_spin.value() != value:
            blocker = QtCore.QSignalBlocker(self.icon_size_spin)
            self.icon_size_spin.setValue(value)
            del blocker
        self.apply_display_settings_preview()

    def on_icon_size_spin_changed(self, value):
        if hasattr(self, "icon_size_slider") and self.icon_size_slider.value() != value:
            blocker = QtCore.QSignalBlocker(self.icon_size_slider)
            self.icon_size_slider.setValue(value)
            del blocker
        self.apply_display_settings_preview()

    def on_icon_spacing_slider_changed(self, value):
        if hasattr(self, "icon_spacing_spin") and self.icon_spacing_spin.value() != value:
            blocker = QtCore.QSignalBlocker(self.icon_spacing_spin)
            self.icon_spacing_spin.setValue(value)
            del blocker
        self.apply_display_settings_preview()

    def on_icon_spacing_spin_changed(self, value):
        if hasattr(self, "icon_spacing_slider") and self.icon_spacing_slider.value() != value:
            blocker = QtCore.QSignalBlocker(self.icon_spacing_slider)
            self.icon_spacing_slider.setValue(value)
            del blocker
        self.apply_display_settings_preview()

    def on_swatch_size_slider_changed(self, value):
        if hasattr(self, "swatch_size_spin") and self.swatch_size_spin.value() != value:
            blocker = QtCore.QSignalBlocker(self.swatch_size_spin)
            self.swatch_size_spin.setValue(value)
            del blocker
        self.apply_display_settings_preview()

    def on_swatch_size_spin_changed(self, value):
        if hasattr(self, "swatch_size_slider") and self.swatch_size_slider.value() != value:
            blocker = QtCore.QSignalBlocker(self.swatch_size_slider)
            self.swatch_size_slider.setValue(value)
            del blocker
        self.apply_display_settings_preview()

    def on_swatch_spacing_slider_changed(self, value):
        if hasattr(self, "swatch_spacing_spin") and self.swatch_spacing_spin.value() != value:
            blocker = QtCore.QSignalBlocker(self.swatch_spacing_spin)
            self.swatch_spacing_spin.setValue(value)
            del blocker
        self.apply_display_settings_preview()

    def on_swatch_spacing_spin_changed(self, value):
        if hasattr(self, "swatch_spacing_slider") and self.swatch_spacing_slider.value() != value:
            blocker = QtCore.QSignalBlocker(self.swatch_spacing_slider)
            self.swatch_spacing_slider.setValue(value)
            del blocker
        self.apply_display_settings_preview()

    def apply_display_settings_preview(self, *args):
        self.shape_grid_spacing = int(self.icon_spacing_spin.value()) if hasattr(self, "icon_spacing_spin") else self.shape_grid_spacing
        self.swatch_spacing = int(self.swatch_spacing_spin.value()) if hasattr(self, "swatch_spacing_spin") else self.swatch_spacing
        self.icon_button_size = int(self.icon_size_spin.value()) if hasattr(self, "icon_size_spin") else self.icon_button_size
        self.swatch_button_size = int(self.swatch_size_spin.value()) if hasattr(self, "swatch_size_spin") else self.swatch_button_size
        self.current_color_swatch_size = max(20, min(28, int(self.swatch_button_size * 0.55)))
        self.icon_draw_size = max(12, int(self.icon_button_size * FACTORY_ICON_DRAW_RATIO))
        self.text_button_min_width = max(96, int(self.icon_button_size * 2.05))

        self.current_color_swatch.setFixedSize(self.current_color_swatch_size, self.current_color_swatch_size)
        self.builtin_shapes_layout.setHorizontalSpacing(self.shape_grid_spacing)
        self.builtin_shapes_layout.setVerticalSpacing(self.shape_grid_spacing)
        self.custom_shapes_layout.setHorizontalSpacing(self.shape_grid_spacing)
        self.custom_shapes_layout.setVerticalSpacing(self.shape_grid_spacing)
        self.invalidate_icon_cache()
        self.rebuild_all_color_swatches()
        self.update_shape_grid_metrics()
        self.populate_builtin_shape_buttons()
        self.rebuild_custom_shape_buttons()
        self._last_shape_grid_state = self.current_shape_grid_state()
        self._last_swatch_grid_state = self.current_swatch_grid_state()

    def select_custom_palette_color(self, index, auto_apply=False):
        if index < 0 or index >= len(self.custom_palette):
            return
        self.selected_custom_palette_index = index
        self.set_current_rgb(self.custom_palette[index], selected_name=None, update_recent=True, auto_apply=auto_apply)

    def select_recent_color(self, index, auto_apply=False):
        if index < 0 or index >= len(self.recent_colors):
            return
        self.selected_custom_palette_index = -1
        self.set_current_rgb(self.recent_colors[index], selected_name=None, update_recent=True, auto_apply=auto_apply)

    def add_current_to_custom_palette(self):
        rgb = tuple(self.current_rgb)
        if rgb in self.custom_palette:
            self.selected_custom_palette_index = self.custom_palette.index(rgb)
            self.rebuild_all_color_swatches()
            cmds.inViewMessage(amg="Color already exists in Custom Palette.", pos="botLeft", fade=True)
            return
        if len(self.custom_palette) >= CUSTOM_PALETTE_LIMIT:
            cmds.warning("Custom Palette is full. Remove or replace a color first.")
            return
        self.custom_palette.append(rgb)
        self.selected_custom_palette_index = len(self.custom_palette) - 1
        self.sync_settings_to_disk()
        self.rebuild_all_color_swatches()
        cmds.inViewMessage(amg="Added color to <hl>Custom Palette</hl>.", pos="botLeft", fade=True)

    def replace_selected_custom_palette_color(self):
        if self.selected_custom_palette_index < 0 or self.selected_custom_palette_index >= len(self.custom_palette):
            cmds.warning("Select a color in Custom Palette first.")
            return
        self.custom_palette[self.selected_custom_palette_index] = tuple(self.current_rgb)
        self.sync_settings_to_disk()
        self.rebuild_all_color_swatches()
        cmds.inViewMessage(amg="Custom Palette color updated.", pos="botLeft", fade=True)

    def remove_selected_custom_palette_color(self):
        if self.selected_custom_palette_index < 0 or self.selected_custom_palette_index >= len(self.custom_palette):
            cmds.warning("Select a color in Custom Palette first.")
            return
        self.custom_palette.pop(self.selected_custom_palette_index)
        self.selected_custom_palette_index = -1
        self.sync_settings_to_disk()
        self.rebuild_all_color_swatches()
        cmds.inViewMessage(amg="Removed color from <hl>Custom Palette</hl>.", pos="botLeft", fade=True)

    def refresh_template_library_lists(self):
        self.promoted_templates = self.sanitized_promoted_templates()
        self.template_manager["promoted_templates"] = list(self.promoted_templates)
        standard_names = list(preinstalled_template_names())
        for name in self.promoted_templates:
            if name not in standard_names:
                standard_names.append(name)
        custom_names = self.custom_shape_names()
        self.standard_templates_list.clear()
        self.standard_templates_list.addItems(standard_names)
        self.custom_templates_list.clear()
        self.custom_templates_list.addItems(custom_names)

    def promote_selected_templates(self):
        names = [item.text() for item in self.custom_templates_list.selectedItems()]
        if not names:
            cmds.warning("Select one or more custom templates to promote.")
            return
        changed = False
        for name in names:
            safe_name = sanitize_template_name(name)
            if safe_name and safe_name not in self.promoted_templates and safe_name in template_names():
                self.promoted_templates.append(safe_name)
                changed = True
        if not changed:
            return
        self.promoted_templates = self.sanitized_promoted_templates(self.promoted_templates)
        self.template_manager["promoted_templates"] = list(self.promoted_templates)
        self.sync_settings_to_disk()
        self.populate_builtin_shape_buttons()
        self.rebuild_custom_shape_buttons()
        self.refresh_template_library_lists()

    def demote_selected_templates(self):
        names = [item.text() for item in self.standard_templates_list.selectedItems()]
        if not names:
            cmds.warning("Select one or more promoted custom templates to move back to Custom.")
            return
        target_names = set(sanitize_template_name(name) for name in names)
        new_list = [name for name in self.promoted_templates if name not in target_names]
        if new_list == self.promoted_templates:
            return
        self.promoted_templates = self.sanitized_promoted_templates(new_list)
        self.template_manager["promoted_templates"] = list(self.promoted_templates)
        self.sync_settings_to_disk()
        self.populate_builtin_shape_buttons()
        self.rebuild_custom_shape_buttons()
        self.refresh_template_library_lists()

    def toggle_settings_panel(self, checked):
        self.settings_panel.setVisible(checked)
        self.settings_toggle.setArrowType(QtCore.Qt.DownArrow if checked else QtCore.Qt.RightArrow)
        if checked:
            self.expand_window_for_panel(self.settings_panel)

    def current_user_defaults_snapshot(self):
        return {
            "constraint": self.constraint_checkbox.isChecked(),
            "create_offset_group": self.create_offset_checkbox.isChecked(),
            "direction": self.current_direction(),
            "up_vector": self.current_up_vector(),
            "shape_display_mode": self.template_view_combo.currentText(),
            "shape_scale": self.shape_scale_spin.value(),
            "line_width": self.line_width_spin.value(),
            "text_enabled": self.enable_text_checkbox.isChecked(),
            "text_scale": self.text_scale_spin.value(),
            "text_offset": self.text_offset_spin.value(),
            "rgb": [self.current_rgb[0], self.current_rgb[1], self.current_rgb[2]],
        }

    def current_display_settings_snapshot(self):
        return {
            "shape_grid_spacing": int(self.icon_spacing_spin.value()) if hasattr(self, "icon_spacing_spin") else self.shape_grid_spacing,
            "swatch_spacing": int(self.swatch_spacing_spin.value()) if hasattr(self, "swatch_spacing_spin") else self.swatch_spacing,
            "icon_button_size": int(self.icon_size_spin.value()) if hasattr(self, "icon_size_spin") else self.icon_button_size,
            "swatch_button_size": self.swatch_button_size,
            "window_height": int(self.height()),
        }

    def sync_settings_to_disk(self):
        self.template_manager["promoted_templates"] = list(self.sanitized_promoted_templates())
        self.settings_data = {
            "display_settings": copy.deepcopy(self.display_settings),
            "user_defaults": copy.deepcopy(self.user_defaults),
            "template_manager": copy.deepcopy(self.template_manager),
        }
        self.settings_data = save_tool_settings(self.settings_data)

        self.palette_data = {
            "color_presets": copy.deepcopy(self.color_presets),
            "custom_palette": [list(rgb) for rgb in self.custom_palette],
            "recent_colors": [list(rgb) for rgb in self.recent_colors],
            "saved_color_state": {
                "color_presets": copy.deepcopy(self.saved_color_state.get("color_presets", self.color_presets)),
                "custom_palette": [list(rgb) for rgb in self.saved_color_state.get("custom_palette", self.custom_palette)],
                "recent_colors": [list(rgb) for rgb in self.saved_color_state.get("recent_colors", self.recent_colors)],
            },
        }
        self.palette_data = save_palette_data(self.palette_data)

        self.user_defaults = copy.deepcopy(self.settings_data.get("user_defaults", factory_settings_data()["user_defaults"]))
        self.display_settings = copy.deepcopy(self.settings_data.get("display_settings", factory_settings_data()["display_settings"]))
        self.template_manager = copy.deepcopy(self.settings_data.get("template_manager", factory_settings_data()["template_manager"]))
        self.promoted_templates = self.sanitized_promoted_templates(self.template_manager.get("promoted_templates", []))
        self.color_presets = copy.deepcopy(self.palette_data.get("color_presets", FACTORY_COLOR_PRESETS))
        self.custom_palette = [tuple(rgb) for rgb in self.palette_data.get("custom_palette", [])]
        self.recent_colors = [tuple(rgb) for rgb in self.palette_data.get("recent_colors", [])]
        saved_color_state = self.palette_data.get("saved_color_state", {})
        self.saved_color_state = {
            "color_presets": copy.deepcopy(saved_color_state.get("color_presets", self.color_presets)),
            "custom_palette": [tuple(rgb) for rgb in saved_color_state.get("custom_palette", self.custom_palette)],
            "recent_colors": [tuple(rgb) for rgb in saved_color_state.get("recent_colors", self.recent_colors)],
        }

    def on_preset_edit_combo_changed(self, preset_name):
        pass

    def save_or_update_preset(self):
        pass

    def delete_selected_preset(self):
        pass

    def save_current_settings_as_defaults(self):
        self.display_settings = self.current_display_settings_snapshot()
        self.user_defaults = self.current_user_defaults_snapshot()
        self.sync_settings_to_disk()
        cmds.inViewMessage(amg="User defaults saved.", pos="botLeft", fade=True)


    def save_current_color_state(self):
        self.saved_color_state = {
            "color_presets": copy.deepcopy(self.color_presets),
            "custom_palette": [tuple(rgb) for rgb in self.custom_palette],
            "recent_colors": [tuple(rgb) for rgb in self.recent_colors],
        }
        self.sync_settings_to_disk()
        cmds.inViewMessage(amg="Color palettes snapshot saved.", pos="botLeft", fade=True)

    def restore_saved_color_state(self):
        saved = copy.deepcopy(getattr(self, "saved_color_state", None) or {})
        self.color_presets = copy.deepcopy(saved.get("color_presets", FACTORY_COLOR_PRESETS))
        self.custom_palette = [tuple(rgb) for rgb in saved.get("custom_palette", [])]
        self.recent_colors = [tuple(rgb) for rgb in saved.get("recent_colors", [])]
        self.selected_custom_palette_index = -1

        palette_payload = {
            "color_presets": copy.deepcopy(self.color_presets),
            "custom_palette": [list(rgb) for rgb in self.custom_palette],
            "recent_colors": [list(rgb) for rgb in self.recent_colors],
            "saved_color_state": {
                "color_presets": copy.deepcopy(saved.get("color_presets", self.color_presets)),
                "custom_palette": [list(rgb) for rgb in saved.get("custom_palette", self.custom_palette)],
                "recent_colors": [list(rgb) for rgb in saved.get("recent_colors", self.recent_colors)],
            },
        }
        self.palette_data = save_palette_data(palette_payload)
        self.rebuild_all_color_swatches()
        self.refresh_color_ui()
        cmds.inViewMessage(amg="Saved palettes restored to Custom Palette and Recent Colors.", pos="botLeft", fade=True)

    def restore_factory_defaults(self):
        saved_color_state = copy.deepcopy(getattr(self, "saved_color_state", factory_palette_data()["saved_color_state"]))

        self.settings_data = factory_settings_data()
        save_tool_settings(self.settings_data)

        self.palette_data = factory_palette_data()
        self.palette_data["saved_color_state"] = {
            "color_presets": copy.deepcopy(saved_color_state.get("color_presets", FACTORY_COLOR_PRESETS)),
            "custom_palette": [list(rgb) for rgb in saved_color_state.get("custom_palette", [])],
            "recent_colors": [list(rgb) for rgb in saved_color_state.get("recent_colors", [])],
        }
        self.palette_data = save_palette_data(self.palette_data)

        self.color_presets = copy.deepcopy(self.palette_data["color_presets"])
        self.user_defaults = copy.deepcopy(self.settings_data["user_defaults"])
        self.display_settings = copy.deepcopy(self.settings_data["display_settings"])
        self.template_manager = copy.deepcopy(self.settings_data.get("template_manager", factory_settings_data()["template_manager"]))
        self.promoted_templates = self.sanitized_promoted_templates(self.template_manager.get("promoted_templates", []))
        self.custom_palette = [tuple(rgb) for rgb in self.palette_data.get("custom_palette", [])]
        self.recent_colors = [tuple(rgb) for rgb in self.palette_data.get("recent_colors", [])]
        saved_state = self.palette_data.get("saved_color_state", {})
        self.saved_color_state = {
            "color_presets": copy.deepcopy(saved_state.get("color_presets", FACTORY_COLOR_PRESETS)),
            "custom_palette": [tuple(rgb) for rgb in saved_state.get("custom_palette", [])],
            "recent_colors": [tuple(rgb) for rgb in saved_state.get("recent_colors", [])],
        }
        self.selected_custom_palette_index = -1
        self.invalidate_icon_cache()
        self.apply_saved_defaults_to_ui(silent=True)
        cmds.inViewMessage(amg="Factory defaults restored.", pos="botLeft", fade=True)

    def apply_saved_defaults_to_ui(self, silent=False):
        display = copy.deepcopy(self.display_settings)
        user_defaults = copy.deepcopy(self.user_defaults)

        if hasattr(self, "icon_size_spin"):
            value = int(display.get("icon_button_size", FACTORY_ICON_BUTTON_SIZE))
            blocker = QtCore.QSignalBlocker(self.icon_size_spin)
            self.icon_size_spin.setValue(value)
            del blocker
            if hasattr(self, "icon_size_slider"):
                blocker = QtCore.QSignalBlocker(self.icon_size_slider)
                self.icon_size_slider.setValue(value)
                del blocker
        self.swatch_button_size = int(display.get("swatch_button_size", FACTORY_SWATCH_SIZE))
        if hasattr(self, "icon_spacing_slider"):
            blocker = QtCore.QSignalBlocker(self.icon_spacing_slider)
            self.icon_spacing_slider.setValue(int(display.get("shape_grid_spacing", SHAPE_GRID_SPACING)))
            del blocker
        if hasattr(self, "icon_spacing_spin"):
            blocker = QtCore.QSignalBlocker(self.icon_spacing_spin)
            self.icon_spacing_spin.setValue(int(display.get("shape_grid_spacing", SHAPE_GRID_SPACING)))
            del blocker
        if hasattr(self, "swatch_size_slider"):
            blocker = QtCore.QSignalBlocker(self.swatch_size_slider)
            self.swatch_size_slider.setValue(int(display.get("swatch_button_size", FACTORY_SWATCH_SIZE)))
            del blocker
        if hasattr(self, "swatch_size_spin"):
            blocker = QtCore.QSignalBlocker(self.swatch_size_spin)
            self.swatch_size_spin.setValue(int(display.get("swatch_button_size", FACTORY_SWATCH_SIZE)))
            del blocker
        if hasattr(self, "swatch_spacing_slider"):
            blocker = QtCore.QSignalBlocker(self.swatch_spacing_slider)
            self.swatch_spacing_slider.setValue(int(display.get("swatch_spacing", FACTORY_SWATCH_SPACING)))
            del blocker
        if hasattr(self, "swatch_spacing_spin"):
            blocker = QtCore.QSignalBlocker(self.swatch_spacing_spin)
            self.swatch_spacing_spin.setValue(int(display.get("swatch_spacing", FACTORY_SWATCH_SPACING)))
            del blocker
        self.apply_display_settings_preview()
        target_height = max(int(display.get("window_height", FACTORY_WINDOW_HEIGHT)), default_window_height())
        self.resize(self.width(), target_height)

        self.create_radio.setChecked(True)
        self.constraint_checkbox.setChecked(bool(user_defaults.get("constraint", False)))
        self.create_offset_checkbox.setChecked(bool(user_defaults.get("create_offset_group", DEFAULT_CREATE_OFFSET_GROUP)))
        self.direction_combo.setCurrentText(str(user_defaults.get("direction", DEFAULT_DIRECTION)))
        self.up_vector_combo.setCurrentText(str(user_defaults.get("up_vector", DEFAULT_UP_VECTOR)))
        self.template_view_combo.setCurrentText(str(user_defaults.get("shape_display_mode", DEFAULT_SHAPE_DISPLAY_MODE)))
        self.shape_scale_spin.setValue(float(user_defaults.get("shape_scale", DEFAULT_SHAPE_SCALE)))
        self.line_width_spin.setValue(float(user_defaults.get("line_width", DEFAULT_LINE_WIDTH)))
        self.enable_text_checkbox.setChecked(bool(user_defaults.get("text_enabled", DEFAULT_TEXT_ENABLED)))
        self.text_field.clear()
        self.text_scale_spin.setValue(float(user_defaults.get("text_scale", DEFAULT_TEXT_SCALE)))
        self.text_offset_spin.setValue(float(user_defaults.get("text_offset", DEFAULT_TEXT_OFFSET)))
        self.current_rgb = tuple(user_defaults.get("rgb", FACTORY_COLOR_PRESETS[DEFAULT_COLOR_NAME]))
        self.builder.rgb_color = self.current_rgb
        self.selected_custom_palette_index = -1
        self.rebuild_all_color_swatches()
        self.toggle_text_tools_panel(False)
        self.text_tools_toggle.setChecked(False)
        self.toggle_template_helper_panel(False)
        self.template_helper_toggle.setChecked(False)
        self.toggle_settings_panel(False)
        self.settings_toggle.setChecked(False)
        self.update_text_controls_enabled(self.enable_text_checkbox.isChecked())
        if not silent:
            cmds.inViewMessage(amg="UI settings reset.", pos="botLeft", fade=True)

    def default_template_name_from_selection(self):
        roots = selected_root_transforms()
        if not roots:
            return ""
        return sanitize_template_name(short_name(roots[0]))

    def use_selection_name_for_template(self):
        name = self.default_template_name_from_selection()
        if not name:
            cmds.warning("Select a curve control first.")
            return
        self.template_name_field.setText(name)

    def create_template_from_selected(self):
        template_name = sanitize_template_name(self.template_name_field.text())
        if not template_name:
            template_name = self.default_template_name_from_selection()
            self.template_name_field.setText(template_name)
        if not template_name:
            cmds.warning("Enter a template name or select a curve control.")
            return
        if template_name in BUILTIN_SHAPE_NAMES:
            cmds.warning("That name is reserved by a built-in shape.")
            return
        if os.path.exists(template_file_path(template_name)):
            cmds.warning("Template already exists. Use Replace Selected Template to overwrite it.")
            return

        try:
            cmds.undoInfo(openChunk=True)
            data = collect_template_data_from_selection(template_name, self.current_direction(), self.current_up_vector())
            save_template_data(template_name, data)
            self.invalidate_icon_cache(template_name)
            self.rebuild_custom_shape_buttons()
            self.template_overwrite_combo.setCurrentText(template_name)
            cmds.inViewMessage(amg="Template saved: <hl>{0}</hl>".format(template_name), pos="botLeft", fade=True)
        except Exception as exc:
            cmds.warning(str(exc))
        finally:
            cmds.undoInfo(closeChunk=True)

    def overwrite_selected_template(self):
        template_name = sanitize_template_name(self.template_overwrite_combo.currentText())
        if not template_name:
            cmds.warning("Choose a template to replace.")
            return
        if template_name in BUILTIN_SHAPE_NAMES:
            cmds.warning("Built-in shapes cannot be replaced this way.")
            return

        try:
            cmds.undoInfo(openChunk=True)
            data = collect_template_data_from_selection(template_name, self.current_direction(), self.current_up_vector())
            save_template_data(template_name, data)
            self.invalidate_icon_cache(template_name)
            self.rebuild_custom_shape_buttons()
            self.template_overwrite_combo.setCurrentText(template_name)
            cmds.inViewMessage(amg="Template replaced: <hl>{0}</hl>".format(template_name), pos="botLeft", fade=True)
        except Exception as exc:
            cmds.warning(str(exc))
        finally:
            cmds.undoInfo(closeChunk=True)

    def refresh_template_overwrite_combo(self, names=None):
        if names is None:
            names = template_names()
        current_text = self.template_overwrite_combo.currentText() if hasattr(self, "template_overwrite_combo") else ""
        blocker = QtCore.QSignalBlocker(self.template_overwrite_combo)
        self.template_overwrite_combo.clear()
        self.template_overwrite_combo.addItems(names)
        if current_text and current_text in names:
            self.template_overwrite_combo.setCurrentText(current_text)
        del blocker

    def invalidate_icon_cache(self, shape_name=None):
        if shape_name is None:
            self.icon_cache = {}
        else:
            self.icon_cache.pop(shape_name, None)

    def create_shape_icon(self, shape_name):
        if shape_name in self.icon_cache:
            return self.icon_cache[shape_name]

        icon = self.generate_shape_icon(shape_name)
        self.icon_cache[shape_name] = icon
        return icon

    def generate_shape_icon(self, shape_name):
        curves = self.generate_preview_curves(shape_name)
        if not curves:
            return self.placeholder_icon()

        planar_axis = self.detect_planar_axis(curves)
        projected_curves = []
        for curve in curves:
            current_curve = []
            for point in curve:
                if planar_axis:
                    current_curve.append(self.project_point_for_plane(point, planar_axis))
                else:
                    current_curve.append(self.project_point_for_icon(point))
            if len(current_curve) >= 2:
                projected_curves.append(current_curve)

        if not projected_curves:
            return self.placeholder_icon()

        return self.render_icon_from_projected_curves(projected_curves)

    def generate_preview_curves(self, shape_name):
        selection = cmds.ls(selection=True, long=True) or []
        temp_root = None
        try:
            if shape_name in SHAPE_BUILDERS:
                temp_root = SHAPE_BUILDERS[shape_name](unique_name("__iconPreview"))
                orient_transform(temp_root, DEFAULT_DIRECTION, DEFAULT_UP_VECTOR)
                freeze_transform(temp_root)
            elif shape_name in template_names():
                temp_root = create_template_root(unique_name("__iconPreview"), shape_name, direction=DEFAULT_DIRECTION, up_vector=DEFAULT_UP_VECTOR)
                freeze_transform(temp_root)
            else:
                return []

            curves = []
            for shape in gather_curve_shapes([temp_root]):
                points = self.sample_curve_points(shape, sample_count=60)
                if len(points) >= 2:
                    curves.append(points)
            return curves
        except Exception:
            return []
        finally:
            if temp_root and cmds.objExists(temp_root):
                try:
                    cmds.delete(temp_root)
                except Exception:
                    pass
            try:
                if selection:
                    cmds.select(selection, replace=True)
                else:
                    cmds.select(clear=True)
            except Exception:
                pass

    def sample_curve_points(self, shape, sample_count=60):
        if not cmds.objExists(shape) or cmds.nodeType(shape) != "nurbsCurve":
            return []
        try:
            min_value = cmds.getAttr(shape + ".minValue")
            max_value = cmds.getAttr(shape + ".maxValue")
        except Exception:
            return []

        if abs(max_value - min_value) < 1e-6:
            return []

        points = []
        for index in range(sample_count + 1):
            ratio = float(index) / float(sample_count)
            parameter = min_value + ((max_value - min_value) * ratio)
            try:
                position = cmds.pointOnCurve(shape, pr=parameter, p=True)
            except Exception:
                continue
            if position and len(position) >= 3:
                points.append((position[0], position[1], position[2]))
        return points

    def detect_planar_axis(self, curves, relative_tolerance=0.025, absolute_tolerance=0.001):
        all_points = [point for curve in curves for point in curve]
        if not all_points:
            return None

        ranges = {
            "x": max(point[0] for point in all_points) - min(point[0] for point in all_points),
            "y": max(point[1] for point in all_points) - min(point[1] for point in all_points),
            "z": max(point[2] for point in all_points) - min(point[2] for point in all_points),
        }
        max_range = max(ranges.values())
        if max_range <= absolute_tolerance:
            return "z"

        flat_limit = max(absolute_tolerance, max_range * relative_tolerance)
        planar_axis = min(ranges, key=ranges.get)
        if ranges[planar_axis] <= flat_limit:
            return planar_axis
        return None

    def project_point_for_plane(self, point, planar_axis):
        x_value, y_value, z_value = point
        if planar_axis == "x":
            return (z_value, -y_value)
        if planar_axis == "y":
            return (x_value, -z_value)
        return (x_value, -y_value)

    def project_point_for_icon(self, point):
        x_value, y_value, z_value = point
        rotate_y = math.radians(35.0)
        rotate_x = math.radians(-28.0)

        x_one = (x_value * math.cos(rotate_y)) + (z_value * math.sin(rotate_y))
        z_one = (-x_value * math.sin(rotate_y)) + (z_value * math.cos(rotate_y))
        y_one = y_value

        y_two = (y_one * math.cos(rotate_x)) - (z_one * math.sin(rotate_x))
        return (x_one, -y_two)

    def render_icon_from_projected_curves(self, curves):
        all_points = [point for curve in curves for point in curve]
        if not all_points:
            return self.placeholder_icon()

        min_x = min(point[0] for point in all_points)
        max_x = max(point[0] for point in all_points)
        min_y = min(point[1] for point in all_points)
        max_y = max(point[1] for point in all_points)

        width = max(max_x - min_x, 1e-5)
        height = max(max_y - min_y, 1e-5)
        padding = 8.0
        size = float(self.icon_draw_size)
        scale = min((size - (padding * 2.0)) / width, (size - (padding * 2.0)) / height)

        pixmap = QtGui.QPixmap(self.icon_draw_size, self.icon_draw_size)
        pixmap.fill(QtCore.Qt.transparent)

        painter = QtGui.QPainter(pixmap)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        pen = QtGui.QPen(QtGui.QColor(238, 242, 248))
        pen.setWidthF(2.1)
        pen.setCapStyle(QtCore.Qt.RoundCap)
        pen.setJoinStyle(QtCore.Qt.RoundJoin)
        painter.setPen(pen)

        center_x = (min_x + max_x) * 0.5
        center_y = (min_y + max_y) * 0.5

        for curve in curves:
            if len(curve) < 2:
                continue
            path = QtGui.QPainterPath()
            first = curve[0]
            start_point = QtCore.QPointF(
                ((first[0] - center_x) * scale) + (self.icon_draw_size * 0.5),
                ((first[1] - center_y) * scale) + (self.icon_draw_size * 0.5),
            )
            path.moveTo(start_point)
            for point in curve[1:]:
                draw_point = QtCore.QPointF(
                    ((point[0] - center_x) * scale) + (self.icon_draw_size * 0.5),
                    ((point[1] - center_y) * scale) + (self.icon_draw_size * 0.5),
                )
                path.lineTo(draw_point)
            painter.drawPath(path)

        painter.end()
        return QtGui.QIcon(pixmap)

    def placeholder_icon(self):
        pixmap = QtGui.QPixmap(self.icon_draw_size, self.icon_draw_size)
        pixmap.fill(QtCore.Qt.transparent)
        painter = QtGui.QPainter(pixmap)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        pen = QtGui.QPen(QtGui.QColor(150, 160, 178))
        pen.setWidthF(2.0)
        painter.setPen(pen)
        painter.drawRoundedRect(10, 10, self.icon_draw_size - 20, self.icon_draw_size - 20, 8, 8)
        painter.drawLine(16, 16, self.icon_draw_size - 16, self.icon_draw_size - 16)
        painter.drawLine(self.icon_draw_size - 16, 16, 16, self.icon_draw_size - 16)
        painter.end()
        return QtGui.QIcon(pixmap)

    def current_text_settings(self):
        return {
            "text": self.text_field.text().strip(),
            "add_text": self.enable_text_checkbox.isChecked(),
            "text_scale": self.text_scale_spin.value(),
            "text_offset": self.text_offset_spin.value(),
        }

    def current_direction(self):
        return normalize_direction_name(self.direction_combo.currentText())

    def current_up_vector(self):
        return normalize_up_vector_name(self.up_vector_combo.currentText())

    def ensure_valid_orientation_selection(self, *args):
        direction_name, up_name = resolve_direction_and_up(self.current_direction(), self.current_up_vector())
        if self.direction_combo.currentText() != direction_name:
            blocker = QtCore.QSignalBlocker(self.direction_combo)
            self.direction_combo.setCurrentText(direction_name)
            del blocker
        if self.up_vector_combo.currentText() != up_name:
            blocker = QtCore.QSignalBlocker(self.up_vector_combo)
            self.up_vector_combo.setCurrentText(up_name)
            del blocker

    def update_text_controls_enabled(self, state):
        self.text_field.setEnabled(state)
        self.text_scale_spin.setEnabled(state)
        self.text_offset_spin.setEnabled(state)

    def color_to_hex(self, rgb):
        color = QtGui.QColor()
        color.setRgbF(rgb[0], rgb[1], rgb[2])
        return color.name().upper()

    def set_preset_color(self, preset_name, auto_apply=False):
        rgb = self.color_presets.get(preset_name)
        if rgb:
            self.selected_custom_palette_index = -1
            self.set_current_rgb(rgb, selected_name=preset_name, update_recent=True, auto_apply=auto_apply)

    def set_current_rgb(self, rgb, selected_name=None, update_recent=True, auto_apply=False):
        self.current_rgb = tuple(rgb)
        self.builder.rgb_color = self.current_rgb
        if update_recent:
            self.push_recent_color(self.current_rgb)
        self.refresh_color_ui(selected_name=selected_name)
        if auto_apply:
            self.auto_apply_color_if_selection()

    def push_recent_color(self, rgb):
        rgb = tuple(rgb)
        self.recent_colors = [existing for existing in self.recent_colors if any(abs(a - b) > 0.0001 for a, b in zip(existing, rgb))]
        self.recent_colors.insert(0, rgb)
        self.recent_colors = self.recent_colors[:RECENT_COLOR_LIMIT]
        self.sync_settings_to_disk()
        self.rebuild_recent_color_swatches()

    def refresh_color_ui(self, selected_name=None):
        current_hex = self.color_to_hex(self.current_rgb)
        self.current_color_label.setText(current_hex)
        radius = max(10, int(self.current_color_swatch_size * 0.5))
        self.current_color_swatch.setStyleSheet(
            "QFrame#currentColorSwatch {background-color: %s; border: none; border-radius: %dpx;}" % (current_hex, radius)
        )

        luminance = (0.299 * self.current_rgb[0]) + (0.587 * self.current_rgb[1]) + (0.114 * self.current_rgb[2])
        button_border = current_hex
        hover_bg = "#343b4c" if luminance > 0.65 else "#303745"
        self.color_button.setStyleSheet(
            "QPushButton {background-color: #262b36; color: #f7f9fd; font-weight: 700; min-height: 34px; border-radius: 9px; border: 2px solid %s;}"
            "QPushButton:hover {background-color: %s; border: 2px solid %s;}"
            % (button_border, hover_bg, button_border)
        )

        for preset_name, button in self.color_preset_buttons.items():
            rgb = self.color_presets[preset_name]
            hex_color = self.color_to_hex(rgb)
            is_selected = selected_name == preset_name or all(abs(a - b) < 0.0001 for a, b in zip(rgb, self.current_rgb))
            border = "3px solid #ffffff" if is_selected else "1px solid #3c3c3c"
            button.setStyleSheet(
                "QToolButton {background-color: %s; border: %s; border-radius: 6px;}" % (hex_color, border)
            )

        for index, button in self.custom_palette_buttons.items():
            rgb = self.custom_palette[index]
            hex_color = self.color_to_hex(rgb)
            is_selected = index == self.selected_custom_palette_index
            border = "3px solid #ffffff" if is_selected else "1px solid #3c3c3c"
            button.setStyleSheet(
                "QToolButton {background-color: %s; border: %s; border-radius: 6px;}" % (hex_color, border)
            )

        for index, button in self.recent_color_buttons.items():
            rgb = self.recent_colors[index]
            hex_color = self.color_to_hex(rgb)
            is_selected = all(abs(a - b) < 0.0001 for a, b in zip(rgb, self.current_rgb)) and self.selected_custom_palette_index < 0 and selected_name is None
            border = "3px solid #ffffff" if is_selected else "1px solid #3c3c3c"
            button.setStyleSheet(
                "QToolButton {background-color: %s; border: %s; border-radius: 6px;}" % (hex_color, border)
            )

    def pick_color(self):
        initial = QtGui.QColor()
        initial.setRgbF(self.current_rgb[0], self.current_rgb[1], self.current_rgb[2])
        color = QtWidgets.QColorDialog.getColor(initial, self, "Pick RGB Color")
        if not color.isValid():
            return

        self.selected_custom_palette_index = -1
        self.set_current_rgb(color.getRgbF()[:3], selected_name=None, update_recent=True, auto_apply=True)

    def selected_transforms(self):
        selection = cmds.ls(selection=True, long=True) or []
        transforms = []
        for node in selection:
            if not cmds.objExists(node):
                continue
            node_type = cmds.nodeType(node)
            if node_type == "transform":
                transforms.append(node)
            elif node_type == "nurbsCurve":
                parents = cmds.listRelatives(node, parent=True, fullPath=True) or []
                transforms.extend(parents)
        return list(dict.fromkeys(transforms))

    def auto_apply_color_if_selection(self):
        targets = self.selected_transforms()
        if targets:
            self.builder.recolor_targets(targets)

    def handle_shape_click(self, shape_name):
        try:
            cmds.undoInfo(openChunk=True)
            if self.change_shape_radio.isChecked():
                self.replace_selected_shapes(shape_name)
            else:
                self.create_from_shape(shape_name)
        except Exception as exc:
            cmds.warning(str(exc))
        finally:
            cmds.undoInfo(closeChunk=True)

    def create_from_shape(self, shape_name):
        targets = self.selected_transforms()
        text_settings = self.current_text_settings()
        kwargs = {
            "shape_name": shape_name,
            "text": text_settings["text"],
            "add_text": text_settings["add_text"],
            "text_scale": text_settings["text_scale"],
            "text_offset": text_settings["text_offset"],
            "constrain_target": self.constraint_checkbox.isChecked(),
            "direction": self.current_direction(),
            "up_vector": self.current_up_vector(),
            "create_offset_group": self.create_offset_checkbox.isChecked(),
            "shape_scale": self.shape_scale_spin.value(),
            "line_width": self.line_width_spin.value(),
        }

        if targets:
            for target in targets:
                self.builder.create_controller(target=target, **kwargs)
        else:
            self.builder.create_controller(**kwargs)

    def create_text_only(self):
        text_value = self.text_field.text().strip()
        if not text_value:
            cmds.warning("Enter text before creating a text controller.")
            return

        try:
            cmds.undoInfo(openChunk=True)
            targets = self.selected_transforms()
            kwargs = {
                "text": text_value,
                "scale": self.text_scale_spin.value(),
                "offset_y": self.text_offset_spin.value(),
                "constrain_target": self.constraint_checkbox.isChecked(),
                "direction": self.current_direction(),
                "up_vector": self.current_up_vector(),
                "create_offset_group": self.create_offset_checkbox.isChecked(),
                "line_width": self.line_width_spin.value(),
            }
            if targets:
                for target in targets:
                    self.builder.create_text_only(target=target, **kwargs)
            else:
                self.builder.create_text_only(**kwargs)
        except Exception as exc:
            cmds.warning(str(exc))
        finally:
            cmds.undoInfo(closeChunk=True)

    def replace_selected_shapes(self, shape_name):
        targets = self.selected_transforms()
        if not targets:
            cmds.warning("Select one or more controllers to change their shapes.")
            return

        text_settings = self.current_text_settings()
        self.builder.replace_shape(
            targets,
            shape_name,
            text=text_settings["text"],
            add_text=text_settings["add_text"],
            text_scale=text_settings["text_scale"],
            text_offset=text_settings["text_offset"],
            direction=self.current_direction(),
            up_vector=self.current_up_vector(),
            shape_scale=self.shape_scale_spin.value(),
            line_width=self.line_width_spin.value(),
        )

    def reset_defaults(self, silent=False):
        self.create_radio.setChecked(True)
        self.constraint_checkbox.setChecked(False)
        self.create_offset_checkbox.setChecked(DEFAULT_CREATE_OFFSET_GROUP)
        self.direction_combo.setCurrentText(DEFAULT_DIRECTION)
        self.up_vector_combo.setCurrentText(DEFAULT_UP_VECTOR)
        self.template_view_combo.setCurrentText(DEFAULT_SHAPE_DISPLAY_MODE)
        self.shape_scale_spin.setValue(DEFAULT_SHAPE_SCALE)
        self.line_width_spin.setValue(DEFAULT_LINE_WIDTH)
        self.enable_text_checkbox.setChecked(DEFAULT_TEXT_ENABLED)
        self.text_field.clear()
        self.text_scale_spin.setValue(DEFAULT_TEXT_SCALE)
        self.text_offset_spin.setValue(DEFAULT_TEXT_OFFSET)
        self.apply_saved_defaults_to_ui(silent=silent)


    def show_help_dialog(self):
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Help - {} {}".format(WINDOW_TITLE, VERSION))
        dialog.setMinimumSize(620, 520)
        dialog.resize(700, 620)
        layout = QtWidgets.QVBoxLayout(dialog)
        browser = QtWidgets.QTextBrowser()
        browser.setOpenExternalLinks(True)
        browser.setReadOnly(True)
        help_text = load_help_text()
        if hasattr(browser, "setMarkdown"):
            browser.setMarkdown(help_text)
        else:
            browser.setPlainText(help_text)
        layout.addWidget(browser)
        button_row = QtWidgets.QHBoxLayout()
        button_row.addStretch()
        close_button = QtWidgets.QPushButton("Close")
        close_button.clicked.connect(dialog.accept)
        button_row.addWidget(close_button)
        layout.addLayout(button_row)
        dialog.exec_()


def launch_ui():
    app = QtWidgets.QApplication.instance()
    if app:
        for widget in app.allWidgets():
            name_attr = getattr(widget, "objectName", None)
            widget_name = name_attr() if callable(name_attr) else name_attr
            if widget_name == WINDOW_OBJECT:
                widget.close()
                widget.deleteLater()

    dialog = ControllerToolUI(parent=maya_main_window())
    dialog.show()
    return dialog
