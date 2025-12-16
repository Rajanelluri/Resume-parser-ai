# backend/services/skills_config.py

ROLE_SKILLS = {
    "cloud_engineer": [
        "azure", "aws", "gcp", "virtual machines", "docker", "kubernetes",
        "linux", "iac", "terraform", "ansible", "powershell", "devops"
    ],

    "data_analyst": [
        "excel", "sql", "power bi", "tableau", "statistics", "python",
        "data cleaning", "reporting", "dashboard", "visualization"
    ],

    "data_engineer": [
        "sql", "python", "spark", "pyspark", "etl", "data pipelines",
        "airflow", "databricks", "kafka", "data modeling", "snowflake"
    ],

    "devops_engineer": [
        "ci/cd", "jenkins", "github actions", "docker", "kubernetes",
        "terraform", "ansible", "linux", "monitoring", "prometheus", "grafana"
    ],

    "cybersecurity_analyst": [
        "siem", "splunk", "incident response", "mfa", "zero trust",
        "network security", "iam", "vulnerability management", "phishing", "edr"
    ],

    "software_developer": [
        "python", "java", "javascript", "git", "apis", "rest",
        "oop", "debugging", "testing", "sql", "data structures"
    ],
}
