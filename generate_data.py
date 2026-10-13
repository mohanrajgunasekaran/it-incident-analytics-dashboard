"""Generate reproducible synthetic incident records."""
from pathlib import Path
import csv, random, math
from datetime import datetime, timedelta

OUT = Path(__file__).parent / "data" / "incidents.csv"
def main():
    random.seed(42)
    now = datetime.now().replace(minute=0, second=0, microsecond=0)
    start = now - timedelta(days=365)
    services = ["Customer Portal", "Identity & Access", "Data Integration", "Monitoring Platform", "Virtualisation", "Network Services"]
    categories = ["Availability", "Performance", "Access", "Data Pipeline", "Capacity", "Configuration"]
    causes = ["Configuration Change", "Capacity Constraint", "Software Defect", "Network Issue", "Dependency Failure", "Human Error", "Unknown"]
    teams = ["Platform Operations", "Application Support", "Network Operations", "Database Team", "Identity Team", "Vendor Support"]
    priorities, weights = ["P1", "P2", "P3", "P4"], [0.06, 0.22, 0.48, 0.24]
    targets = {"P1": 4, "P2": 8, "P3": 24, "P4": 72}
    impacts = ["Partial service outage", "Degraded response time", "Data feed delayed", "Authentication failures", "Increased monitoring alerts", "Workaround available"]
    rows = []
    for i in range(1, 901):
        created = start + timedelta(seconds=random.randint(0, int((now-start).total_seconds())))
        priority = random.choices(priorities, weights=weights, k=1)[0]
        duration = max(0.2, random.lognormvariate(math.log({"P1": 5.5, "P2": 6, "P3": 8, "P4": 10}[priority]), 0.8))
        status = random.choices(["Resolved", "In Progress", "Open"], weights=[0.88, 0.08, 0.04], k=1)[0]
        resolved = created + timedelta(hours=duration) if status == "Resolved" else None
        rows.append({
            "incident_id": f"INC-SYN-{i:05d}", "created_at": created.isoformat(timespec="minutes"),
            "resolved_at": resolved.isoformat(timespec="minutes") if resolved else "",
            "priority": priority, "service": random.choice(services), "category": random.choice(categories),
            "root_cause": random.choice(causes), "status": status, "sla_target_hours": targets[priority],
            "business_impact": random.choice(impacts), "assigned_team": random.choice(teams)
        })
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys()); writer.writeheader(); writer.writerows(rows)
    print(f"Wrote {len(rows)} synthetic incidents to {OUT}")
if __name__ == "__main__":
    main()
