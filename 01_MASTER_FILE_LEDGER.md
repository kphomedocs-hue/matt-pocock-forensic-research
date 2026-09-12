# Master File Ledger

Source: frozen recursive tree of `mattpocock/skills` at commit `3cca18b368ae95cdbdebbff572ccafa662551015`, tree `6e84c093fda2026396cea9fad6a924a6da0e1452`.

Physical denominator: **164 blobs/files**.

Generated deterministically by `scripts/build_master_ledger.py`. MP-IDs are assigned in lexicographic path order. Durable per-file notes under `02_FILE_NOTES/` are authoritative for READ-or-higher status.

## Status rules

`UNREAD → READ → CONNECTIONS TRACED → VERIFIED`

A status transition requires durable evidence. A conversation summary is not evidence.

## Ledger

| MP-ID | Path | Mode/Type | Size | Blob SHA | Category | Status | Evidence | Ref-out | Ref-in | Runtime Risk | Notes |
|---|---|---|---:|---|---|---|---|---|---|---|---|
| MP-0001 | .agents/adr/0001-explicit-setup-pointer-only-for-hard-dependencies.md | 100644/blob | 1154 | 56b348d9fea2d7ee2e326fe1838215d0c94c413b | governance | READ | [MP-0001 note](02_FILE_NOTES/MP-0001.md) |  |  | MEDIUM |  |
| MP-0002 | .agents/adr/0002-ship-as-a-claude-code-plugin.md | 100644/blob | 5528 | 263d10290d60ea15119d2d3c51af5f4f08b5f178 | governance | READ | [MP-0002 note](02_FILE_NOTES/MP-0002.md) |  |  | MEDIUM |  |
| MP-0003 | .agents/install-block.md | 100644/blob | 2780 | a93751108599407637bec35c08dde6c4eb1afefe | governance | READ | [MP-0003 note](02_FILE_NOTES/MP-0003.md) |  |  | MEDIUM |  |
| MP-0004 | .agents/invocation.md | 100644/blob | 3848 | c13b8a5ea97466e14259de602c6b66e72133fef1 | governance | READ | [MP-0004 note](02_FILE_NOTES/MP-0004.md) |  |  | MEDIUM |  |
| MP-0005 | .agents/writing-docs.md | 100644/blob | 12688 | 68f9216230f2bbafefc985eccf81fcc506c14b3b | governance | READ | [MP-0005 note](02_FILE_NOTES/MP-0005.md) |  |  | MEDIUM |  |
| MP-0006 | .changeset/README.md | 100644/blob | 512 | 654c6d4750dca19541bd9803371735943bb3fe4e | changeset | READ | [MP-0006 note](02_FILE_NOTES/MP-0006.md) |  |  | LOW |  |
| MP-0007 | .changeset/add-implement-spec-skill.md | 100644/blob | 450 | 2128b7d4220ed30503e957fe8c8bbcf9b521931d | changeset | READ | [MP-0007 note](02_FILE_NOTES/MP-0007.md) |  |  | LOW |  |
| MP-0008 | .changeset/config.json | 100644/blob | 380 | 06c7350518b33bdaedd0eae254f75fd887f16963 | changeset | READ | [MP-0008 note](02_FILE_NOTES/MP-0008.md) |  |  | LOW |  |
| MP-0009 | .changeset/domain-modeling-trigger-context-adr.md | 100644/blob | 437 | 8ab6722a781dedf4d52456d6a02f83e358e62f1f | changeset | READ | [MP-0009 note](02_FILE_NOTES/MP-0009.md) |  |  | LOW |  |
| MP-0010 | .changeset/fix-yaml-frontmatter-colons.md | 100644/blob | 387 | 64f830b202aaef799c5dabe2ba53d0ab05f87efa | changeset | READ | [MP-0010 note](02_FILE_NOTES/MP-0010.md) |  |  | LOW |  |
| MP-0011 | .changeset/grilling-add-hr-between-questions.md | 100644/blob | 169 | 0fc8ee080d9d5b7ed6709af70a5d66a4b65ca5cb | changeset | READ | [MP-0011 note](02_FILE_NOTES/MP-0011.md) |  |  | LOW |  |
| MP-0012 | .changeset/grilling-remove-em-dashes.md | 100644/blob | 162 | 6cd562fb6a8b46afb9db06756deb76a2bd6688aa | changeset | READ | [MP-0012 note](02_FILE_NOTES/MP-0012.md) |  |  | LOW |  |
| MP-0013 | .changeset/remove-em-dashes-repo-wide.md | 100644/blob | 350 | a3909afb95f471194fe96430127799bb7e7df5b1 | changeset | READ | [MP-0013 note](02_FILE_NOTES/MP-0013.md) |  |  | LOW |  |
| MP-0014 | .changeset/skill-tool-invocation-terminology.md | 100644/blob | 1006 | 153b5564e6ab98f85ddb36988f72a00adfe1a716 | changeset | READ | [MP-0014 note](02_FILE_NOTES/MP-0014.md) |  |  | LOW |  |
| MP-0015 | .changeset/user-invoked-skill-invocation.md | 100644/blob | 1565 | 18e6a7c38d55a5fb75f3b4bfceb6807e95060032 | changeset | READ | [MP-0015 note](02_FILE_NOTES/MP-0015.md) |  |  | LOW |  |
| MP-0016 | .changeset/wait-what-context-map.md | 100644/blob | 191 | edaa4d6a86c16095fef8e18f8214487627a9cba2 | changeset | READ | [MP-0016 note](02_FILE_NOTES/MP-0016.md) |  |  | LOW |  |
| MP-0017 | .claude-plugin/marketplace.json | 100644/blob | 605 | 1f868cee17708d691ad71d963e847dad209d0c07 | distribution | READ | [MP-0017 note](02_FILE_NOTES/MP-0017.md) |  |  | HIGH |  |
| MP-0018 | .claude-plugin/plugin.json | 100644/blob | 1636 | 0a2e3088d2bcaaabcc02ff1c691c5e6c0f81d01d | distribution | READ | [MP-0018 note](02_FILE_NOTES/MP-0018.md) |  |  | HIGH |  |
| MP-0019 | .github/workflows/release.yml | 100644/blob | 780 | b503eff7b073afe8a08d0b25cc31efca78caea02 | ci-release | READ | [MP-0019 note](02_FILE_NOTES/MP-0019.md) |  |  | HIGH |  |
| MP-0020 | .gitignore | 100644/blob | 21 | 98dd2d8dd55043ee7a28c5ecbf08cc6a18afacaf | root | READ | [MP-0020 note](02_FILE_NOTES/MP-0020.md) |  |  | LOW |  |
| MP-0021 | .out-of-scope/mainstream-issue-trackers-only.md | 100644/blob | 1573 | 72f09fe5a9cb64bd55a46d45e116cd538d48fe20 | negative-memory | READ | [MP-0021 note](02_FILE_NOTES/MP-0021.md) |  |  | LOW |  |
| MP-0022 | .out-of-scope/question-limits.md | 100644/blob | 1259 | 5a3a7f677027a48a9e2a08df7c6d601b322f38da | negative-memory | READ | [MP-0022 note](02_FILE_NOTES/MP-0022.md) |  |  | LOW |  |
| MP-0023 | .out-of-scope/setup-skill-verify-mode.md | 100644/blob | 1125 | 418dba12c17b2cd77e0b3161b107c624b7b2ee97 | negative-memory | READ | [MP-0023 note](02_FILE_NOTES/MP-0023.md) |  |  | LOW |  |
| MP-0024 | AGENTS.md | 120000/blob | 9 | 681311eb9cf453d0faddf3aacaec7357e97ba8e9 | root | READ | [MP-0024 note](02_FILE_NOTES/MP-0024.md) |  |  | LOW | Git symlink blob; logical target must be reconciled separately. |
| MP-0025 | CHANGELOG.md | 100644/blob | 44408 | 26d68ffa7cf2f58471abd578042dded7b75675aa | root | READ | [MP-0025 note](02_FILE_NOTES/MP-0025.md) |  |  | LOW |  |
| MP-0026 | CLAUDE.md | 100644/blob | 3737 | 6de72d80dfdfbba9c8ce93d69a85254fdaebf2b6 | root | READ | [MP-0026 note](02_FILE_NOTES/MP-0026.md) |  |  | LOW |  |
| MP-0027 | CONTEXT.md | 100644/blob | 1768 | 76ebd23dbb8266dab9491425b39f3c4857fb4a52 | root | READ | [MP-0027 note](02_FILE_NOTES/MP-0027.md) |  |  | LOW |  |
| MP-0028 | LICENSE | 100644/blob | 1068 | f1dd2c09108dde1a5f56097cee8461b3ea834499 | root | READ | [MP-0028 note](02_FILE_NOTES/MP-0028.md) |  |  | LOW |  |
| MP-0029 | README.md | 100644/blob | 15587 | ff9b797a342d3a64b52f9f5a83d9fc4ce28709dc | root | READ | [MP-0029 note](02_FILE_NOTES/MP-0029.md) |  |  | LOW |  |
| MP-0030 | docs/engineering/ask-matt.md | 100644/blob | 10723 | 67d1e46192cc22f2f93f6d463dbd831ce174518e | human-docs | READ | [MP-0030 note](02_FILE_NOTES/MP-0030.md) |  |  | LOW |  |
| MP-0031 | docs/engineering/code-review.md | 100644/blob | 10553 | 46353162627210af65296c6dee62e422a3400373 | human-docs | READ | [MP-0031 note](02_FILE_NOTES/MP-0031.md) |  |  | LOW |  |
| MP-0032 | docs/engineering/codebase-design.md | 100644/blob | 12370 | 706365ca56fc2c5253fe407a72c494c51cb91c2e | human-docs | READ | [MP-0032 note](02_FILE_NOTES/MP-0032.md) |  |  | LOW |  |
| MP-0033 | docs/engineering/diagnosing-bugs.md | 100644/blob | 10701 | cd6887ac414d40695b52c6a121ba033cb8d5ce98 | human-docs | READ | [MP-0033 note](02_FILE_NOTES/MP-0033.md) |  |  | LOW |  |
| MP-0034 | docs/engineering/domain-modeling.md | 100644/blob | 10742 | fb8100db71dca3bb044076f537a2e6ba1ed7c3ef | human-docs | READ | [MP-0034 note](02_FILE_NOTES/MP-0034.md) |  |  | LOW |  |
| MP-0035 | docs/engineering/grill-with-docs.md | 100644/blob | 9922 | 26ac9de3bbdf49db18c7a1aa0ff508c6bf680cda | human-docs | READ | [MP-0035 note](02_FILE_NOTES/MP-0035.md) |  |  | LOW |  |
| MP-0036 | docs/engineering/implement.md | 100644/blob | 10259 | 25f9980d382ba65d1fa44fc8849412469200d626 | human-docs | READ | [MP-0036 note](02_FILE_NOTES/MP-0036.md) |  |  | LOW |  |
| MP-0037 | docs/engineering/improve-codebase-architecture.md | 100644/blob | 11814 | 076fad04c9d16903334baf8ecee8e14b47fd2d1b | human-docs | READ | [MP-0037 note](02_FILE_NOTES/MP-0037.md) |  |  | LOW |  |
| MP-0038 | docs/engineering/prototype.md | 100644/blob | 9630 | 03703cac77b4d361e7b06c9e6ef4366501c12087 | human-docs | READ | [MP-0038 note](02_FILE_NOTES/MP-0038.md) |  |  | LOW |  |
| MP-0039 | docs/engineering/research.md | 100644/blob | 9674 | a2b2074c426720af9ef50dc1cd697b3064eb8844 | human-docs | READ | [MP-0039 note](02_FILE_NOTES/MP-0039.md) |  |  | LOW |  |
| MP-0040 | docs/engineering/resolving-merge-conflicts.md | 100644/blob | 5326 | ee5e0e2db00c994a1cb5eaf4a49efdc379f93ac7 | human-docs | READ | [MP-0040 note](02_FILE_NOTES/MP-0040.md) |  |  | LOW |  |
| MP-0041 | docs/engineering/setup-matt-pocock-skills.md | 100644/blob | 9359 | d7f4933af11e6dfaf2dd307b7a69d3edb2b74dbc | human-docs | READ | [MP-0041 note](02_FILE_NOTES/MP-0041.md) |  |  | LOW |  |
| MP-0042 | docs/engineering/tdd.md | 100644/blob | 10453 | 63aae75be887420c21bad0f837c444332ec683c1 | human-docs | READ | [MP-0042 note](02_FILE_NOTES/MP-0042.md) |  |  | LOW |  |
| MP-0043 | docs/engineering/to-spec.md | 100644/blob | 8790 | e72c71c44c170114d7d83ebbda594a772f955441 | human-docs | READ | [MP-0043 note](02_FILE_NOTES/MP-0043.md) |  |  | LOW |  |
| MP-0044 | docs/engineering/to-tickets.md | 100644/blob | 10724 | 6f6f894fe0bfecd2a8b05fb1053b22da74985d90 | human-docs | READ | [MP-0044 note](02_FILE_NOTES/MP-0044.md) |  |  | LOW |  |
| MP-0045 | docs/engineering/triage.md | 100644/blob | 13140 | 10ddf79c6fbfb8c27e86f2e03998905fefa90ec1 | human-docs | READ | [MP-0045 note](02_FILE_NOTES/MP-0045.md) |  |  | LOW |  |
| MP-0046 | docs/engineering/wayfinder.md | 100644/blob | 15976 | 1efc4b18bd8a1d7733852813873474475abb3a2b | human-docs | READ | [MP-0046 note](02_FILE_NOTES/MP-0046.md) |  |  | LOW |  |
| MP-0047 | docs/engineering/wizard.md | 100644/blob | 9877 | 84e047b2481c2afe4e5247231a8600d9721f1b88 | human-docs | READ | [MP-0047 note](02_FILE_NOTES/MP-0047.md) |  |  | LOW |  |
| MP-0048 | docs/productivity/grill-me.md | 100644/blob | 6489 | d79d4864eca912ed2ed4ea3c13137c384e0868fb | human-docs | READ | [MP-0048 note](02_FILE_NOTES/MP-0048.md) |  |  | LOW |  |
| MP-0049 | docs/productivity/grilling.md | 100644/blob | 10413 | 512d76af564bc0899c59c90a5287a442f7846530 | human-docs | READ | [MP-0049 note](02_FILE_NOTES/MP-0049.md) |  |  | LOW |  |
| MP-0050 | docs/productivity/handoff.md | 100644/blob | 8746 | 72aa2f0d292a2b6f22c12ac54e9e0c9afa42f672 | human-docs | READ | [MP-0050 note](02_FILE_NOTES/MP-0050.md) |  |  | LOW |  |
| MP-0051 | docs/productivity/teach.md | 100644/blob | 13260 | 012113bd2379a4318ad3c1c7e4f4e848bbc29990 | human-docs | READ | [MP-0051 note](02_FILE_NOTES/MP-0051.md) |  |  | LOW |  |
| MP-0052 | docs/productivity/to-questionnaire.md | 100644/blob | 7828 | 52f0e437bb241630c9960f02c7e6fd7091a3030f | human-docs | READ | [MP-0052 note](02_FILE_NOTES/MP-0052.md) |  |  | LOW |  |
| MP-0053 | docs/productivity/wait-what.md | 100644/blob | 3528 | 0b14100932844507dc8b3de6e3b6bc2002d493e1 | human-docs | READ | [MP-0053 note](02_FILE_NOTES/MP-0053.md) |  |  | LOW |  |
| MP-0054 | docs/productivity/writing-for-agents.md | 100644/blob | 7784 | de12e66714721f305af1ded601f7a570c6331a72 | human-docs | READ | [MP-0054 note](02_FILE_NOTES/MP-0054.md) |  |  | LOW |  |
| MP-0055 | package-lock.json | 100644/blob | 49290 | db12f086c92da55b5d724f0dd3afecfebd2d793f | dependency-lock | READ | [MP-0055 note](02_FILE_NOTES/MP-0055.md) |  |  | HIGH |  |
| MP-0056 | package.json | 100644/blob | 597 | 2200fefca3d8c1ebac5a823681915eec736dfa07 | package-config | READ | [MP-0056 note](02_FILE_NOTES/MP-0056.md) |  |  | HIGH |  |
| MP-0057 | scripts/link-skills.sh | 100755/blob | 2240 | 558fae823c0e296ad0eff528f827142600a18135 | repo-executable | READ | [MP-0057 note](02_FILE_NOTES/MP-0057.md) |  |  | HIGH |  |
| MP-0058 | scripts/list-skills.sh | 100755/blob | 168 | f13da41774c8bffea798e64505a4c3adc528ee63 | repo-executable | READ | [MP-0058 note](02_FILE_NOTES/MP-0058.md) |  |  | HIGH |  |
| MP-0059 | scripts/sync-plugin-version.mjs | 100644/blob | 1429 | 44063fc0d14a78927caf3990882ea3809157bc21 | repo-executable | READ | [MP-0059 note](02_FILE_NOTES/MP-0059.md) |  |  | HIGH |  |
| MP-0060 | skills/deprecated/README.md | 100644/blob | 160 | aa1242c27b1f5e3f762bd5743affbd966811b5b4 | bucket-docs | READ | [MP-0060 note](02_FILE_NOTES/MP-0060.md) |  |  | LOW |  |
| MP-0061 | skills/engineering/README.md | 100644/blob | 3840 | 676977ee31f86172f4a5653ab719f6b5be3072d1 | bucket-docs | READ | [MP-0061 note](02_FILE_NOTES/MP-0061.md) |  |  | LOW |  |
| MP-0062 | skills/engineering/ask-matt/PHASE-BOUNDARIES.md | 100644/blob | 4249 | fb58ef9febcfd558cdb4517e370f19034869ba26 | skill-support | UNREAD |  |  |  | LOW |  |
| MP-0063 | skills/engineering/ask-matt/SKILL.md | 100644/blob | 11417 | ae8eb9b211972d9ae584b41d0f1439c644494fc7 | skill | UNREAD |  |  |  | MEDIUM |  |
| MP-0064 | skills/engineering/ask-matt/agents/openai.yaml | 100644/blob | 137 | 5c60d51b5b1248d7210bff8c6b42a5a06524b8a4 | codex-metadata | UNREAD |  |  |  | MEDIUM |  |
| MP-0065 | skills/engineering/code-review/SKILL.md | 100644/blob | 6589 | e28d7acbf7b3bb4d7817b7eb5d9c105af03f6ec4 | skill | UNREAD |  |  |  | MEDIUM |  |
| MP-0066 | skills/engineering/code-review/agents/openai.yaml | 100644/blob | 100 | 9076774ba327f49068db9273feceda03bfe940fa | codex-metadata | UNREAD |  |  |  | MEDIUM |  |
| MP-0067 | skills/engineering/codebase-design/DEEPENING.md | 100644/blob | 2553 | cd94075cfd754d147555c5d747a16431ed4c7dd8 | skill-support | UNREAD |  |  |  | LOW |  |
| MP-0068 | skills/engineering/codebase-design/DESIGN-IT-TWICE.md | 100644/blob | 2664 | 7edc861a31b1b219b933af18079f66b564c5de67 | skill-support | UNREAD |  |  |  | LOW |  |
| MP-0069 | skills/engineering/codebase-design/SKILL.md | 100644/blob | 6446 | 3f63c8146dd2604b419c929e9876b90c30d410e9 | skill | UNREAD |  |  |  | MEDIUM |  |
| MP-0070 | skills/engineering/codebase-design/agents/openai.yaml | 100644/blob | 102 | 3180715edb37f6e96bec42f92f00169faa8886ef | codex-metadata | UNREAD |  |  |  | MEDIUM |  |
| MP-0071 | skills/engineering/diagnosing-bugs/SKILL.md | 100644/blob | 8529 | 061c25a524acaa93d4534e9e08a793c0a5fe45fd | skill | UNREAD |  |  |  | MEDIUM |  |
| MP-0072 | skills/engineering/diagnosing-bugs/agents/openai.yaml | 100644/blob | 103 | a13a755a77634ce61a649a3a0d905a66d3865b35 | codex-metadata | UNREAD |  |  |  | MEDIUM |  |
| MP-0073 | skills/engineering/diagnosing-bugs/scripts/hitl-loop.template.sh | 100644/blob | 1316 | 243198464a8401a7ba1d63b3708fa43c3d067665 | skill-executable-config | UNREAD |  |  |  | HIGH |  |
| MP-0074 | skills/engineering/domain-modeling/ADR-FORMAT.md | 100644/blob | 2733 | d7e61f30a9fd8ca70d9ee68f019c2a9ebf2d13f7 | skill-support | UNREAD |  |  |  | LOW |  |
| MP-0075 | skills/engineering/domain-modeling/CONTEXT-FORMAT.md | 100644/blob | 2290 | 79bbb32f6fda55758b377c980f72a6cb2b8c670e | skill-support | UNREAD |  |  |  | LOW |  |
| MP-0076 | skills/engineering/domain-modeling/SKILL.md | 100644/blob | 3331 | 9b97707e19ef1f590aada356f2b3f6bb881f91be | skill | UNREAD |  |  |  | MEDIUM |  |
| MP-0077 | skills/engineering/domain-modeling/agents/openai.yaml | 100644/blob | 101 | 7f1522d2f11506ee205275ab7c282aa52366ecf6 | codex-metadata | UNREAD |  |  |  | MEDIUM |  |
| MP-0078 | skills/engineering/grill-with-docs/SKILL.md | 100644/blob | 247 | 62b9efb6f991d1b229adee7506962f13ced0c499 | skill | UNREAD |  |  |  | MEDIUM |  |
| MP-0079 | skills/engineering/grill-with-docs/agents/openai.yaml | 100644/blob | 145 | 5dbe2780a51be3e9b118bd7758a73e54a9384e11 | codex-metadata | UNREAD |  |  |  | MEDIUM |  |
| MP-0080 | skills/engineering/implement/SKILL.md | 100644/blob | 433 | 7a0b11f5f4fe9505ea5c7983c3083ba1bf754f69 | skill | UNREAD |  |  |  | MEDIUM |  |
| MP-0081 | skills/engineering/implement/agents/openai.yaml | 100644/blob | 139 | f8794dc153b409052a9167baf10858cf01b36175 | codex-metadata | UNREAD |  |  |  | MEDIUM |  |
| MP-0082 | skills/engineering/improve-codebase-architecture/HTML-REPORT.md | 100644/blob | 6641 | e39e8255b8797cf8257d014fb6658fb533f3a399 | skill-support | UNREAD |  |  |  | LOW |  |
| MP-0083 | skills/engineering/improve-codebase-architecture/SKILL.md | 100644/blob | 5993 | a578dd0a34ad0a8886abe7e7642b100106ba86d6 | skill | UNREAD |  |  |  | MEDIUM |  |
| MP-0084 | skills/engineering/improve-codebase-architecture/agents/openai.yaml | 100644/blob | 166 | 706fdca096da5937fe57875a9154017d50668c42 | codex-metadata | UNREAD |  |  |  | MEDIUM |  |
| MP-0085 | skills/engineering/prototype/LOGIC.md | 100644/blob | 6036 | 32be86a0a5d9928db84b3988e55f9debe476ab40 | skill-support | UNREAD |  |  |  | LOW |  |
| MP-0086 | skills/engineering/prototype/SKILL.md | 100644/blob | 2931 | a0044501fe0d385b4d8575b610188ede9b236ccf | skill | UNREAD |  |  |  | MEDIUM |  |
| MP-0087 | skills/engineering/prototype/UI.md | 100644/blob | 6913 | 3977951663490882c2632b40695d9f59a2fe2408 | skill-support | UNREAD |  |  |  | LOW |  |
| MP-0088 | skills/engineering/prototype/agents/openai.yaml | 100644/blob | 100 | 1618b147965bc729b7bf3e8da5f130132067aadc | codex-metadata | UNREAD |  |  |  | MEDIUM |  |
| MP-0089 | skills/engineering/research/SKILL.md | 100644/blob | 794 | fecee97e9457ba039678d2fcf1b1bc9fca78307d | skill | UNREAD |  |  |  | MEDIUM |  |
| MP-0090 | skills/engineering/research/agents/openai.yaml | 100644/blob | 94 | e18b96ca0ccc1003889d5d6991386207c2454bc2 | codex-metadata | UNREAD |  |  |  | MEDIUM |  |
| MP-0091 | skills/engineering/resolving-merge-conflicts/SKILL.md | 100644/blob | 918 | bfb7e5606e231e6808979f623fce76a9aad4b71c | skill | UNREAD |  |  |  | MEDIUM |  |
| MP-0092 | skills/engineering/resolving-merge-conflicts/agents/openai.yaml | 100644/blob | 113 | 331ffb9d38937877f51a5f867a66dc61eee259ae | codex-metadata | UNREAD |  |  |  | MEDIUM |  |
| MP-0093 | skills/engineering/setup-matt-pocock-skills/SKILL.md | 100644/blob | 6841 | 7f6f576e2e54e0d287cbb9731ebe0343f54e50cf | skill | UNREAD |  |  |  | MEDIUM |  |
| MP-0094 | skills/engineering/setup-matt-pocock-skills/agents/openai.yaml | 100644/blob | 152 | 65a0da8128c98051183235e490767a8065310868 | codex-metadata | UNREAD |  |  |  | MEDIUM |  |
| MP-0095 | skills/engineering/setup-matt-pocock-skills/domain.md | 100644/blob | 2033 | 35249041162b1eed5b873d97fc430fb3e4adb18f | skill-support | UNREAD |  |  |  | LOW |  |
| MP-0096 | skills/engineering/setup-matt-pocock-skills/issue-tracker-github.md | 100644/blob | 3731 | b258aeb3c44420a2464b72ba228b77b4b3abbaea | skill-support | UNREAD |  |  |  | LOW |  |
| MP-0097 | skills/engineering/setup-matt-pocock-skills/issue-tracker-gitlab.md | 100644/blob | 3809 | 251035a6d74b4af8d68f066b8d7f1cef90904570 | skill-support | UNREAD |  |  |  | LOW |  |
| MP-0098 | skills/engineering/setup-matt-pocock-skills/issue-tracker-local.md | 100644/blob | 1810 | 0209a19af92c9c485cf3acc3d9e253171517ea17 | skill-support | UNREAD |  |  |  | LOW |  |
| MP-0099 | skills/engineering/setup-matt-pocock-skills/triage-labels.md | 100644/blob | 1045 | b716855d485f3865f9dfde2a82141721f065b2e7 | skill-support | UNREAD |  |  |  | LOW |  |
| MP-0100 | skills/engineering/tdd/SKILL.md | 100644/blob | 3549 | 8fc086710806190ee7c4baa32089cb877a75736a | skill | UNREAD |  |  |  | MEDIUM |  |
| MP-0101 | skills/engineering/tdd/agents/openai.yaml | 100644/blob | 87 | 651b838a7663e027b1b8884491e867f26bb9a021 | codex-metadata | UNREAD |  |  |  | MEDIUM |  |
| MP-0102 | skills/engineering/tdd/mocking.md | 100644/blob | 1481 | 71cbfee674d93244ce81d1830b930ca9a69200bd | skill-support | UNREAD |  |  |  | LOW |  |
| MP-0103 | skills/engineering/tdd/tests.md | 100644/blob | 2214 | 7ab86479f925a1f9e8ba680af33cb3b12e015381 | skill-support | UNREAD |  |  |  | LOW |  |
| MP-0104 | skills/engineering/to-spec/SKILL.md | 100644/blob | 3043 | 3f52599ae2a4347aee5a07432c2707518e691a7f | skill | UNREAD |  |  |  | MEDIUM |  |
| MP-0105 | skills/engineering/to-spec/agents/openai.yaml | 100644/blob | 135 | 549e6f76f020a1b9ba65f52ccda336566ee6222a | codex-metadata | UNREAD |  |  |  | MEDIUM |  |
| MP-0106 | skills/engineering/to-tickets/SKILL.md | 100644/blob | 5671 | e868c831fcfb1e124e010bcdf84a429ec879160f | skill | UNREAD |  |  |  | MEDIUM |  |
| MP-0107 | skills/engineering/to-tickets/agents/openai.yaml | 100644/blob | 146 | 24605a5db64e4fc750b999aa94aea126bee814ee | codex-metadata | UNREAD |  |  |  | MEDIUM |  |
| MP-0108 | skills/engineering/triage/AGENT-BRIEF.md | 100644/blob | 7942 | 1462fcd9e8cc21921158c296149dc05d9be39d20 | skill-support | UNREAD |  |  |  | LOW |  |
| MP-0109 | skills/engineering/triage/OUT-OF-SCOPE.md | 100644/blob | 4667 | c9fba2f77ee0619975ec8488c0d4861a0c7e3151 | skill-support | UNREAD |  |  |  | LOW |  |
| MP-0110 | skills/engineering/triage/SKILL.md | 100644/blob | 6557 | 37ddea1e3dcf8fb5be5b92e4e45f2c34b8e61d3e | skill | UNREAD |  |  |  | MEDIUM |  |
| MP-0111 | skills/engineering/triage/agents/openai.yaml | 100644/blob | 135 | acb366cf0f2527e8925ff1223b77610ac0b1be4c | codex-metadata | UNREAD |  |  |  | MEDIUM |  |
| MP-0112 | skills/engineering/wayfinder/SKILL.md | 100644/blob | 11908 | 812805b760baf328db0ebdef6f3807e381f97016 | skill | UNREAD |  |  |  | MEDIUM |  |
| MP-0113 | skills/engineering/wayfinder/agents/openai.yaml | 100644/blob | 144 | b37544751e0570f9df8de6c02aef238de8c3e1e0 | codex-metadata | UNREAD |  |  |  | MEDIUM |  |
| MP-0114 | skills/engineering/wizard/SKILL.md | 100644/blob | 4123 | c4294ad8298b9b95fc727496b1b802b1f7363fba | skill | UNREAD |  |  |  | MEDIUM |  |
| MP-0115 | skills/engineering/wizard/agents/openai.yaml | 100644/blob | 96 | b601bdf3a321e7d32d5714681540b811287d3988 | codex-metadata | UNREAD |  |  |  | MEDIUM |  |
| MP-0116 | skills/engineering/wizard/template.sh | 100644/blob | 8567 | 1b3cdf40ad4923a9845fd682653d8cc4510f516e | skill-executable-config | UNREAD |  |  |  | HIGH |  |
| MP-0117 | skills/in-progress/README.md | 100644/blob | 2177 | ee394b7985a8c296ffa068e63e4f5dcf23b8969b | bucket-docs | UNREAD |  |  |  | LOW |  |
| MP-0118 | skills/in-progress/claude-handoff/SKILL.md | 100644/blob | 1301 | 9ab14e312a0d5cffe926eeeab12cef7dc8f84d54 | skill | UNREAD |  |  |  | MEDIUM |  |
| MP-0119 | skills/in-progress/claude-handoff/agents/openai.yaml | 100644/blob | 141 | 0a7aa5da50d0e73248fc17fb8fe82409ec071eaf | codex-metadata | UNREAD |  |  |  | MEDIUM |  |
| MP-0120 | skills/in-progress/implement-spec/SKILL.md | 100644/blob | 2043 | d5097f847fc003935599a7f7bf8f0f7186427910 | skill | UNREAD |  |  |  | MEDIUM |  |
| MP-0121 | skills/in-progress/implement-spec/agents/openai.yaml | 100644/blob | 143 | 043f27f43eed1a8a3c0e3fdbf920f07935faf05d | codex-metadata | UNREAD |  |  |  | MEDIUM |  |
| MP-0122 | skills/in-progress/loop-me/SKILL.md | 100644/blob | 2522 | e58a474ca80feffdeb28842bc3bdee37da6510e7 | skill | UNREAD |  |  |  | MEDIUM |  |
| MP-0123 | skills/in-progress/loop-me/agents/openai.yaml | 100644/blob | 140 | 1a4f4111192ff75b4771e8a248c603994d5eafdc | codex-metadata | UNREAD |  |  |  | MEDIUM |  |
| MP-0124 | skills/in-progress/retro/SKILL.md | 100644/blob | 3388 | f5fed82c7b8597a852a4fa8d292b00a1d5c8bd16 | skill | UNREAD |  |  |  | MEDIUM |  |
| MP-0125 | skills/in-progress/retro/agents/openai.yaml | 100644/blob | 146 | a2f0bac3f9cebf29beee2e79960cb876e0adc65d | codex-metadata | UNREAD |  |  |  | MEDIUM |  |
| MP-0126 | skills/in-progress/setup-ts-deep-modules/SKILL.md | 100644/blob | 7546 | 7e30047eaeda175de5d93886596a37baf365bb90 | skill | UNREAD |  |  |  | MEDIUM |  |
| MP-0127 | skills/in-progress/setup-ts-deep-modules/agents/openai.yaml | 100644/blob | 149 | 5d0581bdd4f9337cfb1e13feb7e1e18f43ea9db1 | codex-metadata | UNREAD |  |  |  | MEDIUM |  |
| MP-0128 | skills/in-progress/setup-ts-deep-modules/dependency-cruiser.config.cjs | 100644/blob | 3712 | 54030ede7d36b7f72fc0f645fa414efa9b6f63ed | skill-executable-config | UNREAD |  |  |  | HIGH |  |
| MP-0129 | skills/in-progress/writing-beats/SKILL.md | 100644/blob | 4855 | 3d3b25b605491adc5c62ae5423127717a94b9632 | skill | UNREAD |  |  |  | MEDIUM |  |
| MP-0130 | skills/in-progress/writing-beats/agents/openai.yaml | 100644/blob | 142 | e8eaa188d4c70b582eed2d1775fe4c4ea3562b25 | codex-metadata | UNREAD |  |  |  | MEDIUM |  |
| MP-0131 | skills/in-progress/writing-fragments/SKILL.md | 100644/blob | 3558 | c7c889b880cf9c8d289119dea5ff240641b615ca | skill | UNREAD |  |  |  | MEDIUM |  |
| MP-0132 | skills/in-progress/writing-fragments/agents/openai.yaml | 100644/blob | 140 | be3713e91e3ddc6c71e04e6b512b6ad6502d7cc8 | codex-metadata | UNREAD |  |  |  | MEDIUM |  |
| MP-0133 | skills/in-progress/writing-shape/SKILL.md | 100644/blob | 5922 | 02f2866d13e72504e010f2ad3458eb9b36b876db | skill | UNREAD |  |  |  | MEDIUM |  |
| MP-0134 | skills/in-progress/writing-shape/agents/openai.yaml | 100644/blob | 144 | 87e0c736be148002f9db275258cd2f405643ad7b | codex-metadata | UNREAD |  |  |  | MEDIUM |  |
| MP-0135 | skills/misc/README.md | 100644/blob | 684 | 6b169d22be12c078f1e70763d367fe693de342e2 | bucket-docs | UNREAD |  |  |  | LOW |  |
| MP-0136 | skills/misc/git-guardrails-claude-code/SKILL.md | 100644/blob | 2313 | 58bcdd875b164093b95f436fa32a65c6cb5eb572 | skill | UNREAD |  |  |  | MEDIUM |  |
| MP-0137 | skills/misc/git-guardrails-claude-code/agents/openai.yaml | 100644/blob | 112 | 3f5d756f1b9b97d94cef1473fb480ccda5fdfbc1 | codex-metadata | UNREAD |  |  |  | MEDIUM |  |
| MP-0138 | skills/misc/git-guardrails-claude-code/scripts/block-dangerous-git.sh | 100755/blob | 507 | c40b59cb47880fc9da8fe4179bd742f51f09d17d | skill-executable-config | UNREAD |  |  |  | HIGH |  |
| MP-0139 | skills/misc/migrate-to-shoehorn/SKILL.md | 100644/blob | 2795 | ae4f965e204fc93cedbc4e2c306e92829d93f800 | skill | UNREAD |  |  |  | MEDIUM |  |
| MP-0140 | skills/misc/migrate-to-shoehorn/agents/openai.yaml | 100644/blob | 110 | 3bd79ee2b502075c6d1fe40e6fe98f4fe3f3c5f5 | codex-metadata | UNREAD |  |  |  | MEDIUM |  |
| MP-0141 | skills/misc/scaffold-exercises/SKILL.md | 100644/blob | 3589 | d87df28e7d8abb4e57ecc6e47d71c274d16054c7 | skill | UNREAD |  |  |  | MEDIUM |  |
| MP-0142 | skills/misc/scaffold-exercises/agents/openai.yaml | 100644/blob | 108 | 963723a58973effa256cbfe0f23a7bcc03a374b8 | codex-metadata | UNREAD |  |  |  | MEDIUM |  |
| MP-0143 | skills/misc/setup-pre-commit/SKILL.md | 100644/blob | 2258 | 1b9708168263067adb4684d06ebb8f4ccfe9682c | skill | UNREAD |  |  |  | MEDIUM |  |
| MP-0144 | skills/misc/setup-pre-commit/agents/openai.yaml | 100644/blob | 99 | e5a1c63df9e0703893cdad799bd5e2a6b5e6939d | codex-metadata | UNREAD |  |  |  | MEDIUM |  |
| MP-0145 | skills/productivity/README.md | 100644/blob | 1480 | 0ac94ab2de3dfa98639c2cc17c12a291f4924f54 | bucket-docs | UNREAD |  |  |  | LOW |  |
| MP-0146 | skills/productivity/grill-me/SKILL.md | 100644/blob | 157 | 3947ff9c4ad980d14fc07fccbf659d47c114e81d | skill | UNREAD |  |  |  | MEDIUM |  |
| MP-0147 | skills/productivity/grill-me/agents/openai.yaml | 100644/blob | 137 | 4d6fb0c746c5d21364dce5d0cf8c51eab9712e7b | codex-metadata | UNREAD |  |  |  | MEDIUM |  |
| MP-0148 | skills/productivity/grilling/SKILL.md | 100644/blob | 1987 | 8ca78c6d8f901aab0c5a1f896034b70e666ff2a3 | skill | UNREAD |  |  |  | MEDIUM |  |
| MP-0149 | skills/productivity/grilling/agents/openai.yaml | 100644/blob | 113 | ddbdb96139c0c1dfe6bca698f39d0465674b8a39 | codex-metadata | UNREAD |  |  |  | MEDIUM |  |
| MP-0150 | skills/productivity/handoff/SKILL.md | 100644/blob | 894 | 2eb98a51b97bb5bac461a26ad14828eeac827909 | skill | UNREAD |  |  |  | MEDIUM |  |
| MP-0151 | skills/productivity/handoff/agents/openai.yaml | 100644/blob | 141 | 6e1d8da121beceddc2f9ec7fa8714c1d914dd11a | codex-metadata | UNREAD |  |  |  | MEDIUM |  |
| MP-0152 | skills/productivity/teach/GLOSSARY-FORMAT.md | 100644/blob | 2122 | fdd7e366ad9760588b28981e42b3d3b561e56aca | skill-support | UNREAD |  |  |  | LOW |  |
| MP-0153 | skills/productivity/teach/LEARNING-RECORD-FORMAT.md | 100644/blob | 2747 | 953c61422776b47612c3c945920358ad7b5daee7 | skill-support | UNREAD |  |  |  | LOW |  |
| MP-0154 | skills/productivity/teach/MISSION-FORMAT.md | 100644/blob | 1540 | 45250bb1bad70988bf381625931df64645e10246 | skill-support | UNREAD |  |  |  | LOW |  |
| MP-0155 | skills/productivity/teach/RESOURCES-FORMAT.md | 100644/blob | 1924 | 18b588c8b6f96a50ae2352f264928c643d2782e4 | skill-support | UNREAD |  |  |  | LOW |  |
| MP-0156 | skills/productivity/teach/SKILL.md | 100644/blob | 9506 | c679eeccd48ca720c8196e5d9a9e58223abf213b | skill | UNREAD |  |  |  | MEDIUM |  |
| MP-0157 | skills/productivity/teach/agents/openai.yaml | 100644/blob | 139 | 3452a850e3b0c1f0a3d41b2bfd45164d2d38d7f6 | codex-metadata | UNREAD |  |  |  | MEDIUM |  |
| MP-0158 | skills/productivity/to-questionnaire/SKILL.md | 100644/blob | 2904 | dadd0c00d6a350acaa15bb9ca1b96b20ead684ca | skill | UNREAD |  |  |  | MEDIUM |  |
| MP-0159 | skills/productivity/to-questionnaire/agents/openai.yaml | 100644/blob | 166 | a58d14765beb4acb4c9708b516310558e1308a22 | codex-metadata | UNREAD |  |  |  | MEDIUM |  |
| MP-0160 | skills/productivity/wait-what/SKILL.md | 100644/blob | 394 | f8854f1b4527bca90378baf5430557172136a1bf | skill | UNREAD |  |  |  | MEDIUM |  |
| MP-0161 | skills/productivity/wait-what/agents/openai.yaml | 100644/blob | 158 | 6f7a9c33f99ec4ba70d986d6fc0de06c8b811bc3 | codex-metadata | UNREAD |  |  |  | MEDIUM |  |
| MP-0162 | skills/productivity/writing-for-agents/SKILL-MECHANICS.md | 100644/blob | 2629 | 9cdbdb22aadc438755392216e75ad9a14cc9832e | skill-support | UNREAD |  |  |  | LOW |  |
| MP-0163 | skills/productivity/writing-for-agents/SKILL.md | 100644/blob | 10886 | a37608daf6e835e767deecfb498facecaaba82ba | skill | UNREAD |  |  |  | MEDIUM |  |
| MP-0164 | skills/productivity/writing-for-agents/agents/openai.yaml | 100644/blob | 102 | 079c933b75743dec18b5d0c01006def20b6aad26 | codex-metadata | UNREAD |  |  |  | MEDIUM |  |
