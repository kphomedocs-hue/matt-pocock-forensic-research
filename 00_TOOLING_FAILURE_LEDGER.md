# Tooling Failure & Cancellation Ledger

Repository: `kphomedocs-hue/matt-pocock-forensic-research`

Classifier version: **3**

Failed workflow runs enumerated: **132**

Cancelled workflow runs enumerated: **26**

Total incident runs: **158**

Incident entries classified: **158**

Unknown entries: **0**

Unresolved/review-required entries: **0**

## Classification summary

| Classification | Count |
|---|---:|
| CLASSIFIER_CLOSURE_GATE | 21 |
| CLASSIFIER_REFRESH_SUPERSEDED | 23 |
| CLASSIFIER_SCHEMA_TRANSITION | 1 |
| CROSS_WORKFLOW_CONCURRENCY_CANCEL | 3 |
| FOUNDATION_GATE | 1 |
| FOUNDATION_PROVENANCE_GATE | 1 |
| FOUNDATION_REGISTER_GATE | 3 |
| INFRA_SETUP | 1 |
| PHASE3_HISTORY_BLOB_SHA_PARSER_SCOPE | 1 |
| PHASE3_HISTORY_DEFINITION_RECONCILIATION | 4 |
| PHASE3_HISTORY_EVENT_COUNT_TRANSITION | 2 |
| PHASE3_HISTORY_EXACT_EVIDENCE_GATE | 2 |
| PHASE3_HISTORY_LEDGER_PARSER_SCOPE | 1 |
| PHASE3_HISTORY_PARITY_PARSER_SCOPE | 1 |
| PHASE3_PROMOTION_PROVENANCE_PARSER | 1 |
| PHASE3_QUALITY_RECHECK_GATE | 1 |
| PHASE4_ARCHITECTURE_REPORT_BOOTSTRAP_MISSING_SCRIPT | 1 |
| PHASE4_ARCHITECTURE_REPORT_CONNECTOR_ESCAPE_TRANSITION | 3 |
| PHASE4_BATCH_BOOTSTRAP_TRIGGER | 1 |
| PHASE4_CT019_ROW_ANCHOR_TRANSITION | 2 |
| PHASE4_DEEP_MODULE_HARNESS_BOOTSTRAP_TRANSITION | 1 |
| PHASE4_DEEP_MODULE_TYPESCRIPT_COMPATIBILITY_TRANSITION | 1 |
| PHASE4_PRECOMMIT_EXECUTABLE_PREDICATE_DISCOVERY | 1 |
| PHASE4_RUNTIME_ACCEPTANCE_SCHEMA_TRANSITION | 1 |
| PHASE4_RUNTIME_PROVENANCE_ID_TYPE_TRANSITION | 1 |
| PHASE4_RUNTIME_PROVENANCE_WIRING_TRANSITION | 1 |
| PHASE4_STATUS_CHECKPOINT_BOOTSTRAP_TRANSITION | 1 |
| PHASE4_STATUS_STALE_GUARD_TRANSITION | 3 |
| PUSH_RACE | 63 |
| STATUS_PARSER | 10 |
| TOOLING_CLASSIFIER_BACKLOG_CLOSURE | 1 |

## Impact summary

| Impact | Count |
|---|---:|
| DELAYED_PROMOTION | 10 |
| DETECTED_AND_BLOCKED | 26 |
| DETECTED_AND_BLOCKED_FIXED | 18 |
| DISCARDED_EXECUTION_FIXED | 3 |
| FIXED_CONFIGURATION_MISMATCH | 3 |
| NO_DATA_CHANGE_FIXED | 1 |
| NO_RESEARCH_DATA_CHANGE_FIXED | 10 |
| REDUNDANT_REFRESH_DISCARDED | 23 |
| TEMPORARILY_STALE | 63 |
| TRANSIENT_OR_INFRA | 1 |

## Incident ledger

