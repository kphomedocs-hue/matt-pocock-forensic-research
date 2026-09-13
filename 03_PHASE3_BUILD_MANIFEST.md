# Phase 3 Build Manifest

Frozen source: `mattpocock/skills` @ `3cca18b368ae95cdbdebbff572ccafa662551015`.

This manifest cryptographically binds the authoritative Phase 3 generator and acceptance-gate inputs to the generated outputs using SHA-256. It intentionally contains no timestamp so unchanged state is reproducible byte-for-byte.

Inputs fingerprinted: **14**. Outputs fingerprinted: **11**.

## Inputs

| Path | SHA-256 | Bytes |
|---|---|---:|
| `01_FILE_CENSUS.json` | `d8b67db99e2e7f8faa238ce23d1ecdc351d62b1f927bca6eb2b24cc374ce638d` | 62852 |
| `05_HISTORY_LEDGER.md` | `30b2106e9966591f0950f74f9ed68ed576865d3fd372fb9cba21965de7b3ec48` | 4388 |
| `03_REFERENCE_DISPOSITIONS.json` | `fd73861af35577456935bf864f9542f72fe38f5ac921ddf50adf8fbd231f5f5b` | 1926 |
| `03_ORPHAN_DISPOSITIONS.json` | `d5fccf73d72ff577277ddd513b0375a65953c2b67f5d18d44db06af14a3dd73c` | 2362 |
| `scripts/build_connection_graph.py` | `8637654ee7a93f6ecd075f9ceb599c60cb441cd3c94e6d10eda1447c8c40e7b3` | 17173 |
| `scripts/build_router_matrix.py` | `f37a809162fafeceacffa2bdedc2c46f1925c81ab7801ac78e189a21fdcf8eea` | 6719 |
| `scripts/build_distribution_matrix.py` | `378525c18c1e19e4f10772ee521f53c7d6efa6d0b3e4ead706c9031546af8925` | 10290 |
| `scripts/build_history_bindings.py` | `0d131e92bcaf0e937d3503be5d544081ad514dd591b4d3fde830285149be478c` | 9654 |
| `scripts/build_phase3_closure_index.py` | `d54c10b1fe8484a0646123df8de6061360d8e633ed32a0d849b2d7e8d170f344` | 13589 |
| `scripts/enrich_master_ledger_connections.py` | `ba0dcd6d2012aaa7dc950c73ed7ef8523d6954e955a18406dea09bce22150c03` | 2653 |
| `scripts/build_phase3_manifest.py` | `ea0954d5223270a385dc33c90a6ca0a40798ea79f11be1aa70d993a9e64b4fe7` | 4010 |
| `scripts/verify_phase3_manifest.py` | `22cc607713b72b89f37525eb953e199b09d805ba42b7b28f53ac892c61a1ba0a` | 1584 |
| `scripts/validate_phase3_quality.py` | `942f2f3aeb9ab0c135aaef2aeb45d7cd7cba732b819e11b89f604337d5f10f7a` | 14953 |
| `.github/workflows/rebuild-phase3-state.yml` | `dd4f51732d4b364b31a843edc56f4812ad04126c2faa67715b97ccaa823a876f` | 6073 |

## Outputs

| Path | SHA-256 | Bytes |
|---|---|---:|
| `01_MASTER_FILE_LEDGER.md` | `04ea5006569d91ceead4a2acb366e76428849fa21e7af5ff87bcad29781ce490` | 36228 |
| `03_CONNECTION_EDGES.json` | `5cd78ec0dc3d5c584b63745763e834c455976c9c7e4482e02f840381a427c4a7` | 153578 |
| `03_CONNECTION_INDEX.md` | `8c72981ee3555dd1dc4a81e7febecf8568ce460bec57ebf5080925f7fb68990e` | 18003 |
| `03_ROUTER_MATRIX.json` | `ef8c1b111793f33cf6c13d45f7c87b17bff49a8a2b39ae9bef28eecced3e87f3` | 9889 |
| `03_ROUTER_MATRIX.md` | `cec01fdcbf6e27041a68098ee80438a1ad613b0e4d1638372d1def6f33ada63d` | 3006 |
| `03_DISTRIBUTION_MATRIX.json` | `6585cfcde43c0061b2332857cf3a77d8d710e44e234104c4b274c32326ffa5ed` | 18470 |
| `03_DISTRIBUTION_MATRIX.md` | `0a881421e29296fb8084a38bd50786f7bb7ce5558464723682f3fb8b91ae5f69` | 4115 |
| `03_HISTORY_BINDINGS.json` | `e93a9f6049cabdb275fd3d97b16b5976202fe7c28985aaaf5c43e1ba11513d42` | 90948 |
| `03_HISTORY_BINDINGS.md` | `1f7fbe0b51fb6592a2c875dbf55a8e73ba09e4ba16b6fec6a3c67dab4ad66264` | 7516 |
| `03_PHASE3_CLOSURE_INDEX.json` | `5508d3ecbec5c99b74f6bfed9823883ba05f2b9558dcdadda26ac908fb09ec79` | 112378 |
| `03_PHASE3_CLOSURE_INDEX.md` | `e652f32817b02d18d5c01d264ebb33ad9ed9c17838f9c93a08ebf1e9ecee0cc9` | 22521 |
