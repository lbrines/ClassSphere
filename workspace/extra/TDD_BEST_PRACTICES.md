# TDD Best Practices - Dashboard Educativo
## Mejores Prácticas para Test-Driven Development

**Fecha:** 2025-10-02  
**Basado en:** Fuentes oficiales y documentación confiable  
**Proyecto:** Dashboard Educativo Full-Stack

---

## 📚 Fuentes Oficiales Consultadas

### Fuentes Fundamentales
1. **Mozilla Developer Network (MDN)** - Testing frameworks y mejores prácticas
2. **pytest Documentation** - Convenciones y estructura de tests Python
3. **Vitest Documentation** - Testing para React y TypeScript
4. **React Testing Library** - Principios de testing centrados en el usuario
5. **FastAPI Documentation** - Testing de APIs con pytest
6. **Kent Beck** - Creador de TDD, metodología original

### Fuentes Especializadas en LLM + Testing
7. **Schäfer et al.** - [An Empirical Evaluation of Using Large Language Models for Automated Unit Test Generation](https://arxiv.org/abs/2302.06527) - Baseline de cobertura LLM: ~70.2% líneas, ~52.8% ramas
8. **Pizzorno & Berger** - [CoverUp: Coverage-Guided LLM-Based Test Generation](https://arxiv.org/abs/2403.16218) - Mejoras con feedback iterativo: ~80% módulos, ~90% overall
9. **Ryan et al.** - [SymPrompt: Code-Aware Prompting, Coverage-Guided Test Generation](https://dl.acm.org/doi/10.1145/3643769) - Prompting code-aware incrementa cobertura significativamente
10. **Alshahwan et al.** - [Automated Unit Test Improvement using LLMs at Meta](https://arxiv.org/abs/2402.09171) - Despliegue industrial en Instagram/Facebook
11. **Alshahwan et al.** - [Observation-based unit test generation at Meta](https://arxiv.org/abs/2402.06111) - 518 tests en producción, 9.6M ejecuciones CI
12. **Google Testing Blog** - [Code Coverage Best Practices](https://testing.googleblog.com/2020/08/code-coverage-best-practices.html) - Guías de cobertura: 60% aceptable, 75% commendable, 90% exemplary
13. **Google Testing Blog** - [Code coverage goal: 80% and no less!](https://testing.googleblog.com/2010/07/code-coverage-goal-80-and-no-less.html) - Regla simple para contextos específicos

---

## 🎯 Principios Fundamentales de TDD

### Ciclo Red-Green-Refactor

```
1. 🔴 RED: Escribir un test que falle
   ↓
2. 🟢 GREEN: Escribir el código mínimo para que pase
   ↓
3. 🔵 REFACTOR: Mejorar el código manteniendo tests pasando
   ↓
4. Repetir
```

### Reglas de Oro

1. **Nunca escribas código de producción sin un test fallando**
2. **Escribe solo el código necesario para pasar el test**
3. **Refactoriza solo cuando los tests estén en verde**
4. **Un test debe probar una sola cosa**
5. **Los tests deben ser independientes entre sí**

---

## 🔧 BACKEND: TDD con Python + FastAPI + pytest

### 1. Estructura de Archivos (pytest)

**Convención Oficial de pytest:**

```
backend/
├── app/
│   ├── services/
│   │   └── auth_service.py          # Código de producción
│   └── api/
│       └── endpoints/
│           └── auth.py               # Endpoints
└── tests/
    ├── unit/
    │   └── services/
    │       └── test_auth_service.py  # ✅ CORRECTO: test_*.py
    │       └── auth_service_test.py  # ✅ TAMBIÉN VÁLIDO: *_test.py
    │       └── auth.service.test.py  # ❌ INCORRECTO: No detectado
    └── integration/
        └── test_auth.py              # ✅ CORRECTO
        └── test_auth_endpoints.py    # ✅ CORRECTO
```

**Configuración pytest.ini (Optimizada para LLM):**

```ini
[pytest]
testpaths = tests
python_files = test_*.py *_test.py    # ✅ Convenciones aceptadas
python_classes = Test*
python_functions = test_*
addopts = 
    --cov=app
    --cov-branch                    # ✅ NUEVO: Medición de cobertura de ramas
    --cov-report=term-missing
    --cov-report=html
    --cov-fail-under=80             # ✅ AUMENTADO: 70% → 80% (basado en estudios LLM)
    -v
asyncio_mode = auto
markers =
    unit: Unit tests
    integration: Integration tests
    slow: Slow running tests
    critical: Critical business logic tests
```

**⚠️ IMPORTANTE:** Los umbrales han sido ajustados basándose en estudios empíricos de generación de tests con LLMs:
- **Baseline LLM sin guía:** ~70.2% líneas, ~52.8% ramas (Schäfer et al.)
- **Con feedback iterativo:** ~80% módulos, ~90% overall (Pizzorno & Berger)
- **Meta industrial:** Verificación de mejora real antes de proponer tests (Alshahwan et al.)

### 2. Nomenclatura de Tests

**Patrón recomendado:**

```python
# test_auth_service.py

def test_authenticate_user_with_valid_credentials():
    """Should return user when credentials are valid"""
    pass

def test_authenticate_user_with_invalid_password():
    """Should raise AuthenticationError when password is invalid"""
    pass

def test_authenticate_user_with_nonexistent_email():
    """Should raise UserNotFoundError when email doesn't exist"""
    pass
```

**Formato del nombre:**
- `test_<función>_<escenario>_<resultado_esperado>`
- Ejemplo: `test_login_with_invalid_token_returns_401`

### 3. Estructura de Un Test (Arrange-Act-Assert)

```python
# tests/unit/services/test_auth_service.py
import pytest
from app.services.auth_service import AuthService
from app.core.exceptions import AuthenticationError

def test_authenticate_user_with_valid_credentials():
    # ARRANGE: Preparar datos y dependencias
    auth_service = AuthService()
    email = "test@example.com"
    password = "valid_password"
    
    # ACT: Ejecutar la función bajo test
    result = auth_service.authenticate_user(email, password)
    
    # ASSERT: Verificar resultados
    assert result is not None
    assert result.email == email
    assert result.is_authenticated is True

def test_authenticate_user_with_invalid_password_raises_error():
    # ARRANGE
    auth_service = AuthService()
    email = "test@example.com"
    password = "wrong_password"
    
    # ACT & ASSERT: Para excepciones
    with pytest.raises(AuthenticationError) as exc_info:
        auth_service.authenticate_user(email, password)
    
    assert "Invalid credentials" in str(exc_info.value)
```

### 4. Tests de Integración con FastAPI

```python
# tests/integration/test_auth.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_login_endpoint_with_valid_credentials():
    # ARRANGE
    payload = {
        "email": "admin@educational.dashboard",
        "password": "admin123"
    }
    
    # ACT
    response = client.post("/api/v1/auth/login", json=payload)
    
    # ASSERT
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "token" in data["data"]
    assert data["data"]["user"]["email"] == payload["email"]

def test_login_endpoint_with_invalid_credentials_returns_401():
    # ARRANGE
    payload = {
        "email": "admin@educational.dashboard",
        "password": "wrong_password"
    }
    
    # ACT
    response = client.post("/api/v1/auth/login", json=payload)
    
    # ASSERT
    assert response.status_code == 401
    data = response.json()
    assert "error" in data
    assert data["error"]["code"] == "AUTH_INVALID_CREDENTIALS"
```

### 5. Fixtures y Mocks

```python
# tests/conftest.py
import pytest
from app.services.mock_service import MockService

@pytest.fixture
def mock_service():
    """Fixture para proporcionar MockService"""
    service = MockService()
    return service

@pytest.fixture
def test_user():
    """Fixture para proporcionar usuario de prueba"""
    return {
        "id": "test-001",
        "email": "test@example.com",
        "role": "student",
        "name": "Test User"
    }

# Uso en tests
def test_get_user_by_email(mock_service, test_user):
    # ARRANGE
    email = test_user["email"]
    
    # ACT
    result = mock_service.get_user_by_email(email)
    
    # ASSERT
    assert result is not None
    assert result["email"] == email
```

### 6. Tests Asíncronos

```python
# tests/unit/services/test_google_service.py
import pytest
from app.services.google_service import GoogleService

@pytest.mark.asyncio
async def test_fetch_courses_returns_list():
    # ARRANGE
    google_service = GoogleService()
    
    # ACT
    courses = await google_service.fetch_courses()
    
    # ASSERT
    assert isinstance(courses, list)
    assert len(courses) > 0
    assert "id" in courses[0]
    assert "name" in courses[0]
```

### 7. Parametrización de Tests

```python
@pytest.mark.parametrize("email,password,expected", [
    ("admin@educational.dashboard", "admin123", True),
    ("teacher@educational.dashboard", "teacher123", True),
    ("invalid@email.com", "wrong", False),
    ("", "", False),
])
def test_authenticate_user_with_various_credentials(email, password, expected):
    # ARRANGE
    auth_service = AuthService()
    
    # ACT
    if expected:
        result = auth_service.authenticate_user(email, password)
        # ASSERT
        assert result is not None
    else:
        # ASSERT
        with pytest.raises(Exception):
            auth_service.authenticate_user(email, password)
```

---

## ⚛️ FRONTEND: TDD con React + TypeScript + Vitest

### 1. Estructura de Archivos (Vitest)

**Convención recomendada:**

```
frontend/src/
├── components/
│   ├── auth/
│   │   ├── LoginForm.tsx                   # Componente
│   │   ├── LoginForm.test.tsx              # ✅ Junto al componente
│   │   └── __tests__/                      # ✅ O en subdirectorio
│   │       └── LoginForm.test.tsx
│   └── dashboards/
│       ├── StudentDashboard.tsx
│       └── StudentDashboard.test.tsx       # ✅ Junto al componente
├── hooks/
│   ├── useAuth.ts
│   └── useAuth.test.ts                     # ✅ Mismo directorio
└── test/
    └── setup.ts                             # Setup global
```

**Ambas convenciones son válidas:**
- ✅ `Component.test.tsx` junto al componente
- ✅ `__tests__/Component.test.tsx` en subdirectorio

**Configuración vitest.config.ts (Optimizada para LLM):**

```typescript
import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'
import { resolve } from 'path'

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    setupFiles: ['./src/test/setup.ts'],
    globals: true,
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: [
        'node_modules/',
        'src/test/',
      ],
      thresholds: {
        lines: 80,        // ✅ NUEVO: Gate mínimo para líneas
        functions: 80,    // ✅ NUEVO: Gate mínimo para funciones
        statements: 80,   // ✅ NUEVO: Gate mínimo para statements
        branches: 65      // ✅ NUEVO: Gate mínimo para ramas (más permisivo)
      }
    },
  },
  resolve: {
    alias: {
      '@': resolve(__dirname, './src'),
    },
  },
})
```

**⚠️ IMPORTANTE:** Los thresholds están basados en estudios empíricos:
- **Líneas/Funciones/Statements:** 80% (basado en mejoras con feedback iterativo)
- **Branches:** 65% (más permisivo, ya que LLMs tienen dificultad con lógica condicional compleja)

### 2. Setup Global

```typescript
// src/test/setup.ts
import '@testing-library/jest-dom'
import { vi } from 'vitest'

// Mock global de hooks comunes
vi.mock('@/hooks/useTranslation', () => ({
  useTranslation: () => ({
    t: (key: string) => key,
  }),
}))

// Mock de next/navigation si usas Next.js
vi.mock('next/navigation', () => ({
  useRouter: () => ({
    push: vi.fn(),
    replace: vi.fn(),
    back: vi.fn(),
  }),
  usePathname: () => '/',
}))
```

### 3. Testing de Componentes con React Testing Library

**Principios de React Testing Library:**
- **Prueba como el usuario interactúa**
- **No pruebes detalles de implementación**
- **Busca elementos por rol, label o texto, no por clase CSS**

```typescript
// StudentDashboard.test.tsx
import { describe, it, expect, vi } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import StudentDashboard from './StudentDashboard'

describe('StudentDashboard Component', () => {
  const mockData = {
    studentId: 'student-001',
    studentName: 'Alice Johnson',
    progress: {
      overall: 0.75,
      coursesCompleted: 3,
      coursesInProgress: 2,
    },
    courses: [
      { id: 'course-001', name: 'Math 101', progress: 0.80, grade: 85 },
      { id: 'course-002', name: 'Science 101', progress: 0.70, grade: 78 },
    ],
  }

  describe('Rendering', () => {
    it('should render dashboard title', () => {
      // ARRANGE & ACT
      render(<StudentDashboard data={mockData} />)
      
      // ASSERT
      expect(screen.getByText(/student dashboard/i)).toBeInTheDocument()
    })

    it('should display student name', () => {
      // ARRANGE & ACT
      render(<StudentDashboard data={mockData} />)
      
      // ASSERT
      expect(screen.getByText(/alice johnson/i)).toBeInTheDocument()
    })

    it('should display progress stats', () => {
      // ARRANGE & ACT
      render(<StudentDashboard data={mockData} />)
      
      // ASSERT
      expect(screen.getByText('Completed')).toBeInTheDocument()
      expect(screen.getByText('3')).toBeInTheDocument()
    })
  })

  describe('User Interactions', () => {
    it('should handle course click', async () => {
      // ARRANGE
      const onCourseClick = vi.fn()
      const user = userEvent.setup()
      
      render(
        <StudentDashboard 
          data={mockData} 
          onCourseClick={onCourseClick} 
        />
      )
      
      // ACT
      const courseButton = screen.getByRole('button', { name: /math 101/i })
      await user.click(courseButton)
      
      // ASSERT
      expect(onCourseClick).toHaveBeenCalledWith('course-001')
    })
  })

  describe('States', () => {
    it('should show loading state', () => {
      // ARRANGE & ACT
      render(<StudentDashboard loading={true} />)
      
      // ASSERT
      expect(screen.getByText(/loading/i)).toBeInTheDocument()
    })

    it('should show error state', () => {
      // ARRANGE & ACT
      render(<StudentDashboard error="Network error" />)
      
      // ASSERT
      expect(screen.getByText(/network error/i)).toBeInTheDocument()
    })
  })
})
```

### 4. Testing de Hooks Personalizados

```typescript
// useAuth.test.ts
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { renderHook, waitFor } from '@testing-library/react'
import { useAuth } from './useAuth'

describe('useAuth Hook', () => {
  beforeEach(() => {
    // Reset mocks antes de cada test
    vi.clearAllMocks()
  })

  it('should return initial state', () => {
    // ARRANGE & ACT
    const { result } = renderHook(() => useAuth())
    
    // ASSERT
    expect(result.current.user).toBeNull()
    expect(result.current.isAuthenticated).toBe(false)
    expect(result.current.isLoading).toBe(true)
  })

  it('should login successfully with valid credentials', async () => {
    // ARRANGE
    const { result } = renderHook(() => useAuth())
    
    // ACT
    await result.current.login('test@example.com', 'password123')
    
    // ASSERT
    await waitFor(() => {
      expect(result.current.isAuthenticated).toBe(true)
      expect(result.current.user).not.toBeNull()
      expect(result.current.user?.email).toBe('test@example.com')
    })
  })

  it('should handle login error', async () => {
    // ARRANGE
    const { result } = renderHook(() => useAuth())
    
    // ACT
    await result.current.login('invalid@example.com', 'wrong')
    
    // ASSERT
    await waitFor(() => {
      expect(result.current.isAuthenticated).toBe(false)
      expect(result.current.error).toBeDefined()
    })
  })
})
```

### 5. Query Priorities (React Testing Library)

**Orden de prioridad para seleccionar elementos:**

1. **`getByRole`** - ✅ MEJOR (accesibilidad)
   ```typescript
   screen.getByRole('button', { name: /submit/i })
   screen.getByRole('textbox', { name: /email/i })
   ```

2. **`getByLabelText`** - ✅ MUY BUENO (forms)
   ```typescript
   screen.getByLabelText(/email address/i)
   ```

3. **`getByPlaceholderText`** - ⚠️ ACEPTABLE
   ```typescript
   screen.getByPlaceholderText(/enter your email/i)
   ```

4. **`getByText`** - ✅ BUENO (contenido visible)
   ```typescript
   screen.getByText(/welcome back/i)
   ```

5. **`getByTestId`** - ⚠️ ÚLTIMO RECURSO
   ```typescript
   screen.getByTestId('custom-element')
   ```

### 6. Queries Variants

```typescript
// getBy* - Lanza error si no encuentra
screen.getByRole('button')  // ❌ Error si no existe

// queryBy* - Retorna null si no encuentra
screen.queryByRole('button')  // ✅ null si no existe

// findBy* - Async, espera hasta encontrar
await screen.findByRole('button')  // ✅ Espera hasta 1000ms

// getAllBy* - Retorna array
screen.getAllByRole('listitem')  // ✅ [item1, item2, ...]
```

### 7. Testing de Async Operations

```typescript
// GoogleConnect.test.tsx
import { describe, it, expect, vi } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import GoogleConnect from './GoogleConnect'

describe('GoogleConnect Component', () => {
  it('should fetch and display courses on connect', async () => {
    // ARRANGE
    const user = userEvent.setup()
    render(<GoogleConnect />)
    
    // ACT
    const connectButton = screen.getByRole('button', { name: /connect/i })
    await user.click(connectButton)
    
    // ASSERT
    // Esperar a que aparezca el loading
    expect(screen.getByText(/loading/i)).toBeInTheDocument()
    
    // Esperar a que aparezcan los cursos
    await waitFor(() => {
      expect(screen.getByText(/math 101/i)).toBeInTheDocument()
    }, { timeout: 3000 })
  })
})
```

---

## 🎯 Mejores Prácticas Generales

### 1. Nombres Descriptivos

**❌ MAL:**
```typescript
test('test1', () => { ... })
test('should work', () => { ... })
```

**✅ BIEN:**
```typescript
test('should authenticate user with valid credentials', () => { ... })
test('should return 401 when token is expired', () => { ... })
```

### 2. Un Test, Un Concepto

**❌ MAL:**
```typescript
test('login functionality', () => {
  // Prueba login
  // Prueba logout
  // Prueba refresh token
  // Demasiadas cosas
})
```

**✅ BIEN:**
```typescript
test('should login user with valid credentials', () => { ... })
test('should logout user and clear session', () => { ... })
test('should refresh token when expired', () => { ... })
```

### 3. Tests Independientes

**❌ MAL:**
```typescript
let sharedData;

test('test1', () => {
  sharedData = createData()  // ❌ Estado compartido
})

test('test2', () => {
  expect(sharedData).toBeDefined()  // ❌ Depende de test1
})
```

**✅ BIEN:**
```typescript
test('test1', () => {
  const data = createData()  // ✅ Estado local
  expect(data).toBeDefined()
})

test('test2', () => {
  const data = createData()  // ✅ Independiente
  expect(data).toBeDefined()
})
```

### 4. Tests Rápidos

- **Unit tests:** < 50ms cada uno
- **Integration tests:** < 500ms cada uno
- **E2E tests:** Pueden ser más lentos

```python
# Marcar tests lentos
@pytest.mark.slow
def test_full_sync_operation():
    pass
```

### 5. Cobertura de Tests (Optimizada para LLM)

**Objetivos basados en estudios empíricos:**

| Tipo | Mínimo | Recomendado | Críticos |
|------|--------|-------------|----------|
| **Líneas** | 80% | 85% | 90% |
| **Funciones** | 80% | 85% | 90% |
| **Branches** | 65% | 75% | 80% |
| **Statements** | 80% | 85% | 90% |

```bash
# Backend (con branch coverage)
pytest --cov=app --cov-branch --cov-report=html

# Frontend (con thresholds)
pnpm test -- --coverage
```

**⚠️ IMPORTANTE - Evidencia Empírica:**
- **Baseline LLM sin guía:** ~70.2% líneas, ~52.8% ramas (Schäfer et al.)
- **Con feedback iterativo:** ~80% módulos, ~90% overall (Pizzorno & Berger)
- **Meta industrial:** Verificación de mejora real antes de proponer tests (Alshahwan et al.)

**Priorizar cobertura en:**
- ✅ Lógica de negocio crítica (90% líneas, 80% ramas)
- ✅ Manejo de errores (90% líneas, 80% ramas)
- ✅ Casos edge (85% líneas, 75% ramas)
- ⚠️ No obsesionarse con 100% (ley de rendimientos decrecientes)

### 6. Organización de Tests

```
tests/
├── unit/                    # Tests unitarios aislados
│   ├── services/
│   └── utils/
├── integration/             # Tests de integración
│   ├── api/
│   └── database/
├── e2e/                     # Tests end-to-end
│   └── user_flows/
└── fixtures/                # Datos de prueba compartidos
    └── test_data.json
```

---

## 📋 Checklist de TDD

### Antes de Empezar
- [ ] Entiendo el requisito que voy a implementar
- [ ] Sé qué comportamiento espero
- [ ] Tengo claro qué casos edge considerar

### Durante el Desarrollo
- [ ] ✍️ Escribí el test primero
- [ ] 🔴 Verifiqué que el test falla (RED)
- [ ] 💻 Escribí el código mínimo necesario
- [ ] 🟢 El test ahora pasa (GREEN)
- [ ] 🔧 Refactoricé manteniendo tests verdes (REFACTOR)
- [ ] 📝 El nombre del test es descriptivo
- [ ] 🎯 El test prueba una sola cosa
- [ ] ⚡ El test es rápido (< 50ms unit, < 500ms integration)

### Después de Implementar
- [ ] ✅ Todos los tests pasan
- [ ] 📊 La cobertura cumple el mínimo (≥80% líneas, ≥65% ramas)
- [ ] 🎯 Módulos críticos alcanzan ≥90% líneas, ≥80% ramas
- [ ] 🔍 Los tests son legibles y mantenibles
- [ ] 📚 Documenté comportamientos complejos
- [ ] 🗑️ Eliminé tests duplicados o innecesarios
- [ ] 🔄 Verifico mejora real de cobertura (no solo números)

---

## 🚀 Comandos Útiles

### Backend (pytest)
```bash
# Ejecutar todos los tests
pytest

# Tests con cobertura
pytest --cov=app --cov-report=html

# Tests específicos
pytest tests/unit/services/test_auth_service.py

# Tests con marca específica
pytest -m unit
pytest -m integration

# Tests en modo watch (con pytest-watch)
ptw

# Tests verbose
pytest -v

# Tests con output completo
pytest -vv
```

### Frontend (Vitest)
```bash
# Ejecutar todos los tests
pnpm test

# Tests en modo watch
pnpm test --watch

# Tests con cobertura
pnpm test --coverage

# Tests específicos
pnpm test StudentDashboard

# Tests en modo UI
pnpm test --ui

# Tests verbose
pnpm test --reporter=verbose
```

---

## 📚 Referencias Oficiales

### Documentación Técnica
1. **pytest Documentation:** https://docs.pytest.org/
2. **Vitest Documentation:** https://vitest.dev/
3. **React Testing Library:** https://testing-library.com/react
4. **FastAPI Testing:** https://fastapi.tiangolo.com/tutorial/testing/
5. **MDN Testing Guide:** https://developer.mozilla.org/en-US/docs/Learn/Tools_and_testing
6. **Kent Beck - TDD by Example:** Libro fundamental sobre TDD

### Estudios Empíricos LLM + Testing
7. **Schäfer et al.** - [An Empirical Evaluation of Using Large Language Models for Automated Unit Test Generation](https://arxiv.org/abs/2302.06527) - Baseline: ~70.2% líneas, ~52.8% ramas
8. **Pizzorno & Berger** - [CoverUp: Coverage-Guided LLM-Based Test Generation](https://arxiv.org/abs/2403.16218) - Feedback iterativo: ~80% módulos, ~90% overall
9. **Ryan et al.** - [SymPrompt: Code-Aware Prompting, Coverage-Guided Test Generation](https://dl.acm.org/doi/10.1145/3643769) - Prompting code-aware
10. **Alshahwan et al.** - [Automated Unit Test Improvement using LLMs at Meta](https://arxiv.org/abs/2402.09171) - Despliegue industrial
11. **Alshahwan et al.** - [Observation-based unit test generation at Meta](https://arxiv.org/abs/2402.06111) - 518 tests, 9.6M ejecuciones CI

### Guías de Cobertura
12. **Google Testing Blog** - [Code Coverage Best Practices](https://testing.googleblog.com/2020/08/code-coverage-best-practices.html) - 60% aceptable, 75% commendable, 90% exemplary
13. **Google Testing Blog** - [Code coverage goal: 80% and no less!](https://testing.googleblog.com/2010/07/code-coverage-goal-80-and-no-less.html) - Regla simple

---

## 🎓 Conclusión

TDD es una **disciplina** que requiere práctica y compromiso, pero los beneficios son significativos:

- ✅ **Mejor diseño de código** (código más modular y testeable)
- ✅ **Menos bugs en producción** (detección temprana)
- ✅ **Refactoring seguro** (confianza para cambiar código)
- ✅ **Documentación viva** (los tests documentan comportamiento)
- ✅ **Desarrollo más rápido** (menos debugging, más confianza)

### 🤖 TDD Optimizado para LLM

Con la evidencia empírica disponible, hemos ajustado los umbrales de cobertura para aprovechar las capacidades superiores de los LLMs:

- **80% líneas/funciones** (vs 70% tradicional) - Basado en estudios de feedback iterativo
- **65% ramas** (más permisivo) - Reconociendo limitaciones en lógica condicional compleja
- **90% críticos** - Para módulos de negocio críticos
- **Verificación de mejora real** - No solo números, sino calidad de tests

**Recuerda:** Los tests no son el objetivo, son una herramienta para escribir mejor software. Con LLMs, podemos aspirar a estándares más altos de manera eficiente.

---

**Última actualización:** 2025-10-02  
**Proyecto:** Dashboard Educativo  
**Mantenedor:** Leopoldo Brines

