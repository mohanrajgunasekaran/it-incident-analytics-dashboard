import pandas as pd

def calculate_metrics(df):
    resolved = df[df['status'].eq('Resolved')].copy()
    resolved['resolution_hours'] = (pd.to_datetime(resolved['resolved_at']) - pd.to_datetime(resolved['created_at'])).dt.total_seconds() / 3600
    resolved['sla_breached'] = resolved['resolution_hours'] > resolved['sla_target_hours']
    return {'mttr_hours': resolved['resolution_hours'].mean() if len(resolved) else 0.0,
            'breach_rate_pct': resolved['sla_breached'].mean() * 100 if len(resolved) else 0.0,
            'resolved_count': len(resolved)}

def test_mttr_uses_resolved_records_only():
    df = pd.DataFrame([
        {'created_at':'2026-01-01 00:00','resolved_at':'2026-01-01 02:00','status':'Resolved','sla_target_hours':4},
        {'created_at':'2026-01-01 00:00','resolved_at':'2026-01-01 06:00','status':'Resolved','sla_target_hours':4},
        {'created_at':'2026-01-01 00:00','resolved_at':'','status':'Open','sla_target_hours':4}])
    m = calculate_metrics(df)
    assert m['resolved_count'] == 2 and m['mttr_hours'] == 4.0

def test_breach_rate_is_resolved_only():
    df = pd.DataFrame([
        {'created_at':'2026-01-01 00:00','resolved_at':'2026-01-01 02:00','status':'Resolved','sla_target_hours':4},
        {'created_at':'2026-01-01 00:00','resolved_at':'2026-01-01 06:00','status':'Resolved','sla_target_hours':4},
        {'created_at':'2026-01-01 00:00','resolved_at':'','status':'Open','sla_target_hours':1}])
    assert calculate_metrics(df)['breach_rate_pct'] == 50.0

def test_no_resolved_incidents_returns_zero():
    df = pd.DataFrame([{'created_at':'2026-01-01','resolved_at':'','status':'Open','sla_target_hours':4}])
    m = calculate_metrics(df)
    assert m['resolved_count'] == 0 and m['mttr_hours'] == 0.0 and m['breach_rate_pct'] == 0.0
