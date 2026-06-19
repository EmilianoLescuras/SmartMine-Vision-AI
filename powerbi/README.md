# powerbi/

Stores Power BI report files (`.pbix`) and supporting assets for the SmartMine Vision AI analytics dashboard.

---

## Purpose

The Power BI dashboard consumes event and alert data from PostgreSQL to provide real-time and historical safety KPIs for mine site operators and safety managers.

---

## Planned Reports

| File                         | Description                                         |
|------------------------------|-----------------------------------------------------|
| `smartmine_safety.pbix`      | Main safety monitoring dashboard                    |
| `ppe_compliance.pbix`        | PPE violation trends, per-camera breakdown          |
| `proximity_alerts.pbix`      | Person-vehicle proximity alert history              |

---

## Planned KPIs

- PPE compliance rate (%) — per shift, per zone, per day
- Total detections per class per hour
- Proximity alert frequency — warning vs. critical
- Average response time to alert acknowledgment
- Vehicle activity heatmap by zone
- Daily/weekly safety trend lines

---

## Data Sources

Power BI will connect to:
- **PostgreSQL** (direct query or imported via scheduled refresh)
- **FastAPI** (REST connector for live data, Phase 6)

---

## Development Plan (Phase 6)

1. Design PostgreSQL views optimized for Power BI queries.
2. Configure ODBC / PostgreSQL connector in Power BI Desktop.
3. Build report pages: Overview → PPE → Vehicles → Alerts → Trends.
4. Publish to Power BI Service for stakeholder access.
5. Set up scheduled data refresh (hourly).

---

## Dependencies

- Power BI Desktop (Windows)
- PostgreSQL ODBC driver
- SmartMine FastAPI backend (for live feed, optional)
