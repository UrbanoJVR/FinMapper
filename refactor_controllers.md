# Refactor Flask → MethodView + DI + Controllers Delgados

Este documento describe **cómo quiero que se refactorice mi aplicación Flask** usando IA (por ejemplo, Cursor), con las siguientes ideas clave:

- **Eliminar** el patrón `@blueprint.route(..., methods=['GET', 'POST'])` + `if request.method == 'GET'` / `if request.method == 'POST'`.
- **Introducir `MethodView`** para los endpoints que comparten URL y usan varios verbos HTTP. También deberán migrarse a method view todos los controladores, no solo los que tengan varios métodos por cada recurso (aunque estos son menos prioritarios al ser más sencillos)
- **Inyectar `CommandBus` y `QueryBus`** correctamente (sin singletons mágicos) desde el *entrypoint* de la app.
- **Adelgazar controllers**: sacar lógica de mapeo y helpers fuera de las vistas.
- **Refactor incremental**: endpoint por endpoint, siempre manteniendo los tests pasando.

La IA debe seguir estas instrucciones **paso a paso** y **NO hacer un refactor masivo de golpe**.

---

## 0. Contexto y supuestos

- Proyecto en **Flask 3.X** con **Blueprints**.
- Arquitectura orientada a **DDD / Hexagonal**:
  - Capas tipo `application`, `domain`, `infrastructure`, `presentation`, etc.
  - Uso de `CommandBus` y `QueryBus`.
- La capa de presentación usa **Flask + Jinja** (server-side rendering).
- Actualmente hay endpoints con esta pinta (aprox):

```python
@transactions_crud_blueprint.route('/movements/<int:month>/<int:year>', methods=['GET', 'POST'])
def movements_list(month: int, year: int):
    if request.method == 'GET':
        ...
    if request.method == 'POST':
        ...
```

Este patrón se considera ahora **mala práctica** en este proyecto y debe ser eliminado.

---

## 1. Principios de diseño a respetar

1. **No más `if request.method == 'GET'` / `if request.method == 'POST'`** en un mismo endpoint.
2. **Un `MethodView` por caso de uso / URL base**, con métodos `get()`, `post()`, etc., separados.
3. **`CommandBus` y `QueryBus` no deben instanciarse en el módulo del controller**, sino en un punto central (p. ej. `create_app`) y ser inyectados.
4. El controller (vista Flask) debe:
   - Recoger datos de la request.
   - Delegar en mappers + command/query handlers.
   - Decidir vista/redirect.
   - **No** contener bucles complejos, lógica de dominio ni reglas de negocio.
5. La refactorización debe ser **incremental, endpoint por endpoint**, asegurando:
   - Tests antiguos siguen pasando (o se adaptan con criterio).
   - Se añaden tests nuevos si hace falta.
   - Se hace commit tras cada bloque pequeño de trabajo estable.

---

## 2. DI de `CommandBus` y `QueryBus`

### 2.1. Punto de creación de buses

La IA debe:

- Localizar el punto de entrada de la app (`create_app` o similar).
- Asegurarse de que ahí se instancian **una sola vez**:

  - `CommandBus`
  - `QueryBus`

- Estas instancias deben ser pasadas a las factorías de `Blueprint`.

> **Objetivo:** No crear `CommandBus()` / `QueryBus()` dentro de los módulos de los controllers.

### 2.2. Blueprint factory con inyección

Cada Blueprint principal (por ejemplo, el de transacciones) debe exponerse como una función factory que reciba los buses como parámetros y los use para:

- Guardarlos en el propio blueprint (atributos dinámicos) **o**
- Pasarlos a las vistas (`MethodView`) por constructor.

Ambas opciones son válidas; **preferible** la DI por constructor de `MethodView` (más clara y testable):

- El Blueprint:
  - Se crea.
  - Registra las rutas con `add_url_rule(...)`.
  - Crea las vistas con `XxxView.as_view("nombre_endpoint", command_bus=..., query_bus=...)`.

- Cada `MethodView` recibe `command_bus` / `query_bus` en su `__init__` y los guarda en `self`.

---

## 3. Uso de `MethodView` (en vez de `@route(..., methods=[...])`)

### 3.1. Qué hay que transformar

Siempre que se vea un patrón como:

- `@blueprint.route("/x", methods=["GET", "POST"])` con `if request.method == ...`
- O una función que mezcla lógica de varios verbos HTTP

…ese endpoint debe refactorizarse a `MethodView`.

### 3.2. Objetivo por endpoint

Para cada URL que acepte varios métodos:

- Tener **una clase `MethodView`** por recurso / caso de uso.
- Dentro de la clase:
  - Método `get(...)` → manejo GET
  - Método `post(...)` → manejo POST
  - (Opcional) `delete`, `put`, etc. si aplica.

### 3.3. Registro de rutas

La IA debe:

