# GitHub Rulesets

This directory stores GitHub repository ruleset exports for manual import or
API-based sync.

- `Protect-main-owner-control.json`: limits `main` updates to repository
  administrators and requires an approved Code Owner review for other users'
  pull requests.

GitHub does not automatically apply files in this directory. Import the JSON in
repository settings or sync it with the GitHub Rulesets API.
