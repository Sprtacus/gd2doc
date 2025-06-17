{# doc.md.j2 – Jinja2‑Template für die generierte Markdown‑Dokumentation einer Godot‑GDScript‑Datei #}
---
title: "{{ script.name }}"
description: "{{ script.short_description }}"
---

# {{ script.name }}

{{ script.description }}

## Überblick
- **Dateipfad:** `{{ script.path }}`
- **Klasse:** `{{ script.class_name or "—" }}`
- **Erbt von:** `{{ script.extends or "—" }}`
- **Signale:** {{ signals | length }}
- **Enums:** {{ enums | length }}
- **Konstanten:** {{ consts | length }}
- **Variablen:** {{ variables | length }}
- **Funktionen:** {{ functions | length }}

{% if signals %}
## Signale
{% for signal in signals %}
- `{{ signal.name }}({{ signal.args | map(attribute='name') | join(', ') }})` – {{ signal.description }}
{% endfor %}
{% endif %}

{% if enums %}
## Enums
{% for enum in enums %}
### `{{ enum.name }}`
| Wert | Integer | Beschreibung |
|------|---------|--------------|
{% for item in enum.items %}
| `{{ item.name }}` | {{ item.value }} | {{ item.description }} |
{% endfor %}
{% endfor %}
{% endif %}

{% if consts %}
## Konstanten
| Name | Wert | Beschreibung |
|------|------|--------------|
{% for const in consts %}
| `{{ const.name }}` | {{ const.value }} | {{ const.description }} |
{% endfor %}
{% endif %}

{% if variables %}
## Variablen
| Name | Typ | Standard | Beschreibung |
|------|-----|----------|--------------|
{% for var in variables %}
| `{{ var.name }}` | {{ var.type or "var" }} | {{ var.default or "—" }} | {{ var.description }} |
{% endfor %}
{% endif %}

{% if functions %}
## Funktionen
{% for func in functions %}
### `{{ func.name }}({% for p in func.params %}{{ p.name }}{% if not loop.last %}, {% endif %}{% endfor %})`
{{ func.description }}

{% if func.params %}
#### Parameter
| Name | Typ | Standard | Beschreibung |
|------|-----|----------|--------------|
{% for p in func.params %}
| `{{ p.name }}` | {{ p.type or "var" }} | {{ p.default or "—" }} | {{ p.description }} |
{% endfor %}
{% endif %}

{% if func.returns %}
**Rückgabe:** `{{ func.returns.type or "var" }}` – {{ func.returns.description }}
{% endif %}

{% if func.examples %}
##### Beispiel
```gdscript
{{ func.examples }}
```
{% endif %}

---
{% endfor %}
{% endif %}

{% if todos %}
## TODO
{% for todo in todos %}
- {{ todo }}
{% endfor %}
{% endif %}