1. Crear la clase `XxxView(MethodView)` en el módulo adecuado.
2. Mover el código correspondiente de GET/POST a `get()` y `post()`.
3. En la factory del blueprint, registrar la vista con `add_url_rule` y `as_view`.
4. Usar un nombre de endpoint coherente (ej. `"movements"` o `"edit_transaction"`) y consistente.

**Nota para la IA:**  
La cadena que se pasa a `as_view("...")` es el **nombre interno del endpoint** dentro del blueprint. Debe ser única por endpoint.

---

## 4. Adelgazar controllers: mappers y helpers

### 4.1. Qué se considera “controller gordo”

Un controller está haciendo demasiado trabajo cuando:

- Contiene bucles sobre `request.form` o estructuras similares.
- Aplica lógica de transformación considerable (si A → agregar B, si no → saltar, etc.).
- Procesa ids, castea tipos, construye listas/colecciones complejas.
- Mezcla lógica de mostrar vista con lógica de negocio o de aplicación.

El objetivo:
- El controller solo debe coordinar:
  - input (request/form)
  - mappers / commands / queries
  - output (render_template/redirect/flash)

### 4.2. Mappers de formularios / DTOs

La IA debe:

- Identificar bloques de código que convierten datos `request.form` en:
  - `Command`s
  - `Query`s
  - estructuras intermedias (por ej. listas de `CategorizedTransaction`, etc.)

- Extraer dichos bloques a **clases mapper** en la capa de presentación (p. ej. `app/src/presentation/mapper/...`), que:

  - Reciban el form o los datos de la request.
  - Devuelvan un objeto más limpio (DTO o Command ya preparado).
  - Mantengan el código del controller mucho más corto.

**Importante:**  
No es obligatorio que la IA lo haga TODO de golpe.  
Debe aplicar esta refactorización solo donde tenga sentido y de forma incremental, pero **siempre debe tenerlo en la lista de mejoras a aplicar**.

---

## 5. Tipado más fuerte en mappers y formularios

### 5.1. Intención

El objetivo del tipado fuerte en mappers es:

- Tener funciones/cuñas de código cuyo input y output estén **claramente tipados** (vía type hints).
- Que el resultado del mapeo a DTO/Command **no dependa ya del framework** (ni de Flask ni de WTForms).

### 5.2. Reglas

La IA debe:

- Mantener o mejorar los type hints **en los mappers**, no en los controllers.
- Si es útil, introducir DTOs (p. ej. dataclasses) con tipos explícitos, que luego se transformen en Commands.
- Evitar que el controller tenga que preocuparse de castear tipos manualmente donde pueda delegarse en un mapper.

**Nota específica del autor**:  
En el código actual, ya existen anotaciones como `form: UpsertTransactionForm = UpsertTransactionForm(request.form)`.  
Eso está bien como anotación, pero el objetivo a medio plazo es que sea el mapper quien reciba ese `form` y devuelva algo typed y estable.

---

## 6. Helpers de fecha y lógica “utility”

Hay funciones como:

- `previous_month`
- `next_month`
- `calculate_month_year`
- O similares que no pertenecen al dominio puro ni a la lógica de infraestructura

La IA debe:

- Extraer estas funciones a **módulos helper** (por ejemplo, en una carpeta compartida tipo `shared`, `common` o `presentation/helpers`).
- Asegurarse de que los controllers solo las usan, pero no las definen dentro del mismo archivo, para que el controller se mantenga más limpio.

No es relevante si se llaman `date_utils`, `helpers`, o similar:  
la clave es que NO estén mezcladas con el código de la view.

---

## 7. Estrategia de refactorización **incremental**

Este punto es CRÍTICO y la IA debe respetarlo.

### 7.1. No hacer refactor masivo

La IA **NO debe**:

- Reescribir todos los controllers de golpe.
- Cambiar cientos/miles de líneas en un solo commit.
- Romper medio proyecto para luego ir arreglando.

### 7.2. Proceso deseado (por endpoint)

Para cada endpoint/caso de uso:

1. **Identificar** la función actual del controller (por ejemplo, `movements_list`, `edit_transaction`, etc.).
2. **Crear el `MethodView` equivalente**:
   - Crear clase `XxxView`.
   - Separar `get()` y `post()`.
   - Inyectar `command_bus` y `query_bus` en el constructor (o acceder vía blueprint si se ha decidido así).
3. **Actualizar el Blueprint** para registrar la nueva vista con `add_url_rule` y `as_view`.
4. **Eliminar el antiguo `@route(..., methods=['GET', 'POST'])` + `if request.method`** solo cuando la nueva vista esté conectada y funcione.
5. **Refactorizar el exceso de lógica del controller**:
   - Mover bucles de procesamiento de forms a mappers.
   - Mover funciones auxiliares a helpers, si aplica.
6. **Ejecutar tests**:
   - Asegurarse de que los tests existentes pasan.
   - Si algún test revienta porque estaba muy acoplado a la implementación anterior, actualizarlo de forma coherente.
   - Añadir tests nuevos cuando tenga sentido (por ejemplo, para cubrir el comportamiento de `get()` y `post()` por separado).
