# Input identities (sha256)

## Claude host files (branch impl/claude-host-2026-10 @ 1de943af, unpublished; hashes allow matching at publication)
- `lib/prompts_v2.py` 0e71027198745d2e1f32cc506a45f066dbca56e643d14d9a7ae5679adceb6738
- `lib/verdict_v2.py` d1cc6507bb45c04624b3db8b7bd8e847e8426d96a0820290415177c0f92a1f6f
- `lib/roster_v2.py` 68df88cee60027f9ded926cc7d336f0cf4dee53ca27d96c541e57bf764e2121b
- `spec/prompts/common-clauses.md` 95384c4cc78dc56889d227717953868362ec4918a84d5357112a0c10d831579a
- `spec/prompts/leg-claude.md` ba6383a1a7e991165d1ca8df08f629446e5d83cf114ebab86e94a508ae7219d5
- `spec/prompts/leg-codex.md` d7e0e5017f54542e2be4b95f9c3a0f4e867096d432e7bee832ea0f03d80548df
- `spec/prompts/leg-google.md` e17eb874bf6ff023a5ee79bfffb4cca9970c35135d60d3354a8f9593bc0a6415
- `spec/prompts/investigation.md` a92982e6b9a9f82be8c8c2f8ccb8529a8599f3adf97a59250345e10a87f06583
- `spec/contracts/leg-verdict.schema.json` d755905ac60348542fc1dbbeb37b92bc3fab0a2dc34b7a1b454c935d0be04184
- `spec/contracts/review-legs.schema.json` 1611655cda859a6738ec8ff52dd3d3aa08539cc8ba01741c8a72426abda37cb9
- `spec/contracts/review-kind.schema.json` 855807a26cda96102858da345f4888ee8658ee2ecff7584aecf9cf31ba61f724
- `spec/review-legs.default.json` 5095fd2dd3e43c339d0c6a31c434741962f625aee5b2963c2d21c262fdcd2c46
- `.claude/triad-review-legs.json` 1f558d4b3666c82c342bab582627f4b8ea13e38df5883be40fbd22ad103f4a97

## Library bundle regenerated from those host prompt/schema bytes (lib-A2; tools/sync_spec_assets.py --write at 2d1e62e7)
- `data/source-manifest.json` contract_id 455dfd8a7d586d04eedb60ee492cf421e076a77bafcccbba12de37cc12bf0340
- `data/roster-bundle/source-manifest.json` contract_id a99fb58dbd920dfed0d88d8c8b9117bd07633b76b5d2565e05f50a5b5c423ed8
- `data/prompt-bundle/source-manifest.json` contract_id 9d405c589351aa3553db5709176504dcb56ff7f15aee72a922554555a9d1d89e

## Environment
- macOS 26.6.2 arm64; Python 3.12.13; uv 0.11.8
- library venv: jsonschema 4.26.0 referencing 0.37.0 (uv sync --locked at 2d1e62e7's lock)
- apt-equivalent venv (S1): jsonschema 4.10.3, referencing 0.31.0, pytest 9.1.1
