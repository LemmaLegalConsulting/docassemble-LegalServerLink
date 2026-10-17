The scenario chooses the document/letter path (which uploads generated files to the case), with the bundled SampleLetterhead1 template. The final_letter page is the actual terminal result. It does not use the email branch.

Provision a disposable LegalServer demo environment with a synthetic matter 00000000-0000-4000-8000-000000000001 and user 00000000-0000-4000-8000-000000000002 (or replace the fixture UUIDs with equivalent seeded records), the required API token, and a signed-in docassemble user. API responses must include a client, case, primary assignment and current user. This package fetches those records before asking letter questions. A plain isolated server lacks this environment, so the enabled test currently fails visibly and this PR remains draft.

Packaging fix: the distribution and package-data names now match the actual LegalServerLink directory, so installed YAML and templates are included. The docassemble platform itself is supplied by the isolated server.
