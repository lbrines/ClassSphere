# Page snapshot

```yaml
- generic [active] [ref=e1]:
  - generic [ref=e4]:
    - generic [ref=e5]:
      - heading "ClassSphere" [level=2] [ref=e6]
      - paragraph [ref=e7]: Sign in to your account
    - button "Sign in with Google" [ref=e9] [cursor=pointer]:
      - img [ref=e10] [cursor=pointer]
      - generic [ref=e15] [cursor=pointer]: Sign in with Google
    - generic [ref=e20]: Or continue with email
    - generic [ref=e21]:
      - generic [ref=e22]:
        - generic [ref=e23]:
          - generic [ref=e24]: Email address
          - textbox "Email address" [ref=e25]
        - generic [ref=e26]:
          - generic [ref=e27]: Password
          - textbox "Password" [ref=e28]
      - button "Sign in" [disabled] [ref=e30]:
        - generic [ref=e31]: Sign in
      - paragraph [ref=e33]:
        - text: Don't have an account?
        - link "Sign up here" [ref=e34]:
          - /url: /register
    - button "Demo Users (Testing Only)" [ref=e37] [cursor=pointer]:
      - img [ref=e38] [cursor=pointer]
      - text: Demo Users (Testing Only)
  - generic [ref=e42]:
    - generic [ref=e44]: "TS2305: Module '\"../../services/metrics.service\"' has no exported member 'MetricCardData'."
    - generic [ref=e45]:
      - text: src
      - generic [ref=e46] [cursor=pointer]: /app/components/dashboard/student-dashboard.component.ts:6:25
    - generic [ref=e47]:
      - text: Click outside, press
      - generic [ref=e48]: Esc
      - text: key, or fix the code to dismiss.
```