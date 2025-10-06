# Page snapshot

```yaml
- generic [active] [ref=e1]:
  - generic [ref=e4]:
    - generic [ref=e5]:
      - heading "ClassSphere" [level=2] [ref=e6]
      - paragraph [ref=e7]: Crea tu cuenta
    - generic [ref=e8]:
      - generic [ref=e9]:
        - generic [ref=e10]:
          - generic [ref=e11]: Nombre completo
          - textbox "Nombre completo" [ref=e12]
        - generic [ref=e13]:
          - generic [ref=e14]: Email
          - textbox "Email" [ref=e15]
        - generic [ref=e16]:
          - generic [ref=e17]: Contraseña
          - textbox "Contraseña" [ref=e18]
          - paragraph [ref=e19]: La contraseña debe tener al menos 8 caracteres y contener letras y números.
      - button "Crear cuenta" [ref=e21] [cursor=pointer]:
        - generic [ref=e22] [cursor=pointer]: Crear cuenta
      - paragraph [ref=e24]:
        - text: ¿Ya tienes una cuenta?
        - link "Inicia sesión aquí" [ref=e25]:
          - /url: /login
  - generic [ref=e28]:
    - generic [ref=e30]: "TS2305: Module '\"../../services/metrics.service\"' has no exported member 'MetricCardData'."
    - generic [ref=e31]:
      - text: src
      - generic [ref=e32] [cursor=pointer]: /app/components/dashboard/student-dashboard.component.ts:6:25
    - generic [ref=e33]:
      - text: Click outside, press
      - generic [ref=e34]: Esc
      - text: key, or fix the code to dismiss.
```