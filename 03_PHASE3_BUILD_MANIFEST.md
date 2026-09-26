# Phase 3 Build Manifest

Frozen source: `mattpocock/skills` @ `3cca18b368ae95cdbdebbff572ccafa662551015`.

This manifest cryptographically binds the authoritative Phase 3 generator and acceptance-gate inputs to the generated outputs using SHA-256. It intentionally contains no timestamp so unchanged state is reproducible byte-for-byte.

Inputs fingerprinted: **14**. Outputs fingerprinted: **11**.

## Inputs

| Path | SHA-256 | Bytes |
|---|---|---:|
| `01_FILE_CENSUS.json` | `d8b67db99e2e7f8faa238ce23d1ecdc351d62b1f927bca6eb2b24cc374ce638d` | 62852 |
| `05_HISTORY_LEDGER.md` | `56004a44b7edd09fdb581de7a617fb0988f6e6b97023b3d640e7ffa9f7c2a1ef` | 10227 |
| `03_REFERENCE_DISPOSITIONS.json` | `fd73861af35577456935bf864f9542f72fe38f5ac921ddf50adf8fbd231f5f5b` | 1926 |
| `03_ORPHAN_DISPOSITIONS.json` | `d5fccf73d72ff577277ddd513b0375a65953c2b67f5d18d44db06af14a3dd73c` | 2362 |
| `scripts/build_connection_graph.py` | `0fd9a0fd04a10d9ab34b3870035cbbfd126bd4e1ad57bb03a438edf67fe8443d` | 20440 |
| `scripts/build_router_matrix.py` | `f37a809162fafeceacffa2bdedc2c46f1925c81ab7801ac78e189a21fdcf8eea` | 6719 |
| `scripts/build_distribution_matrix.py` | `378525c18c1e19e4f10772ee521f53c7d6efa6d0b3e4ead706c9031546af8925` | 10290 |
| `scripts/build_history_bindings.py` | `ac7002f89dbc95b443f3388116b0ab927c9b4de493793d14f69119df7439812a` | 10185 |
| `scripts/build_phase3_closure_index.py` | `d54c10b1fe8484a0646123df8de6061360d8e633ed32a0d849b2d7e8d170f344` | 13589 |
| `scripts/enrich_master_ledger_connections.py` | `ba0dcd6d2012aaa7dc950c73ed7ef8523d6954e955a18406dea09bce22150c03` | 2653 |
| `scripts/build_phase3_manifest.py` | `ea0954d5223270a385dc33c90a6ca0a40798ea79f11be1aa70d993a9e64b4fe7` | 4010 |
| `scripts/verify_phase3_manifest.py` | `22cc607713b72b89f37525eb953e199b09d805ba42b7b28f53ac892c61a1ba0a` | 1584 |
| `scripts/validate_phase3_quality.py` | `9ea4acac42a449d89acc97acb5e5091241c75d5cd8f7abec191a2cb78b24be4a` | 15172 |
| `.github/workflows/rebuild-phase3-state.yml` | `7c2dea37a3aff27da0fa6dc4c35c773a92d529c85a0ad9495b7da43ff0a9f775` | 6074 |

## Outputs

| Path | SHA-256 | Bytes |
|---|---|---:|
| `01_MASTER_FILE_LEDGER.md` | `21d3c0f162c65d260714c25bf7551546fa9c897fd3f8271ed7a94f89452ba923` | 36231 |
| `03_CONNECTION_EDGES.json` | `5fa2bbca08b6b47334c212a006a593f8365ad5c5966fecf79035dcc31a38fc1b` | 199540 |
| `03_CONNECTION_INDEX.md` | `893a8c674c5c8eb83eacae14d621d424094de013e4f1b7d0b6879eaf392a3c8f` | 18383 |
| `03_ROUTER_MATRIX.json` | `ef8c1b111793f33cf6c13d45f7c87b17bff49a8a2b39ae9bef28eecced3e87f3` | 9889 |
| `03_ROUTER_MATRIX.md` | `cec01fdcbf6e27041a68098ee80438a1ad613b0e4d1638372d1def6f33ada63d` | 3006 |
| `03_DISTRIBUTION_MATRIX.json` | `6585cfcde43c0061b2332857cf3a77d8d710e44e234104c4b274c32326ffa5ed` | 18470 |
| `03_DISTRIBUTION_MATRIX.md` | `0a881421e29296fb8084a38bd50786f7bb7ce5558464723682f3fb8b91ae5f69` | 4115 |
| `03_HISTORY_BINDINGS.json` | `259f23f980840f1443322e1bb87aaf36299fecae3e3acd366a9aa3a03e24c52f` | 150281 |
| `03_HISTORY_BINDINGS.md` | `7cbfd0518c7e494e647b5f2d5353c550b2a2a6e1c9876642ebe0f13f939582b6` | 11353 |
| `03_PHASE3_CLOSURE_INDEX.json` | `ee091ad1a15a282722f73faaad580db1984608abf287b4c5be9027413bb579bf` | 112422 |
| `03_PHASE3_CLOSURE_INDEX.md` | `8b1eb3eca806cfdc5d5b27508eab85bb7af1578c97369e4d1c44a98cc9007767` | 22524 |
