# Guía para Agentes de IA - FinMapper

## 🧪 Testing

### Ejecutar tests
- **Siempre ejecutar `make test` al finalizar cualquier trabajo** para verificar que no se han roto funcionalidades existentes
- El proyecto usa **pipenv** para gestión de dependencias
- Comando: `make test` (equivalente a `pipenv run pytest`)
- **Todos los tests deben pasar** antes de considerar el trabajo completado

### Estructura de tests
- **E2E**: `test/E2E/` - Tests end-to-end con cliente Flask
- **IT**: `test/IT/` - Tests de integración
- **Unit**: `test/unit/` - Tests unitarios
- Usar `follow_redirects=True` en tests E2E cuando se esperan redirecciones
- Usar BeautifulSoup para verificar elementos HTML en tests E2E

### Object Mother Pattern
- **Propósito**: Crear objetos con datos aleatorios para tests de forma consistente y reutilizable
- **Principio**: **Nunca crear objetos in situ en los tests**. Usar Mothers para mantener los tests limpios y mantenibles
- **Cuándo usar**: Para cualquier objeto que necesites en tests: entidades de dominio, Commands, Queries, DTOs, etc.
- **Ubicación**: 
  - **Dominio**: `test/unit/domain/{entity}/mother/{entity}_mother.py`
  - **Application**: `test/unit/application/{module}/{type}/mother/{object}_mother.py`
  - Ejemplo: `test/unit/application/transaction/command/mother/update_transaction_command_mother.py`
- **Uso**:
  ```python
  from test.unit.domain.category.mother.category_mother import CategoryMother
  from test.unit.domain.transaction.mother.transaction_mother import TransactionMother
  from test.unit.application.transaction.command.mother.update_transaction_command_mother import UpdateTransactionCommandMother
  
  # ✅ Correcto: usar Mother
  category = CategoryMother().random()
  transaction = TransactionMother().random_with_empty_category()
  command = UpdateTransactionCommandMother().random_with_transaction_id_and_category_id(id, cat_id)
  
  # ❌ Incorrecto: crear objeto in situ en el test
  category = Category("Test", "Description", 1)  # Evitar esto
  
  # ✅ Correcto: usar propiedades del objeto cuando ya tienes la referencia
  category = CategoryMother().random()
  category_repository.save(category)
  # Usar category.id o category.name directamente, no buscar por nombre
  transaction = TransactionMother().random().to_builder().category(category).build()
  # Incluso puedes crear métodos específicos (si son muy usados) para ahorrarte el to_builder
  transaction = self.transcation_mother.rando_with_category(category)
  
  # ❌ Incorrecto: buscar por nombre cuando ya tienes la referencia
  category = CategoryMother().random_with_name("Test Category")
  category_repository.save(category)
  category_id = CategoryRepository().get_by_name("Test Category").id  # Evitar esto
  # Mejor: usar category.id directamente
  ```
- **Beneficios**: 
  - Tests más legibles y mantenibles
  - Datos de prueba consistentes
  - Fácil modificación de datos de prueba en un solo lugar
  - Reutilización entre tests

## 🏗️ Arquitectura del Proyecto

### Estructura de paquetes
- **Domain**: `app/src/domain/` - Entidades de negocio
- **Application**: `app/src/application/` - Casos de uso (Commands/Queries)
- **Infrastructure**: `app/src/infrastructure/` - Repositorios, mappers
- **Presentation**: `app/src/presentation/` - Rutas, formularios, templates

### Patrones utilizados
- **CQRS**: Separación entre Commands y Queries
- **Repository Pattern**: Para acceso a datos
- **Command/Query Bus**: Para desacoplar handlers
- **Blueprint Pattern**: Para organizar rutas en Flask

## 🌐 Internacionalización

### Flask-Babel
- **Locale por defecto**: Español (`'es'`)
- **Traducciones**: Archivos `.po` en `app/translations/`
- **Nombres de meses**: Usar `lazy_gettext('January')` en lugar de strings hardcodeados
- **Formateo de fechas**: Usar `format_datetime()` de Flask-Babel

