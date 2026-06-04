def calculate_scores(arch, patches, gaps):
    detected=sum(1 for v in arch.values() if isinstance(v,list) and v)
    total=max(1, sum(1 for v in arch.values() if isinstance(v,list)))
    patch_detected=sum(1 for p in patches if p['implementation_status']!='missing')
    ci=bool(arch.get('ci_cd')); tests=bool(arch.get('tests')); evidence=bool(arch.get('evidence')); deploy=bool(arch.get('deployment')); audit=bool(arch.get('audit_telemetry'))
    scores={
    "repository_visibility_readiness": min(95, 25+len(arch.get('root_files',[]))*5),
    "architecture_understanding_readiness": min(85, int(detected/total*70)),
    "security_patch_point_readiness": min(70, int(patch_detected/len(patches)*60)) if patches else 0,
    "control_implementation_readiness": min(35, patch_detected*2),
    "test_readiness": 35 if tests else 5,
    "demo_attack_readiness": 20 if any('security_test' in g.get('area','').lower() for g in gaps) else 3,
    "ci_readiness": 45 if ci else 5,
    "evidence_readiness": 35 if evidence else 5,
    "staging_readiness": 20 if deploy else 3,
    "production_style_portfolio_readiness": min(60, (35 if tests else 5)+(15 if ci else 0)+(10 if evidence else 0)),
    "enterprise_production_candidate_readiness": min(40, (8 if deploy else 2)+(8 if audit else 0)+(8 if ci else 0)+(4 if evidence else 0))}
    return {k: min(99, max(0,v)) for k,v in scores.items()}
