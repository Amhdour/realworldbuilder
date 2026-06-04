SUPPLY_NAMES={"license","pyproject.toml","requirements.txt","package.json","pnpm-lock.yaml","yarn.lock","package-lock.json","dockerfile","docker-compose.yml","sbom.json","cyclonedx.json"}
def indicators(files):
    return sorted([f.path for f in files if f.path.lower().split('/')[-1] in SUPPLY_NAMES or 'lock' in f.path.lower()])