7. **Hacer commit**:
   - Un commit por endpoint (o por bloque lógico pequeño).
   - Mensajes de commit descriptivos del tipo: `refactor: movements endpoint to MethodView`.

Luego pasar al siguiente endpoint.

---

## 8. Reglas adicionales para la IA (Cursor u otra)

1. **No introducir nuevos frameworks** (FastAPI, etc.).  
   Todo esto se hace dentro de Flask.
2. **No cambiar la arquitectura global** (DDD/Hexagonal sigue igual).
3. **Respetar los nombres actuales** de commands/queries/handlers, salvo que haya una razón clara para renombrarlos.
4. **Mantener la intención funcional EXACTA** de cada endpoint:
   - Si antes renderizaba una vista concreta con ciertos parámetros, debe seguir haciéndolo.
   - Si antes redirigía a un sitio concreto tras un POST, debe seguir igual.
5. **Consultas / commands NO deben depender de Flask**:
   - Controllers → dependen de Flask.
   - Commands / queries / domain → no deben conocer Flask ni objetos de request/response.

---

## 9. Checklist resumido para cada endpoint

La IA puede usar este checklist como guía operativa:

1. ¿El endpoint usa `@route(..., methods=[...])` y `if request.method`?
   - ✅ Sí → candidato a `MethodView`.

2. ¿Hay instancias de `CommandBus()` o `QueryBus()` dentro del módulo del controller?
   - ❌ Sí → mover creación a `create_app` y pasarlas vía blueprint factory/constructor.

3. ¿El controller hace bucles sobre `request.form` o estructuras similares?
   - ❌ Sí → sacar esa lógica a un mapper en la capa de presentación.

4. ¿Hay funciones auxiliares (fecha, dirección anterior/siguiente, etc.) definidas en el mismo archivo?
   - ❌ Sí → extraerlas a un módulo helper compartido.

5. Después del refactor:
   - ¿`get()` y `post()` están separados y claros?
   - ¿El controller está centrado en orquestar, no en calcular?
   - ¿Los tests pasan?  
   - ¿Se ha hecho commit del cambio?

---

Aquí tienes una versión específica en formato checklist para GitHub Issues, ideal para crear issues individuales por cada parte del refactor, o para un único epic con subtareas.

✅ Refactor Flask → MethodView (Checklist para GitHub Issues)
🧩 Preparación de arquitectura (hacer una vez)

 Crear o revisar create_app() como punto único donde se instancian:

 CommandBus

 QueryBus

 Adaptar cada módulo de Blueprints para que tenga una factory:

 create_xxx_blueprint(command_bus, query_bus)

 Añadir DI a los blueprints:

 Pasar buses al constructor del MethodView (preferido)

 O como atributos dinámicos del blueprint

🟨 Refactor endpoint por endpoint (iterativo)
🔁 Para cada endpoint con @route(..., methods=[GET, POST]):

 Localizar la función y revisar su comportamiento actual

 Crear clase XxxView(MethodView) en el módulo adecuado

 Extraer lógica GET → def get(...)

 Extraer lógica POST → def post(...)

 Inyectar buses vía __init__ de la vista

 Registrar vista en el blueprint:

 add_url_rule()

 as_view("nombre_endpoint")

 Eliminar el antiguo @route(methods=[...]) + if request.method

 Ejecutar tests existentes

 Ajustar/crear tests nuevos si es necesario

 Hacer commit con mensaje:

refactor: migrate <endpoint> to MethodView

🔧 Limpieza y mapeo (opcional pero recomendado en cada iteración)
Para cada endpoint refactorizado:

 Identificar lógica excesiva en el controller (loops, transformaciones, parsing)

 Crear mapper(es) en presentation/mappers:

 Mapper de formularios

 Mapper a Commands/DTOs

 Sustituir lógica manual en el controller por llamadas a mappers

 Añadir type hints claros en mappers (no en controllers)

 Ejecutar tests

🧹 Helpers compartidos

Para las funciones tipo:

previous_month

next_month

calculate_month_year

lógica utilitaria relacionada con formularios y fechas

Crear un módulo utilitario:

 Crear carpeta presentation/helpers o shared/utils

 Mover helpers detectados

 Hacer el controller usarlos

 Testear helpers si aplica

🧪 Validación continua

Después de cada endpoint:

 ¿get() está aislado y claro?

 ¿post() está aislado y claro?

 ¿La vista solo orquesta? (sin lógica compleja)

 ¿Los mappers hacen el trabajo sucio?

 ¿Los buses se reciben por DI?

 ¿Todos los tests pasan?

 Hacer commit incremental

🏁 Finalización del epic

Cuando todos los endpoints relevantes hayan sido migrados:

 Eliminar código muerto

 Eliminar helper duplicado

 Revisar que ningún módulo crea su propio CommandBus o QueryBus

 Documentar nueva estructura en README

 Hacer commit final:

refactor: complete MethodView migration + clean controllers