| Run | Conclusion | Date | Workflow | Failed step | Classification | Impact |
|---:|---|---|---|---|---|---|
| 34692928795 | failure | 2026-09-12T12:10:02Z | Rebuild master ledger | Commit regenerated ledger | PUSH_RACE | TEMPORARILY_STALE |
| 34693043883 | failure | 2026-09-12T12:12:28Z | Rebuild master ledger | Commit regenerated ledger | PUSH_RACE | TEMPORARILY_STALE |
| 34693302869 | failure | 2026-09-12T12:18:10Z | Rebuild master ledger | Rebuild frozen census and ledger | STATUS_PARSER | DELAYED_PROMOTION |
| 34693309553 | failure | 2026-09-12T12:18:19Z | Rebuild master ledger | Rebuild frozen census and ledger | STATUS_PARSER | DELAYED_PROMOTION |
| 34693318265 | failure | 2026-09-12T12:18:33Z | Rebuild master ledger | Rebuild frozen census and ledger | STATUS_PARSER | DELAYED_PROMOTION |
| 34693323918 | failure | 2026-09-12T12:18:42Z | Rebuild master ledger | Rebuild frozen census and ledger | STATUS_PARSER | DELAYED_PROMOTION |
| 34693365777 | failure | 2026-09-12T12:19:41Z | Rebuild master ledger | Rebuild frozen census and ledger | STATUS_PARSER | DELAYED_PROMOTION |
| 34693423298 | failure | 2026-09-12T12:20:55Z | Rebuild master ledger | Rebuild frozen census and ledger | STATUS_PARSER | DELAYED_PROMOTION |
| 34693430325 | failure | 2026-09-12T12:21:04Z | Rebuild master ledger | Rebuild frozen census and ledger | STATUS_PARSER | DELAYED_PROMOTION |
| 34693436433 | failure | 2026-09-12T12:21:12Z | Rebuild master ledger | Rebuild frozen census and ledger | STATUS_PARSER | DELAYED_PROMOTION |
| 34693445380 | failure | 2026-09-12T12:21:24Z | Rebuild master ledger | Rebuild frozen census and ledger | STATUS_PARSER | DELAYED_PROMOTION |
| 34693481028 | failure | 2026-09-12T12:22:10Z | Rebuild master ledger | Rebuild frozen census and ledger | STATUS_PARSER | DELAYED_PROMOTION |
| 34699083747 | failure | 2026-09-12T14:22:11Z | Rebuild master ledger | Commit regenerated ledger | PUSH_RACE | TEMPORARILY_STALE |
| 34699181638 | failure | 2026-09-12T14:24:16Z | Rebuild master ledger | Commit regenerated ledger | PUSH_RACE | TEMPORARILY_STALE |
| 34699195524 | failure | 2026-09-12T14:24:34Z | Rebuild master ledger | Commit regenerated ledger | PUSH_RACE | TEMPORARILY_STALE |
| 34701078379 | failure | 2026-09-12T15:03:33Z | Rebuild master ledger | Commit regenerated ledger | PUSH_RACE | TEMPORARILY_STALE |
| 34701148658 | failure | 2026-09-12T15:04:59Z | Rebuild master ledger | Commit regenerated ledger | PUSH_RACE | TEMPORARILY_STALE |
| 34706367588 | failure | 2026-09-12T16:48:51Z | Rebuild master ledger | Commit regenerated ledger | PUSH_RACE | TEMPORARILY_STALE |
| 34706373829 | failure | 2026-09-12T16:48:58Z | Rebuild master ledger | Commit regenerated ledger | PUSH_RACE | TEMPORARILY_STALE |
| 34706391442 | failure | 2026-09-12T16:49:19Z | Rebuild master ledger | Commit regenerated ledger | PUSH_RACE | TEMPORARILY_STALE |
| 34706429708 | failure | 2026-09-12T16:50:06Z | Rebuild master ledger | Commit regenerated ledger | PUSH_RACE | TEMPORARILY_STALE |
| 34706458293 | failure | 2026-09-12T16:50:41Z | Rebuild master ledger | Commit regenerated ledger | PUSH_RACE | TEMPORARILY_STALE |
| 34706986936 | failure | 2026-09-12T17:01:41Z | Rebuild master ledger | Commit regenerated ledger | PUSH_RACE | TEMPORARILY_STALE |
| 34706991986 | failure | 2026-09-12T17:01:47Z | Rebuild master ledger | Commit regenerated ledger | PUSH_RACE | TEMPORARILY_STALE |
| 34706997261 | failure | 2026-09-12T17:01:54Z | Rebuild master ledger | Commit regenerated ledger | PUSH_RACE | TEMPORARILY_STALE |
| 34707052602 | failure | 2026-09-12T17:02:59Z | Rebuild master ledger | Commit regenerated ledger | PUSH_RACE | TEMPORARILY_STALE |
| 34707066433 | failure | 2026-09-12T17:03:14Z | Rebuild master ledger | Commit regenerated ledger | PUSH_RACE | TEMPORARILY_STALE |
| 34707080152 | failure | 2026-09-12T17:03:30Z | Rebuild master ledger | Commit regenerated ledger | PUSH_RACE | TEMPORARILY_STALE |
| 34707713735 | failure | 2026-09-12T17:16:04Z | Rebuild master ledger | Commit regenerated ledger | PUSH_RACE | TEMPORARILY_STALE |
| 34707737518 | failure | 2026-09-12T17:16:33Z | Rebuild master ledger | Commit regenerated ledger | PUSH_RACE | TEMPORARILY_STALE |
| 34707744102 | failure | 2026-09-12T17:16:41Z | Rebuild master ledger | Commit regenerated ledger | PUSH_RACE | TEMPORARILY_STALE |
| 34707750888 | failure | 2026-09-12T17:16:48Z | Rebuild master ledger | Commit regenerated ledger | PUSH_RACE | TEMPORARILY_STALE |
| 34707805308 | failure | 2026-09-12T17:17:53Z | Rebuild master ledger | Commit regenerated ledger | PUSH_RACE | TEMPORARILY_STALE |
| 34707811404 | failure | 2026-09-12T17:18:00Z | Rebuild master ledger | Commit regenerated ledger | PUSH_RACE | TEMPORARILY_STALE |
| 34707878140 | failure | 2026-09-12T17:19:23Z | Rebuild master ledger | Commit regenerated ledger | PUSH_RACE | TEMPORARILY_STALE |
| 34707885096 | failure | 2026-09-12T17:19:31Z | Rebuild master ledger | Commit regenerated ledger | PUSH_RACE | TEMPORARILY_STALE |
| 34707909234 | failure | 2026-09-12T17:19:57Z | Rebuild master ledger | Commit regenerated ledger | PUSH_RACE | TEMPORARILY_STALE |
| 34707966134 | failure | 2026-09-12T17:21:03Z | Rebuild master ledger | Commit regenerated ledger | PUSH_RACE | TEMPORARILY_STALE |
| 34707972228 | failure | 2026-09-12T17:21:11Z | Rebuild master ledger | Commit regenerated ledger | PUSH_RACE | TEMPORARILY_STALE |
| 34707978527 | failure | 2026-09-12T17:21:20Z | Rebuild master ledger | Commit regenerated ledger | PUSH_RACE | TEMPORARILY_STALE |
| 34707989589 | failure | 2026-09-12T17:21:34Z | Rebuild master ledger | Commit regenerated ledger | PUSH_RACE | TEMPORARILY_STALE |
| 34708206640 | failure | 2026-09-12T17:25:55Z | Rebuild master ledger | Commit regenerated ledger | PUSH_RACE | TEMPORARILY_STALE |
| 34708262250 | failure | 2026-09-12T17:27:07Z | Rebuild master ledger | Commit regenerated ledger | PUSH_RACE | TEMPORARILY_STALE |
| 34708326236 | failure | 2026-09-12T17:28:28Z | Rebuild master ledger | Commit regenerated ledger | PUSH_RACE | TEMPORARILY_STALE |
| 34708346671 | failure | 2026-09-12T17:28:53Z | Rebuild master ledger | Commit regenerated ledger | PUSH_RACE | TEMPORARILY_STALE |
| 34708396654 | failure | 2026-09-12T17:29:57Z | Rebuild master ledger | Commit regenerated ledger | PUSH_RACE | TEMPORARILY_STALE |
| 34708412632 | failure | 2026-09-12T17:30:15Z | Rebuild master ledger | Commit regenerated ledger | PUSH_RACE | TEMPORARILY_STALE |
| 34708419908 | failure | 2026-09-12T17:30:23Z | Rebuild master ledger | Commit regenerated ledger | PUSH_RACE | TEMPORARILY_STALE |
| 34708427721 | failure | 2026-09-12T17:30:29Z | Rebuild master ledger | Commit regenerated ledger | PUSH_RACE | TEMPORARILY_STALE |
| 34708498021 | failure | 2026-09-12T17:31:50Z | Rebuild master ledger | Commit regenerated ledger | PUSH_RACE | TEMPORARILY_STALE |
| 34708504540 | failure | 2026-09-12T17:31:58Z | Rebuild master ledger | Commit regenerated ledger | PUSH_RACE | TEMPORARILY_STALE |
| 34708512247 | failure | 2026-09-12T17:32:06Z | Rebuild master ledger | Commit regenerated ledger | PUSH_RACE | TEMPORARILY_STALE |
| 34708531576 | failure | 2026-09-12T17:32:29Z | Rebuild master ledger | Commit regenerated ledger | PUSH_RACE | TEMPORARILY_STALE |
| 34708537655 | failure | 2026-09-12T17:32:36Z | Rebuild master ledger | Commit regenerated ledger | PUSH_RACE | TEMPORARILY_STALE |
| 34708543731 | failure | 2026-09-12T17:32:44Z | Rebuild master ledger | Commit regenerated ledger | PUSH_RACE | TEMPORARILY_STALE |
| 34708550632 | failure | 2026-09-12T17:32:53Z | Rebuild master ledger | Commit regenerated ledger | PUSH_RACE | TEMPORARILY_STALE |
| 34708659267 | failure | 2026-09-12T17:35:04Z | Rebuild master ledger | Commit regenerated ledger | PUSH_RACE | TEMPORARILY_STALE |
| 34708666970 | failure | 2026-09-12T17:35:11Z | Rebuild master ledger | Commit regenerated ledger | PUSH_RACE | TEMPORARILY_STALE |
| 34708674341 | failure | 2026-09-12T17:35:18Z | Rebuild master ledger | Commit regenerated ledger | PUSH_RACE | TEMPORARILY_STALE |
| 34708681772 | failure | 2026-09-12T17:35:27Z | Rebuild master ledger | Commit regenerated ledger | PUSH_RACE | TEMPORARILY_STALE |
| 34708686926 | failure | 2026-09-12T17:35:34Z | Rebuild master ledger | Commit regenerated ledger | PUSH_RACE | TEMPORARILY_STALE |
| 34708692023 | failure | 2026-09-12T17:35:41Z | Rebuild master ledger | Commit regenerated ledger | PUSH_RACE | TEMPORARILY_STALE |
| 34708711893 | failure | 2026-09-12T17:36:04Z | Rebuild master ledger | Commit regenerated ledger | PUSH_RACE | TEMPORARILY_STALE |
| 34708726530 | failure | 2026-09-12T17:36:19Z | Rebuild master ledger | Commit regenerated ledger | PUSH_RACE | TEMPORARILY_STALE |
| 34708732780 | failure | 2026-09-12T17:36:27Z | Rebuild master ledger | Commit regenerated ledger | PUSH_RACE | TEMPORARILY_STALE |
| 34708739085 | failure | 2026-09-12T17:36:36Z | Rebuild master ledger | Commit regenerated ledger | PUSH_RACE | TEMPORARILY_STALE |
| 34708751006 | failure | 2026-09-12T17:36:52Z | Rebuild master ledger | Commit regenerated ledger | PUSH_RACE | TEMPORARILY_STALE |
| 34708756800 | failure | 2026-09-12T17:36:59Z | Rebuild master ledger | Commit regenerated ledger | PUSH_RACE | TEMPORARILY_STALE |
| 34708763471 | failure | 2026-09-12T17:37:06Z | Rebuild master ledger | Commit regenerated ledger | PUSH_RACE | TEMPORARILY_STALE |
| 34708771788 | failure | 2026-09-12T17:37:14Z | Rebuild master ledger | Commit regenerated ledger | PUSH_RACE | TEMPORARILY_STALE |
| 34708792909 | failure | 2026-09-12T17:37:42Z | Rebuild master ledger | Commit regenerated ledger | PUSH_RACE | TEMPORARILY_STALE |
| 34712074395 | failure | 2026-09-12T18:43:47Z | Validate forensic foundation | Validate foundation | FOUNDATION_GATE | DETECTED_AND_BLOCKED |
| 34712105550 | failure | 2026-09-12T18:44:26Z | Validate forensic foundation | Enforce hard-integrity gate | FOUNDATION_PROVENANCE_GATE | DETECTED_AND_BLOCKED |
| 34712169805 | failure | 2026-09-12T18:45:44Z | Validate forensic foundation | Enforce hard-integrity gate | FOUNDATION_REGISTER_GATE | DETECTED_AND_BLOCKED |
| 34712284713 | failure | 2026-09-12T18:48:06Z | Validate forensic foundation | Enforce hard-integrity gate | FOUNDATION_REGISTER_GATE | DETECTED_AND_BLOCKED |
| 34712298868 | failure | 2026-09-12T18:48:24Z | Validate forensic foundation | Enforce hard-integrity gate | FOUNDATION_REGISTER_GATE | DETECTED_AND_BLOCKED |
| 34712776661 | cancelled | 2026-09-12T18:58:29Z | Rebuild connection graph |  | CROSS_WORKFLOW_CONCURRENCY_CANCEL | DISCARDED_EXECUTION_FIXED |
| 34712784616 | cancelled | 2026-09-12T18:58:40Z | Validate forensic foundation |  | CROSS_WORKFLOW_CONCURRENCY_CANCEL | DISCARDED_EXECUTION_FIXED |
| 34712786090 | cancelled | 2026-09-12T18:58:42Z | Classify tooling failures |  | CLASSIFIER_REFRESH_SUPERSEDED | REDUNDANT_REFRESH_DISCARDED |
| 34712787814 | cancelled | 2026-09-12T18:58:45Z | Classify tooling failures |  | CLASSIFIER_REFRESH_SUPERSEDED | REDUNDANT_REFRESH_DISCARDED |
| 34712792316 | cancelled | 2026-09-12T18:58:51Z | Normalize note metadata |  | CROSS_WORKFLOW_CONCURRENCY_CANCEL | DISCARDED_EXECUTION_FIXED |
| 34712806058 | cancelled | 2026-09-12T18:59:08Z | Classify tooling failures |  | CLASSIFIER_REFRESH_SUPERSEDED | REDUNDANT_REFRESH_DISCARDED |
| 34712998533 | cancelled | 2026-09-12T19:02:52Z | Classify tooling failures |  | CLASSIFIER_REFRESH_SUPERSEDED | REDUNDANT_REFRESH_DISCARDED |
| 34713138258 | failure | 2026-09-12T19:05:40Z | Classify tooling failures | Validate failure ledger outputs | CLASSIFIER_SCHEMA_TRANSITION | FIXED_CONFIGURATION_MISMATCH |
| 34713153565 | failure | 2026-09-12T19:06:00Z | Classify tooling failures | Validate tooling incident ledger outputs | CLASSIFIER_CLOSURE_GATE | DETECTED_AND_BLOCKED |
| 34738911437 | failure | 2026-09-13T04:52:20Z | Promote Phase 3 connections | Promote notes with per-file Phase 3 evidence | PHASE3_PROMOTION_PROVENANCE_PARSER | DETECTED_AND_BLOCKED_FIXED |
| 34740170053 | failure | 2026-09-13T05:23:12Z | Validate Phase 3 quality | Enforce Phase 3 quality gate | PHASE3_QUALITY_RECHECK_GATE | DETECTED_AND_BLOCKED_FIXED |
| 34740488271 | failure | 2026-09-13T05:30:57Z | Classify tooling failures | Validate tooling incident ledger outputs | CLASSIFIER_CLOSURE_GATE | DETECTED_AND_BLOCKED |
| 34740614575 | failure | 2026-09-13T05:34:01Z | Classify tooling failures | Validate tooling incident ledger outputs | CLASSIFIER_CLOSURE_GATE | DETECTED_AND_BLOCKED |
| 34745903691 | failure | 2026-09-13T07:42:42Z | Apply Phase 4 batch | Apply pending Phase 4 batch | PHASE4_BATCH_BOOTSTRAP_TRIGGER | NO_DATA_CHANGE_FIXED |
| 34750032928 | failure | 2026-09-13T09:41:47Z | Rebuild Phase 3 state | Rebuild ordered Phase 3 state | PHASE3_HISTORY_EVENT_COUNT_TRANSITION | DETECTED_AND_BLOCKED_FIXED |
| 34750032982 | failure | 2026-09-13T09:41:47Z | Validate Phase 3 quality | Enforce Phase 3 quality gate | PHASE3_HISTORY_DEFINITION_RECONCILIATION | DETECTED_AND_BLOCKED_FIXED |
| 34750058890 | failure | 2026-09-13T09:42:27Z | Classify tooling failures | Validate tooling incident ledger outputs | CLASSIFIER_CLOSURE_GATE | DETECTED_AND_BLOCKED |
| 34750079498 | failure | 2026-09-13T09:43:00Z | Classify tooling failures | Validate tooling incident ledger outputs | CLASSIFIER_CLOSURE_GATE | DETECTED_AND_BLOCKED |
| 34752972889 | failure | 2026-09-13T10:52:25Z | Phase 4 local runtime checks | Enforce runtime-evidence acceptance gate | PHASE4_RUNTIME_ACCEPTANCE_SCHEMA_TRANSITION | NO_RESEARCH_DATA_CHANGE_FIXED |
| 34753069061 | failure | 2026-09-13T10:54:48Z | Classify tooling failures | Validate tooling incident ledger outputs | CLASSIFIER_CLOSURE_GATE | DETECTED_AND_BLOCKED |
| 34753078094 | cancelled | 2026-09-13T10:55:00Z | Classify tooling failures |  | CLASSIFIER_REFRESH_SUPERSEDED | REDUNDANT_REFRESH_DISCARDED |
| 34753085869 | failure | 2026-09-13T10:55:10Z | Validate Phase 3 quality | Enforce Phase 3 quality gate | PHASE3_HISTORY_DEFINITION_RECONCILIATION | DETECTED_AND_BLOCKED_FIXED |
| 34753085943 | failure | 2026-09-13T10:55:10Z | Rebuild Phase 3 state | Rebuild ordered Phase 3 state | PHASE3_HISTORY_EVENT_COUNT_TRANSITION | DETECTED_AND_BLOCKED_FIXED |
| 34753122920 | failure | 2026-09-13T10:56:04Z | Classify tooling failures | Validate tooling incident ledger outputs | CLASSIFIER_CLOSURE_GATE | DETECTED_AND_BLOCKED |
| 34753128364 | failure | 2026-09-13T10:56:13Z | Classify tooling failures | Validate tooling incident ledger outputs | CLASSIFIER_CLOSURE_GATE | DETECTED_AND_BLOCKED |
| 34753173840 | failure | 2026-09-13T10:57:19Z | Rebuild Phase 3 state | Rebuild ordered Phase 3 state | PHASE3_HISTORY_EXACT_EVIDENCE_GATE | DETECTED_AND_BLOCKED_FIXED |
| 34753173848 | failure | 2026-09-13T10:57:19Z | Validate Phase 3 quality | Enforce Phase 3 quality gate | PHASE3_HISTORY_DEFINITION_RECONCILIATION | DETECTED_AND_BLOCKED_FIXED |
| 34753181972 | cancelled | 2026-09-13T10:57:32Z | Classify tooling failures |  | CLASSIFIER_REFRESH_SUPERSEDED | REDUNDANT_REFRESH_DISCARDED |
| 34753197749 | failure | 2026-09-13T10:57:57Z | Classify tooling failures | Validate tooling incident ledger outputs | CLASSIFIER_CLOSURE_GATE | DETECTED_AND_BLOCKED |
| 34753231819 | failure | 2026-09-13T10:58:49Z | Classify tooling failures | Validate tooling incident ledger outputs | CLASSIFIER_CLOSURE_GATE | DETECTED_AND_BLOCKED |
| 34753493374 | failure | 2026-09-13T11:04:42Z | Validate Phase 3 quality | Enforce Phase 3 quality gate | PHASE3_HISTORY_DEFINITION_RECONCILIATION | DETECTED_AND_BLOCKED_FIXED |
| 34753493482 | failure | 2026-09-13T11:04:42Z | Rebuild Phase 3 state | Rebuild ordered Phase 3 state | PHASE3_HISTORY_EXACT_EVIDENCE_GATE | DETECTED_AND_BLOCKED_FIXED |
| 34753534524 | failure | 2026-09-13T11:05:34Z | Classify tooling failures | Validate tooling incident ledger outputs | CLASSIFIER_CLOSURE_GATE | DETECTED_AND_BLOCKED |
| 34753536022 | cancelled | 2026-09-13T11:05:36Z | Classify tooling failures |  | CLASSIFIER_REFRESH_SUPERSEDED | REDUNDANT_REFRESH_DISCARDED |
| 34753546267 | failure | 2026-09-13T11:05:53Z | Classify tooling failures | Validate tooling incident ledger outputs | CLASSIFIER_CLOSURE_GATE | DETECTED_AND_BLOCKED |
| 34849974317 | failure | 2026-09-14T13:33:29Z | Repair Phase 4 recheck findings | Regenerate and validate Phase 4 state | PHASE4_RUNTIME_PROVENANCE_ID_TYPE_TRANSITION | FIXED_CONFIGURATION_MISMATCH |
| 34850175820 | failure | 2026-09-14T13:35:26Z | Repair Phase 4 recheck findings | Verify repaired invariants | PHASE4_RUNTIME_PROVENANCE_WIRING_TRANSITION | FIXED_CONFIGURATION_MISMATCH |
| 34850257070 | failure | 2026-09-14T13:36:11Z | Repair Phase 4 recheck findings | Commit repaired Phase 4 control layer | PUSH_RACE | TEMPORARILY_STALE |
| 34850571686 | failure | 2026-09-14T13:39:16Z | Phase 4 runtime smoke | Reproduce and adjudicate CT-019 | PHASE4_CT019_ROW_ANCHOR_TRANSITION | NO_RESEARCH_DATA_CHANGE_FIXED |
| 34850593696 | failure | 2026-09-14T13:39:29Z | Classify tooling failures | Validate tooling incident ledger outputs | CLASSIFIER_CLOSURE_GATE | DETECTED_AND_BLOCKED |
| 34851582989 | failure | 2026-09-14T13:48:55Z | Phase 4 runtime smoke | Reproduce and adjudicate CT-019 | PHASE4_CT019_ROW_ANCHOR_TRANSITION | NO_RESEARCH_DATA_CHANGE_FIXED |
| 34851605530 | failure | 2026-09-14T13:49:08Z | Classify tooling failures | Validate tooling incident ledger outputs | CLASSIFIER_CLOSURE_GATE | DETECTED_AND_BLOCKED |
| 34860744756 | failure | 2026-09-14T15:13:28Z | Classify tooling failures | Validate tooling incident ledger outputs | CLASSIFIER_CLOSURE_GATE | DETECTED_AND_BLOCKED |
| 34867570179 | failure | 2026-09-14T16:16:31Z | Phase 4 deep-module runtime | Run isolated deep-module runtime harness | PHASE4_DEEP_MODULE_HARNESS_BOOTSTRAP_TRANSITION | NO_RESEARCH_DATA_CHANGE_FIXED |
| 34867918904 | failure | 2026-09-14T16:19:51Z | Phase 4 deep-module runtime | Run isolated deep-module runtime harness | PHASE4_DEEP_MODULE_TYPESCRIPT_COMPATIBILITY_TRANSITION | NO_RESEARCH_DATA_CHANGE_FIXED |
| 34868912572 | failure | 2026-09-14T16:29:17Z | Phase 4 setup-pre-commit runtime | Run isolated setup-pre-commit runtime harness | PHASE4_PRECOMMIT_EXECUTABLE_PREDICATE_DISCOVERY | DETECTED_AND_BLOCKED_FIXED |
| 34869764952 | failure | 2026-09-14T16:37:28Z | Classify tooling failures | Validate tooling incident ledger outputs | CLASSIFIER_CLOSURE_GATE | DETECTED_AND_BLOCKED |
| 34925863951 | cancelled | 2026-09-15T03:40:10Z | Classify tooling failures |  | CLASSIFIER_REFRESH_SUPERSEDED | REDUNDANT_REFRESH_DISCARDED |
| 34925899850 | cancelled | 2026-09-15T03:40:42Z | Classify tooling failures |  | CLASSIFIER_REFRESH_SUPERSEDED | REDUNDANT_REFRESH_DISCARDED |
| 34925982246 | failure | 2026-09-15T03:42:03Z | Phase 4 main guard | Ensure validators are non-mutating on committed main | PHASE4_STATUS_CHECKPOINT_BOOTSTRAP_TRANSITION | NO_RESEARCH_DATA_CHANGE_FIXED |
| 34926001960 | failure | 2026-09-15T03:42:21Z | Classify tooling failures | Validate tooling incident ledger outputs | CLASSIFIER_CLOSURE_GATE | DETECTED_AND_BLOCKED |
| 34926294022 | failure | 2026-09-15T03:46:56Z | Phase 4 main guard | Ensure validators are non-mutating on committed main | PHASE4_STATUS_STALE_GUARD_TRANSITION | DETECTED_AND_BLOCKED_FIXED |
| 34926305041 | cancelled | 2026-09-15T03:47:08Z | Classify tooling failures |  | CLASSIFIER_REFRESH_SUPERSEDED | REDUNDANT_REFRESH_DISCARDED |
| 34926308847 | failure | 2026-09-15T03:47:12Z | Phase 4 main guard | Ensure validators are non-mutating on committed main | PHASE4_STATUS_STALE_GUARD_TRANSITION | DETECTED_AND_BLOCKED_FIXED |
| 34926322371 | cancelled | 2026-09-15T03:47:25Z | Classify tooling failures |  | CLASSIFIER_REFRESH_SUPERSEDED | REDUNDANT_REFRESH_DISCARDED |
| 34926329873 | failure | 2026-09-15T03:47:32Z | Phase 4 main guard | Ensure validators are non-mutating on committed main | PHASE4_STATUS_STALE_GUARD_TRANSITION | DETECTED_AND_BLOCKED_FIXED |
| 34926343682 | cancelled | 2026-09-15T03:47:46Z | Classify tooling failures |  | CLASSIFIER_REFRESH_SUPERSEDED | REDUNDANT_REFRESH_DISCARDED |
| 34926348208 | cancelled | 2026-09-15T03:47:50Z | Classify tooling failures |  | CLASSIFIER_REFRESH_SUPERSEDED | REDUNDANT_REFRESH_DISCARDED |
| 34926367647 | cancelled | 2026-09-15T03:48:10Z | Classify tooling failures |  | CLASSIFIER_REFRESH_SUPERSEDED | REDUNDANT_REFRESH_DISCARDED |
| 34926376206 | cancelled | 2026-09-15T03:48:18Z | Classify tooling failures |  | CLASSIFIER_REFRESH_SUPERSEDED | REDUNDANT_REFRESH_DISCARDED |
| 34926377311 | cancelled | 2026-09-15T03:48:19Z | Classify tooling failures |  | CLASSIFIER_REFRESH_SUPERSEDED | REDUNDANT_REFRESH_DISCARDED |
| 34926378445 | failure | 2026-09-15T03:48:21Z | Phase 4 setup-pre-commit runtime | Set up job | INFRA_SETUP | TRANSIENT_OR_INFRA |
| 34926386173 | cancelled | 2026-09-15T03:48:28Z | Classify tooling failures |  | CLASSIFIER_REFRESH_SUPERSEDED | REDUNDANT_REFRESH_DISCARDED |
| 34926387059 | failure | 2026-09-15T03:48:29Z | Classify tooling failures | Validate tooling incident ledger outputs | CLASSIFIER_CLOSURE_GATE | DETECTED_AND_BLOCKED |
| 34926393025 | cancelled | 2026-09-15T03:48:35Z | Classify tooling failures |  | CLASSIFIER_REFRESH_SUPERSEDED | REDUNDANT_REFRESH_DISCARDED |
| 34926416696 | cancelled | 2026-09-15T03:48:58Z | Classify tooling failures |  | CLASSIFIER_REFRESH_SUPERSEDED | REDUNDANT_REFRESH_DISCARDED |
| 34926418210 | cancelled | 2026-09-15T03:48:59Z | Classify tooling failures |  | CLASSIFIER_REFRESH_SUPERSEDED | REDUNDANT_REFRESH_DISCARDED |
| 34926431919 | cancelled | 2026-09-15T03:49:13Z | Classify tooling failures |  | CLASSIFIER_REFRESH_SUPERSEDED | REDUNDANT_REFRESH_DISCARDED |
| 34928147482 | failure | 2026-09-15T04:15:45Z | Phase 4 architecture-report runtime | Run isolated offline dependency harness | PHASE4_ARCHITECTURE_REPORT_BOOTSTRAP_MISSING_SCRIPT | NO_RESEARCH_DATA_CHANGE_FIXED |
| 34928190384 | failure | 2026-09-15T04:16:24Z | Phase 4 architecture-report runtime | Run isolated offline dependency harness | PHASE4_ARCHITECTURE_REPORT_CONNECTOR_ESCAPE_TRANSITION | NO_RESEARCH_DATA_CHANGE_FIXED |
| 34928232337 | failure | 2026-09-15T04:17:03Z | Phase 4 architecture-report runtime | Run isolated offline dependency harness | PHASE4_ARCHITECTURE_REPORT_CONNECTOR_ESCAPE_TRANSITION | NO_RESEARCH_DATA_CHANGE_FIXED |
| 34928290191 | failure | 2026-09-15T04:17:59Z | Phase 4 architecture-report runtime | Run isolated offline dependency harness | PHASE4_ARCHITECTURE_REPORT_CONNECTOR_ESCAPE_TRANSITION | NO_RESEARCH_DATA_CHANGE_FIXED |
| 34928459181 | failure | 2026-09-15T04:20:39Z | Classify tooling failures | Validate tooling incident ledger outputs | TOOLING_CLASSIFIER_BACKLOG_CLOSURE | DETECTED_AND_BLOCKED_FIXED |
| 34929956423 | failure | 2026-09-15T04:44:00Z | Phase 4 architecture-report runtime | Commit runtime evidence atomically | PUSH_RACE | TEMPORARILY_STALE |
| 35127421564 | failure | 2026-09-16T17:19:02Z | Rebuild Phase 3 state | Rebuild ordered Phase 3 state | PHASE3_HISTORY_LEDGER_PARSER_SCOPE | DETECTED_AND_BLOCKED_FIXED |
| 35127543108 | failure | 2026-09-16T17:20:13Z | Classify tooling failures | Validate tooling incident ledger outputs | CLASSIFIER_CLOSURE_GATE | DETECTED_AND_BLOCKED |
| 35128886485 | failure | 2026-09-16T17:33:06Z | Rebuild Phase 3 state | Rebuild ordered Phase 3 state | PHASE3_HISTORY_BLOB_SHA_PARSER_SCOPE | DETECTED_AND_BLOCKED_FIXED |
| 35128905967 | cancelled | 2026-09-16T17:33:17Z | Classify tooling failures |  | CLASSIFIER_REFRESH_SUPERSEDED | REDUNDANT_REFRESH_DISCARDED |
| 35129044168 | failure | 2026-09-16T17:34:38Z | Classify tooling failures | Validate tooling incident ledger outputs | CLASSIFIER_CLOSURE_GATE | DETECTED_AND_BLOCKED |
| 35129364551 | failure | 2026-09-16T17:37:43Z | Rebuild Phase 3 state | Rebuild ordered Phase 3 state | PHASE3_HISTORY_PARITY_PARSER_SCOPE | DETECTED_AND_BLOCKED_FIXED |
| 35129383713 | cancelled | 2026-09-16T17:37:54Z | Classify tooling failures |  | CLASSIFIER_REFRESH_SUPERSEDED | REDUNDANT_REFRESH_DISCARDED |
| 35129545058 | failure | 2026-09-16T17:39:29Z | Classify tooling failures | Validate tooling incident ledger outputs | CLASSIFIER_CLOSURE_GATE | DETECTED_AND_BLOCKED |

## Closure rule

This ledger is closed only when both `unknown_entries` and `unresolved_entries` are exactly zero. CI enforces both conditions.
