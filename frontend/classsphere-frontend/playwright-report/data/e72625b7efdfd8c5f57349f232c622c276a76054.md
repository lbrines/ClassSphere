# Page snapshot

```yaml
- generic [active] [ref=e1]:
  - generic [ref=e5]:
    - generic [ref=e6]:
      - heading "ClassSphere" [level=2] [ref=e7]
      - paragraph [ref=e8]: Sign in to your account
    - button "Sign in with Google" [ref=e10] [cursor=pointer]:
      - img [ref=e11] [cursor=pointer]
      - generic [ref=e16] [cursor=pointer]: Sign in with Google
    - generic [ref=e21]: Or continue with email
    - generic [ref=e22]:
      - generic [ref=e23]:
        - generic [ref=e24]:
          - generic [ref=e25]: Email address
          - textbox "Email address" [ref=e26]
        - generic [ref=e27]:
          - generic [ref=e28]: Password
          - textbox "Password" [ref=e29]
      - button "Sign in" [disabled] [ref=e31]:
        - generic [ref=e32]: Sign in
      - paragraph [ref=e34]:
        - text: Don't have an account?
        - link "Sign up here" [ref=e35] [cursor=pointer]:
          - /url: /register
    - button "Demo Users (Testing Only)" [ref=e38] [cursor=pointer]:
      - img [ref=e39] [cursor=pointer]
      - text: Demo Users (Testing Only)
  - generic [ref=e43]:
    - generic [ref=e45]: "TS1206: Decorators are not valid here."
    - generic [ref=e46]:
      - text: src
      - generic [ref=e47] [cursor=pointer]: /app/components/login/login.component.ts:14:0
    - generic [ref=e49]:
      - text: Click outside, press
      - generic [ref=e50]: Esc
      - text: key, or fix the code to dismiss.
```