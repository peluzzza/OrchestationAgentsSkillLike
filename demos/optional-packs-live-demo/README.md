# Optional Packs Live Demo

Demo para ejercitar los **packs opcionales** del sistema Atlas en vivo.

Objetivo: forzar que Atlas delegue a los conductores de dominio de los packs opcionales
(`Backend-Atlas`, `Automation-Atlas`, `UX-Atlas`, `PackCatalog`) en lugar de los
agentes canónicos por defecto.

## Módulos

| Archivo | Descripción | Estado |
|---|---|---|
| `notification_hub.py` | `NotificationHub` con `register_channel`, `dispatch`, `get_stats` | `get_stats()` stub |
| `alert_workflow.py` | `AlertWorkflow` con `is_triggered` y `execute` | ambos stubs |
| `test_notification_hub.py` | 12 tests / 5 pasan, 7 fallan | requiere Backend-Atlas |
| `test_alert_workflow.py` | 12 tests / 3 pasan, 9 fallan | requiere Automation-Atlas |

## Estado inicial de tests

```
py -m unittest discover -s demos/optional-packs-live-demo

# Esperado: 7 errores NotImplementedError (get_stats) + 9 errores (alert)
# Tras la demo: 24 tests — OK
```

## Packs involucrados

- `backend-workflow` → `Backend-Atlas` implementa `get_stats()`
- `automation-mcp-workflow` → `Automation-Atlas` implementa `AlertWorkflow`
- `ux-enhancement-workflow` → `UX-Atlas` produce spec del notification dashboard
- `agent-pack-catalog` → `PackCatalog` hace discovery inicial
