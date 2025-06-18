import os
import re
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


@dataclass
class ScriptInfo:
    name: str
    path: str
    short_description: str = ""
    description: str = ""
    class_name: Optional[str] = None
    extends: Optional[str] = None


@dataclass
class ParamInfo:
    name: str
    type: Optional[str] = None
    default: Optional[str] = None
    description: str = ""


@dataclass
class ReturnInfo:
    type: Optional[str] = None
    description: str = ""


@dataclass
class FunctionInfo:
    name: str
    description: str = ""
    params: List[ParamInfo] = field(default_factory=list)
    returns: Optional[ReturnInfo] = None
    examples: Optional[str] = None


@dataclass
class ConstInfo:
    name: str
    value: str
    description: str = ""


@dataclass
class VariableInfo:
    name: str
    type: Optional[str] = None
    default: Optional[str] = None
    description: str = ""


@dataclass
class SignalInfo:
    name: str
    args: List[ParamInfo] = field(default_factory=list)
    description: str = ""


@dataclass
class EnumItem:
    name: str
    value: Optional[int] = None
    description: str = ""


@dataclass
class EnumInfo:
    name: str
    items: List[EnumItem] = field(default_factory=list)
    description: str = ""


def parse_gdscript(path: str) -> Dict[str, Any]:
    """Parse a single GDScript file and return collected information."""
    script = ScriptInfo(name=os.path.splitext(os.path.basename(path))[0], path=path)
    signals: List[SignalInfo] = []
    enums: List[EnumInfo] = []
    consts: List[ConstInfo] = []
    variables: List[VariableInfo] = []
    functions: List[FunctionInfo] = []
    todos: List[str] = []

    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    index = 0
    pending_comments: List[str] = []

    # header comments
    while index < len(lines) and lines[index].strip().startswith("#"):
        comment = lines[index].strip()[1:].strip()
        if comment.lower().startswith("todo"):
            todos.append(comment[4:].strip())
        else:
            pending_comments.append(comment)
        index += 1
    if pending_comments:
        script.short_description = pending_comments[0]
        script.description = "\n".join(pending_comments)
    pending_comments = []

    def consume_comments() -> str:
        nonlocal index
        comments: List[str] = pending_comments.copy()
        pending_comments.clear()
        return "\n".join(comments)

    while index < len(lines):
        line = lines[index].rstrip("\n")
        stripped = line.strip()

        if stripped.startswith("#"):
            text = stripped[1:].strip()
            if text.lower().startswith("todo"):
                todos.append(text[4:].strip())
            else:
                pending_comments.append(text)
            index += 1
            continue

        description = consume_comments()

        if stripped.startswith("class_name"):
            m = re.match(r"class_name\s+(\w+)", stripped)
            if m:
                script.class_name = m.group(1)
            index += 1
            continue
        if stripped.startswith("extends"):
            m = re.match(r"extends\s+([A-Za-z0-9_.]+)", stripped)
            if m:
                script.extends = m.group(1)
            index += 1
            continue
        if stripped.startswith("signal"):
            m = re.match(r"signal\s+(\w+)\((.*)\)", stripped)
            if m:
                name = m.group(1)
                params = m.group(2).strip()
                args: List[ParamInfo] = []
                if params:
                    for p in params.split(','):
                        p = p.strip()
                        if not p:
                            continue
                        args.append(ParamInfo(name=p))
                signals.append(SignalInfo(name=name, args=args, description=description))
            index += 1
            continue
        if stripped.startswith("enum"):
            m = re.match(r"enum\s+(\w+)\s*\{(.*)\}", stripped)
            if m:
                name = m.group(1)
                body = m.group(2)
                items: List[EnumItem] = []
                for item in body.split(','):
                    item = item.strip()
                    if not item:
                        continue
                    if '=' in item:
                        i_name, i_val = map(str.strip, item.split('=', 1))
                        try:
                            value = int(i_val)
                        except ValueError:
                            value = None
                        items.append(EnumItem(name=i_name, value=value))
                    else:
                        items.append(EnumItem(name=item))
                enums.append(EnumInfo(name=name, items=items, description=description))
            index += 1
            continue
        if stripped.startswith("const"):
            m = re.match(r"const\s+(\w+)\s*=\s*(.*)", stripped)
            if m:
                name = m.group(1)
                value = m.group(2).strip()
                consts.append(ConstInfo(name=name, value=value, description=description))
            index += 1
            continue
        if stripped.startswith("var"):
            m = re.match(r"var\s+(\w+)(?::\s*([A-Za-z0-9_.]+))?(?:\s*=\s*(.*))?", stripped)
            if m:
                name = m.group(1)
                type_ = m.group(2)
                default = m.group(3).strip() if m.group(3) else None
                variables.append(VariableInfo(name=name, type=type_, default=default, description=description))
            index += 1
            continue
        if stripped.startswith("func"):
            m = re.match(r"func\s+(\w+)\((.*)\)(?:\s*->\s*([A-Za-z0-9_.]+))?:", stripped)
            if m:
                name = m.group(1)
                params_str = m.group(2)
                return_type = m.group(3)
                params: List[ParamInfo] = []
                if params_str:
                    for p in params_str.split(','):
                        p = p.strip()
                        if not p:
                            continue
                        pm = re.match(r"(\w+)(?::\s*([A-Za-z0-9_.]+))?(?:\s*=\s*(.*))?", p)
                        if pm:
                            pname = pm.group(1)
                            ptype = pm.group(2)
                            pdefault = pm.group(3)
                            params.append(ParamInfo(name=pname, type=ptype, default=pdefault))
                        else:
                            params.append(ParamInfo(name=p))
                returns = ReturnInfo(type=return_type) if return_type else None
                functions.append(FunctionInfo(name=name, description=description, params=params, returns=returns))
            index += 1
            continue

        # reset pending comments if line is empty or other
        index += 1
        pending_comments.clear()

    result = {
        "script": script.__dict__,
        "signals": [s.__dict__ for s in signals],
        "enums": [{"name": e.name, "items": [item.__dict__ for item in e.items], "description": e.description} for e in enums],
        "consts": [c.__dict__ for c in consts],
        "variables": [v.__dict__ for v in variables],
        "functions": [
            {
                "name": f.name,
                "description": f.description,
                "params": [p.__dict__ for p in f.params],
                "returns": f.returns.__dict__ if f.returns else None,
                "examples": f.examples,
            }
            for f in functions
        ],
        "todos": todos,
    }
    return result
