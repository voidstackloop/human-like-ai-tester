# Security Policy

## Supported versions

| Version | Supported          |
| ------- | ------------------ |
| 0.2.x   | :white_check_mark: |
| < 0.2   | :x:                |

## Reporting a vulnerability

This tool intentionally generates messy, hostile-looking input — that is its
job as a tester. If you find a vulnerability in the tester itself (for
example, the mock demo server or report generation executing untrusted
content), please report it through the project's issue tracker with the
`security` label, including:

- A description of the issue and its impact
- Steps to reproduce (a minimal command or script)
- The version you tested (`human-tester --version`)

We aim to acknowledge reports within 3 business days and to ship a fix or
mitigation promptly. Please avoid opening a public issue with exploit details
before a fix is available; describe the impact and offer details privately to
a maintainer instead.
