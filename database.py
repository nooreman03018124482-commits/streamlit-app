# database.py
# Simulates threat intelligence data and storage for Vigilaire


def get_cisa_kev_threats():
  """Returns active CISA KEV and CVE threat entries for the dashboard."""
  return [
      {
          "CVE ID": "CVE-2023-34362",
          "Source": "CISA KEV",
          "Severity": "Critical",
          "Target": "SQL / File Transfer",
      },
      {
          "CVE ID": "CVE-2026-1102",
          "Source": "NVD Feed",
          "Severity": "High",
          "Target": "WordPress Core Auth",
      },
      {
          "CVE ID": "CVE-2026-0884",
          "Source": "CVE.org",
          "Severity": "Medium",
          "Target": "PHP Form Input",
      },
  ]


def log_audit_record(target_url, risk_score):
  """Mock function to record scan results in database storage."""
  # In a production app, this would write to Google BigQuery
  return True