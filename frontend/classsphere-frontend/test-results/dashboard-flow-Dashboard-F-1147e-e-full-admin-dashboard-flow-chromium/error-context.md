# Page snapshot

```yaml
- generic [ref=e5]:
  - generic [ref=e6]:
    - heading "ClassSphere" [level=2] [ref=e7]
    - paragraph [ref=e8]: Crea tu cuenta
  - generic [ref=e9]:
    - generic [ref=e10]:
      - generic [ref=e11]:
        - generic [ref=e12]: Nombre completo
        - textbox "Nombre completo" [ref=e13]: Test Admin
      - generic [ref=e14]:
        - generic [ref=e15]: Email
        - textbox "Email" [ref=e16]: admin@test.com
      - generic [ref=e17]:
        - generic [ref=e18]: Contraseña
        - textbox "Contraseña" [active] [ref=e19]: StrongPassword123!
        - paragraph [ref=e20]: La contraseña debe tener al menos 8 caracteres y contener letras y números.
    - button "Crear cuenta" [ref=e22] [cursor=pointer]:
      - generic [ref=e23] [cursor=pointer]: Crear cuenta
    - paragraph [ref=e25]:
      - text: ¿Ya tienes una cuenta?
      - link "Inicia sesión aquí" [ref=e26] [cursor=pointer]:
        - /url: /login
```