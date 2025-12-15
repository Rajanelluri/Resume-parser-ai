# backend/services/skills_config.py

cloud_engineer_skills = [
    "azure", "aws", "gcp", "virtual machines", "docker", "kubernetes",
    "linux", "iac", "terraform", "ansible", "powershell", "devops"
]

data_analyst_skills = [
    "excel", "sql", "power bi", "tableau", "statistics", "python",
    "data cleaning", "reporting", "dashboard", "visualization"
]

ROLE_SKILLS = {
    "cloud_engineer": cloud_engineer_skills,
    "data_analyst": data_analyst_skills,
}
