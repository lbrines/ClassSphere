# Page snapshot

```yaml
- generic [ref=e1]:
  - generic [ref=e5]:
    - generic [ref=e6]:
      - heading "ClassSphere" [level=2] [ref=e7]
      - paragraph [ref=e8]: Inicia sesión en tu cuenta
    - generic [ref=e9]:
      - generic [ref=e10]:
        - generic [ref=e11]:
          - generic [ref=e12]: Email
          - textbox "Email" [ref=e13]: invalid-email
        - generic [ref=e14]:
          - generic [ref=e15]: Contraseña
          - textbox "Contraseña" [active] [ref=e16]: password123
      - button "Iniciar sesión" [ref=e18]:
        - generic [ref=e19]: Iniciar sesión
      - paragraph [ref=e21]:
        - text: ¿No tienes una cuenta?
        - link "Regístrate aquí" [ref=e22] [cursor=pointer]:
          - /url: /register
  - generic [ref=e25]:
    - generic [ref=e27]: "NG5002: Only void, custom and foreign elements can be self closed \"div\""
    - generic [ref=e28]:
      - text: src
      - generic [ref=e29] [cursor=pointer]: /app/components/login/login.component.ts:48:12
    - generic [ref=e30]:
      - text: Click outside, press
      - generic [ref=e31]: Esc
      - text: key, or fix the code to dismiss.
```