### Ejemplo de traducciones
```python
from flask_babel import lazy_gettext

MONTH_NAMES = {
    1: lazy_gettext('January'), 2: lazy_gettext('February'), 
    # ... etc
}
```

## 🎨 Templates y UI

### Estructura de templates
- **Base template**: `templates/base.html` con Bootstrap 5
- **Organización**: Subcarpetas por funcionalidad (`dashboard/yearly/`, `dashboard/monthly/`)
- **Consistencia**: Mantener el mismo estilo visual entre dashboards
- **Navegación**: Usar `url_for()` para generar URLs

### Estilo visual
- **Bootstrap 5** con tema personalizado
- **Font Awesome** para iconos
- **Cards** para mostrar información
- **Botones de navegación** con iconos y texto descriptivo

## 🗄️ Base de Datos

### Migraciones
- **Alembic** para migraciones de base de datos
- **Auto-migrate**: Se ejecuta automáticamente al iniciar la app
- **SQLite** en desarrollo, configurable para producción

## 🚀 Desarrollo

### Comandos útiles
```bash
# Tests
make test                    # Ejecutar todos los tests
make coverage               # Tests con coverage
make lint                   # Linting del código

# Desarrollo
make run                    # Ejecutar la aplicación
make install               # Instalar dependencias
make clean                 # Limpiar archivos generados
```

### Configuración
- **Entornos**: `development`, `test`, `production`
- **Configuración**: `config.py` con clases por entorno
- **Secrets**: `SECRET_KEY` y otras configuraciones sensibles

## 📁 Organización de Archivos

### Rutas
- **Estructura**: `app/src/presentation/routes/`
- **Paquetes**: Agrupar por funcionalidad (`dashboard/`, `transactions/`)
- **Naming**: `*_routes.py` para archivos de rutas

### Templates
- **Estructura**: `app/templates/`
- **Subcarpetas**: Por funcionalidad (`dashboard/yearly/`, `dashboard/monthly/`)
- **Naming**: Descriptivo (`monthly_dashboard.html`, `empty_monthly_dashboard.html`)

## 🔧 Consideraciones Técnicas

### Manejo de errores
- **404**: Redirigir al dashboard principal
- **Validación**: Meses entre 1-12, años válidos
- **Redirecciones**: Usar `follow_redirects=True` en tests

### Navegación entre fechas
- **Lógica de meses**: Enero → Diciembre anterior, Diciembre → Enero siguiente
- **Años**:**: Manejar cambio de año correctamente
- **URLs**: Formato `/dashboard/<year>/<month>`

### Datos de prueba
- **Transacciones**: Usar `TransactionRepository` para crear datos de prueba
- **Fechas**: Usar `date()` para fechas específicas
- **Montos**: Usar `Decimal` para cantidades monetarias

## 🎯 Mejores Prácticas

### Código
- **Seguir la arquitectura existente** (CQRS, Repository Pattern)
- **Usar tipos de datos apropiados** (Decimal para dinero, date para fechas)
- **Mantener consistencia** con el estilo de código existente
- **Evitar abuso de comentarios** en el código. Solo cuando algunas líneas tengan lógica compleja y el comentario aporte valor significativo

### Testing
- **Cobertura completa** de nuevas funcionalidades
- **Tests E2E** para flujos de usuario
- **Tests unitarios** para lógica de negocio
- **Verificar navegación** entre páginas

### UI/UX
- **Consistencia visual** con el resto de la aplicación
- **Navegación intuitiva** entre meses/años
- **Mensajes claros** para estados vacíos
- **Responsive design** con Bootstrap

## 📝 Notas Importantes

- **Siempre ejecutar `make test`** antes de finalizar cualquier trabajo
- **Mantener compatibilidad** con funcionalidades existentes
- **Usar las traducciones existentes** en lugar de hardcodear texto
- **Seguir la estructura de paquetes** establecida
- **Documentar cambios** en comentarios cuando sea necesario

