<!-- SPECKIT START -->
For additional context about technologies to be used, project structure,
shell commands, and other important information, read the current plan
<!-- SPECKIT END -->

## Setup local obligatorio

Antes de trabajar en este repo, cada colaborador (humano o agente) debe correr:

```bash
make dev-setup
```

Esto instala dos cosas críticas:

- **nbstripout**: filtro de git que elimina outputs y execution counts de los
  notebooks antes de cada commit. Sin esto, los notebooks commitiados incluyen
  outputs que generan conflictos de merge entre colaboradores.

- **pull.autostash**: config de git que hace que `git pull` guarde y restaure
  automáticamente los cambios locales. Sin esto, ejecutar un notebook y luego
  hacer `git pull` falla porque git detecta el notebook como modificado y se
  niega a mergear. El workaround sin esta config es `git stash && git pull &&
  git stash drop`, que es engorroso y propenso a errores.

Si un colaborador reporta que `git pull` falla con mensajes del estilo
_"your local changes would be overwritten by merge"_ en notebooks, la causa
es que no corrió `make dev-setup`. La solución inmediata es:

```bash
git fetch origin && git reset --hard origin/<rama>
make dev-setup
```

---

## Spec-Kit Workflow

Este proyecto usa spec-driven development. Lee `.specify/memory/constitution.md`
al inicio de cada sesión — es el contrato técnico del proyecto.

Los specs viven en `specs/<###-nombre>/spec.md`. Los specs históricos (Fase 1)
ya están ahí. Features nuevas siguen el mismo esquema.

---

### Modo interactivo (sesión de codeo activa)

**Cuándo sugerir armar un spec antes de codear:**

Ante cualquier pedido que implique agregar una capacidad nueva, cambiar una
interfaz existente o introducir un módulo nuevo, sugerí armar el spec primero.
No hace falta pedírtelo — tomá la iniciativa. La frase puede ser breve:
_"Esto merece un spec antes de codear, ¿arrancamos con `/speckit-specify`?"_

**Cuándo no hace falta spec:**

- Bug fix acotado que no cambia comportamiento observable
- Cambio de config o constante
- Refactor interno sin cambio de interfaz pública

**Si el usuario pide armar un spec:**

Antes de escribir `spec.md`, hacé las preguntas necesarias para afinar
requisitos. No escribas el spec con ambigüedades — es mejor una ronda de
preguntas corta que un spec que necesite reescribirse.

Flujo recomendado:
```
preguntas de clarificación → /speckit-specify → /speckit-clarify (si quedan dudas)
→ /speckit-plan → /speckit-tasks → /speckit-implement
```

---

### Modo autónomo (auto mode / /goal / sesión de research)

En modo autónomo, no esperés confirmación para crear un spec. Si la tarea
implica una feature sin spec existente, creá el spec, el plan y las tasks antes
de implementar. El flujo mínimo aceptable:

```
/speckit-specify → /speckit-plan → /speckit-tasks → /speckit-implement
```

Durante una sesión de research, si identificás features que habrá que construir
(aunque no estén en el scope inmediato), creá el spec correspondiente en
`specs/` y dejalo en estado `draft`. No implementes sin spec.

---

### Rama, PR y gate de implementación

Después de armar un spec (specify + plan + tasks), **nunca implementes de
inmediato**. El flujo obligatorio es:

1. Crear rama `###-nombre-feature` desde `main` si no existe.
2. Commitear los artefactos del spec (`specs/###-nombre/spec.md`, `plan.md`,
   `tasks.md`) en esa rama.
3. Abrir un PR con el spec como descripción — sin código de implementación.
4. **Detenerse**. No avanzar con implementación hasta recibir aprobación
   explícita del usuario, tanto en modo interactivo como en modo autónomo.

Spec-kit detecta la feature activa por el nombre de la rama, así que la rama
debe seguir la convención `###-nombre-feature` (ej. `003-model-training`).
