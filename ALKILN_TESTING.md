The scenario chooses the document/letter path (which uploads generated files to the case), with the bundled SampleLetterhead1 template. The final_letter page is the actual terminal result. It does not use the email branch.

Provision a disposable LegalServer demo environment with a synthetic matter 00000000-0000-4000-8000-000000000001 and user 00000000-0000-4000-8000-000000000002 (or replace the fixture UUIDs with equivalent seeded records), the required API token, and a signed-in docassemble user. API responses must include a client, case, primary assignment and current user. This package fetches those records before asking letter questions. A plain isolated server lacks this environment, so the enabled test currently fails visibly and this PR remains draft.

Packaging fix: the distribution and package-data names now match the actual LegalServerLink directory, so installed YAML and templates are included. The docassemble platform itself is supplied by the isolated server.

For the seeded fixture site, the precise configuration is:

```yaml
legalserver:
  alkiln-demo:
    bearer: "<disposable demo API token>"
    expiration: "<future ISO timestamp>"
```

The interview normalizes abbreviation `alkiln` plus type `Demo` to `alkiln-demo`. The token must permit matter, user, assignment, and document access for the synthetic records above.

The package also includes a Flask compatibility repair: API preload resolves app/CSRF in both older and newer docassemble module layouts. Four compatibility/authentication unit cases passed. This removes an import blocker for dependent interviews; it does not replace the LegalServer integration or make this sample-letter scenario pass without its environment.

Create repository secret `ALKILN_DOCASSEMBLE_CONFIG` containing a complete disposable docassemble YAML configuration. The workflow passes it as `CONFIG_CONTENTS` to the temporary server; this is actual config wiring, not just a documented secret name. Configure only test service accounts/endpoints. This does not provision private dependency Git access.

The fixture now signs into the temporary server using its synthetic admin credentials from the isolated action outputs (`ALKILN_ADMIN_EMAIL`/`ALKILN_ADMIN_PASSWORD`). No production login is used. Service authentication and any required profile/database seed data remain separate prerequisites.
