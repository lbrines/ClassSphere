# Page snapshot

```yaml
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
    - generic [ref=e21]: Por favor, completa todos los campos
    - button "Crear cuenta" [active] [ref=e23] [cursor=pointer]:
      - generic [ref=e24] [cursor=pointer]: Crear cuenta
    - paragraph [ref=e26]:
      - text: ¿Ya tienes una cuenta?
      - link "Inicia sesión aquí" [ref=e27]:
        - /url: /login
```