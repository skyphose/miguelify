# Private overlay - template

Copy this file to `references/private.md` and fill it in. `.gitignore` excludes the
real one and `tools/voicecheck.py` refuses to run if it ever gets committed.

Only backticked strings under the `## Leak list` heading are used. Each one is matched
at word boundaries, case-sensitively when it contains an uppercase letter, and a `.x`
octet in an address means "any number". Everything else in this file is notes to
yourself. Keep entries specific: a bare first name or a common word will flag half of
every document.

## Leak list

Home and account:

- `/Users/<your-macos-username>`
- `<your-personal-email>@example.com`

Machines and network:

- hostnames: `<machine-one>`, `<machine-two>`
- VPN range `100.x.x.x`, LAN ranges `192.168.x.x`, `10.x.x.x`

Affiliations and data:

- `<SCHOOL>`, `<EMPLOYER>`, and any student, staff or program data from either

Anything else that must never leave this machine:

- `<private-project-name>`
- `<internal-dashboard-name>`
