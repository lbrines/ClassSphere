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
        - textbox "Nombre completo" [ref=e13]: Test User
      - generic [ref=e14]:
        - generic [ref=e15]: Email
        - textbox "Email" [ref=e16]: invalid-email
      - generic [ref=e17]:
        - generic [ref=e18]: Contraseña
        - textbox "Contraseña" [ref=e19]: password123
        - paragraph [ref=e20]: La contraseña debe tener al menos 8 caracteres y contener letras y números.
    - generic [ref=e22]: code=400, message=Invalid email format
    - button "Crear cuenta" [ref=e24] [cursor=pointer]:
      - generic [ref=e25] [cursor=pointer]: Crear cuenta
    - paragraph [ref=e27]:
      - text: ¿Ya tienes una cuenta?
      - link "Inicia sesión aquí" [ref=e28] [cursor=pointer]:
        - /url: /login
```