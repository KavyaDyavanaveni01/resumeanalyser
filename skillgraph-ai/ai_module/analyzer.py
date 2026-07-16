import re

# Define target career goals and their required skills
CAREER_GOALS = {
    "Full Stack Developer": ["Java", "Spring Boot", "Python", "Flask", "JavaScript", "HTML", "CSS", "Bootstrap", "SQL", "Git", "Docker", "REST APIs", "React", "Linux"],
    "Data Scientist": ["Python", "SQL", "Machine Learning", "Deep Learning", "Pandas", "NumPy", "Scikit-Learn", "TensorFlow", "PyTorch", "spaCy", "Git", "Data Visualization", "R"],
    "DevOps Engineer": ["Linux", "Docker", "Kubernetes", "AWS", "Jenkins", "Terraform", "Ansible", "Git", "CI/CD", "Python", "Shell Scripting", "Nginx", "Monitoring"],
    "Frontend Developer": ["HTML", "CSS", "JavaScript", "React", "Vue", "Angular", "Bootstrap", "Tailwind CSS", "Sass", "Webpack", "Git", "Responsive Design"]
}

# Detailed regexes for extracting skills (case-insensitive)
SKILLS_DICTIONARY = {
    "Java": r"\bjava\b(?!script)",
    "Spring Boot": r"\bspring\s*boot\b|\bspring\s*framework\b",
    "Python": r"\bpython\b",
    "Flask": r"\bflask\b",
    "JavaScript": r"\bjavascript\b|\bjs\b",
    "HTML": r"\bhtml\b|\bhtml5\b",
    "CSS": r"\bcss\b|\bcss3\b",
    "Bootstrap": r"\bbootstrap\b",
    "SQL": r"\bsql\b|\bmysql\b|\bpostgresql\b|\bsqlite\b|\boracle\s*db\b|\bmariadb\b",
    "Git": r"\bgit\b|\bgithub\b|\bgitlab\b|\bversion\s*control\b",
    "Docker": r"\bdocker\b",
    "REST APIs": r"\brest\s*api\b|\brest\s*apis\b|\brestful\b",
    "React": r"\breact\b|\breactjs\b|\breact\.js\b",
    "Linux": r"\blinux\b|\bubuntu\b|\bdebian\b|\bcentos\b|\bredhat\b",
    "Machine Learning": r"\bmachine\s*learning\b|\bml\b",
    "Deep Learning": r"\bdeep\s*learning\b|\bdl\b",
    "Pandas": r"\bpandas\b",
    "NumPy": r"\bnumpy\b",
    "Scikit-Learn": r"\bscikit\s*learn\b|\bsklearn\b",
    "TensorFlow": r"\btensorflow\b|\btf\b",
    "PyTorch": r"\bpytorch\b",
    "spaCy": r"\bspacy\b",
    "Data Visualization": r"\bdata\s*visualization\b|\btableau\b|\bpowerbi\b|\bmatplotlib\b|\bseaborn\b|\bplotly\b",
    "R": r"\br\s*programming\b|\b(?<![a-zA-Z])r(?![a-zA-Z])\b",
    "Kubernetes": r"\bkubernetes\b|\bk8s\b",
    "AWS": r"\baws\b|\bamazon\s*web\s*services\b",
    "Jenkins": r"\bjenkins\b",
    "Terraform": r"\bterraform\b",
    "Ansible": r"\bansible\b",
    "CI/CD": r"\bci/cd\b|\bci\s*cd\b|\bcontinuous\s*integration\b",
    "Shell Scripting": r"\bshell\s*scripting\b|\bbash\b|\bpowershell\b",
    "Nginx": r"\bnginx\b",
    "Monitoring": r"\bmonitoring\b|\bprometheus\b|\bgrafana\b|\belk\b",
    "Vue": r"\bvue\b|\bvuejs\b|\bvue\.js\b",
    "Angular": r"\bangular\b|\bangularjs\b",
    "Tailwind CSS": r"\btailwind\b|\btailwindcss\b",
    "Sass": r"\bsass\b|\bscss\b",
    "Webpack": r"\bwebpack\b",
    "Responsive Design": r"\bresponsive\s*design\b|\bmobile\s*first\b"
}

# Timeline milestone, step details, and certification mapping
SKILL_METRICS = {
    "Java": {
        "milestone": "Month 1",
        "description": "Learn Core Java (OOP, Multi-threading, Collections, Lambda Expressions).",
        "cert": "Oracle Certified Professional: Java SE Developer"
    },
    "Spring Boot": {
        "milestone": "Month 2",
        "description": "Master Spring Boot framework, Dependency Injection, JPA/Hibernate, and RESTful APIs.",
        "cert": "VMware Spring Certified Professional"
    },
    "Python": {
        "milestone": "Month 1",
        "description": "Study Python fundamentals, data structures, file handling, and packaging.",
        "cert": "PCEP (Certified Entry-Level Python Programmer)"
    },
    "Flask": {
        "milestone": "Month 2",
        "description": "Learn Python Flask for lightweight backend service development.",
        "cert": "Python Web Developer Certification"
    },
    "JavaScript": {
        "milestone": "Month 1",
        "description": "Learn JavaScript (ES6+, DOM Manipulation, Async/Await, Events).",
        "cert": "W3Schools JavaScript Developer Certificate"
    },
    "HTML": {
        "milestone": "Week 1",
        "description": "Study semantic HTML5 markup, accessibility, and structures.",
        "cert": "W3Schools HTML Developer Certificate"
    },
    "CSS": {
        "milestone": "Week 2",
        "description": "Learn CSS3 Layouts (Flexbox, Grid), Media Queries, and Animations.",
        "cert": "W3Schools CSS Developer Certificate"
    },
    "Bootstrap": {
        "milestone": "Week 3",
        "description": "Utilize Bootstrap 5 grid system, UI components, and responsiveness utilities.",
        "cert": "Bootstrap 5 CSS Certification"
    },
    "SQL": {
        "milestone": "Month 1",
        "description": "Learn relational database design, queries, joins, indices, and transactions.",
        "cert": "Oracle Database SQL Certified Associate"
    },
    "Git": {
        "milestone": "Week 1",
        "description": "Master Git version control, branching, merging, and remote collaboration on GitHub.",
        "cert": "GitHub Actions / Git Fundamentals Badge"
    },
    "Docker": {
        "milestone": "Month 3",
        "description": "Learn containerization: dockerfiles, images, containers, networks, and volumes.",
        "cert": "Docker Certified Associate"
    },
    "REST APIs": {
        "milestone": "Month 2",
        "description": "Design RESTful Web Services: HTTP methods, status codes, JSON payload design.",
        "cert": "REST API Design Academy Certificate"
    },
    "React": {
        "milestone": "Month 2",
        "description": "Build single-page apps using React components, props, state, hooks, and routing.",
        "cert": "Meta Front-End Developer Certificate (Coursera)"
    },
    "Linux": {
        "milestone": "Month 1",
        "description": "Understand Linux command line navigation, shell scripting, and permissions.",
        "cert": "CompTIA Linux+"
    },
    "Machine Learning": {
        "milestone": "Month 2",
        "description": "Understand supervised & unsupervised models (regression, clustering, trees).",
        "cert": "Stanford Machine Learning Specialization"
    },
    "Deep Learning": {
        "milestone": "Month 3",
        "description": "Build neural networks (ANN, CNN, RNN) for advanced predictions.",
        "cert": "DeepLearning.AI TensorFlow Developer Certificate"
    },
    "Pandas": {
        "milestone": "Month 1",
        "description": "Learn data structures (DataFrames, Series) and manipulation using Python Pandas.",
        "cert": "Kaggle Data Cleaning Certification"
    },
    "NumPy": {
        "milestone": "Week 3",
        "description": "Learn array computation, slicing, vectorization, and algebraic formulas.",
        "cert": "Kaggle Intro to Python Badge"
    },
    "Scikit-Learn": {
        "milestone": "Month 2",
        "description": "Apply predictive models and evaluation metrics using Scikit-Learn.",
        "cert": "IBM Data Science Professional Certificate"
    },
    "TensorFlow": {
        "milestone": "Month 3",
        "description": "Build, compile, and train deep neural models using TensorFlow.",
        "cert": "Google TensorFlow Developer Certificate"
    },
    "PyTorch": {
        "milestone": "Month 3",
        "description": "Implement Deep Learning architectures and autograd using PyTorch.",
        "cert": "Deep Learning with PyTorch (Udacity)"
    },
    "spaCy": {
        "milestone": "Month 2",
        "description": "Learn Natural Language Processing pipeline: tokenization, NER, parsing.",
        "cert": "Advanced NLP with spaCy Certificate"
    },
    "Data Visualization": {
        "milestone": "Month 1",
        "description": "Create analytical dashboards using Tableau, Power BI, or Matplotlib.",
        "cert": "Tableau Desktop Certified Associate"
    },
    "R": {
        "milestone": "Month 2",
        "description": "Master statistics, regression models, and plotting (ggplot2) in R.",
        "cert": "Google Data Analytics Professional Certificate"
    },
    "Kubernetes": {
        "milestone": "Month 4",
        "description": "Learn cluster architecture, pods, deployments, services, ingress, and configmaps.",
        "cert": "Certified Kubernetes Administrator (CKA)"
    },
    "AWS": {
        "milestone": "Month 3",
        "description": "Learn AWS Cloud infrastructure (EC2, S3, RDS, IAM, Lambda, VPC).",
        "cert": "AWS Certified Solutions Architect - Associate"
    },
    "Jenkins": {
        "milestone": "Month 3",
        "description": "Create CI/CD pipelines, build triggers, and automated deployments using Jenkins.",
        "cert": "CloudBees Jenkins Platform Certification"
    },
    "Terraform": {
        "milestone": "Month 4",
        "description": "Deploy Infrastructure as Code (IaC), state files, providers, and modules.",
        "cert": "HashiCorp Certified: Terraform Associate"
    },
    "Ansible": {
        "milestone": "Month 4",
        "description": "Automate configurations using playbooks, inventories, roles, and tasks.",
        "cert": "Red Hat Certified Specialist in Ansible Automation"
    },
    "CI/CD": {
        "milestone": "Month 3",
        "description": "Integrate code linting, tests, builds, and container uploads into release pipelines.",
        "cert": "GitLab Certified CI/CD Associate"
    },
    "Shell Scripting": {
        "milestone": "Month 2",
        "description": "Automate routine system tasks and environment setups using Bash/PowerShell.",
        "cert": "Linux Professional Institute (LPI) Shell Scripting Badge"
    },
    "Nginx": {
        "milestone": "Month 3",
        "description": "Configure HTTP server, reverse proxying, load balancing, and SSL termination.",
        "cert": "NGINX Core Certified Specialist"
    },
    "Monitoring": {
        "milestone": "Month 4",
        "description": "Implement alerts, log aggregation, and system dashboarding using Prometheus.",
        "cert": "Certified Prometheus Associate (PCA)"
    },
    "Vue": {
        "milestone": "Month 2",
        "description": "Develop dynamic web clients with components and state using Vue.js.",
        "cert": "Vue.js Certified Frontend Developer"
    },
    "Angular": {
        "milestone": "Month 3",
        "description": "Build scalable enterprise SPAs using Angular, TypeScript, and RxJS.",
        "cert": "Google Developer Certified Web Specialist"
    },
    "Tailwind CSS": {
        "milestone": "Week 3",
        "description": "Implement utility-first layouts, responsiveness, and dark styling with Tailwind.",
        "cert": "Tailwind CSS Developer Badge"
    },
    "Sass": {
        "milestone": "Week 2",
        "description": "Compile advanced stylesheets using nested styling, mixins, variables, and loops.",
        "cert": "Advanced CSS/Sass Specialist Certificate"
    },
    "Webpack": {
        "milestone": "Month 3",
        "description": "Configure module bundle loaders, optimization chunks, and environmental variables.",
        "cert": "Frontend Tooling Certification"
    },
    "Responsive Design": {
        "milestone": "Week 2",
        "description": "Develop fluid UI breakpoints using flex, grids, and viewport metrics.",
        "cert": "FreeCodeCamp Responsive Web Design Certificate"
    }
}

def analyze_resume(text, career_goal):
    """
    Perform skill extraction and gap analysis.
    """
    # 1. Match career goal to predefined list (default to Full Stack Developer if missing)
    goal = career_goal
    if goal not in CAREER_GOALS:
        # Fallback search
        closest_goal = "Full Stack Developer"
        for g in CAREER_GOALS.keys():
            if g.lower() in goal.lower():
                closest_goal = g
                break
        goal = closest_goal

    required_skills = CAREER_GOALS[goal]

    # 2. Extract skills using Regex Dictionary
    extracted_skills = []
    text_lower = text.lower()
    
    for skill, regex in SKILLS_DICTIONARY.items():
        if re.search(regex, text_lower):
            extracted_skills.append(skill)

    # 3. Calculate missing skills and match percentage
    matched_skills = [s for s in required_skills if s in extracted_skills]
    missing_skills = [s for s in required_skills if s not in extracted_skills]

    # Ensure match percentage calculation has no division by zero
    total_req = len(required_skills)
    match_percentage = round((len(matched_skills) / total_req) * 100, 2) if total_req > 0 else 100.0

    # 4. Generate Learning Roadmap
    learning_roadmap = []
    # Order missing skills sequentially by milestone duration (e.g. Weeks first, then Month 1, Month 2...)
    def get_milestone_weight(skill):
        metrics = SKILL_METRICS.get(skill, {"milestone": "Month 5"})
        milestone = metrics["milestone"].lower()
        if "week 1" in milestone: return 1
        if "week 2" in milestone: return 2
        if "week 3" in milestone: return 3
        if "week 4" in milestone: return 4
        if "month 1" in milestone: return 5
        if "month 2" in milestone: return 6
        if "month 3" in milestone: return 7
        if "month 4" in milestone: return 8
        return 9

    sorted_missing = sorted(missing_skills, key=get_milestone_weight)

    for idx, skill in enumerate(sorted_missing):
        metrics = SKILL_METRICS.get(skill, {
            "milestone": f"Step {idx + 1}",
            "description": f"Learn {skill} core concepts and apply them in minor projects."
        })
        learning_roadmap.append({
            "step": idx + 1,
            "skill": skill,
            "milestone": metrics["milestone"],
            "description": metrics["description"]
        })

    # 5. Generate Certifications
    certifications = []
    for skill in missing_skills:
        metrics = SKILL_METRICS.get(skill)
        if metrics and "cert" in metrics:
            certifications.append({
                "skill": skill,
                "certification": metrics["cert"]
            })

    return {
        "match_percentage": match_percentage,
        "extracted_skills": matched_skills,
        "missing_skills": missing_skills,
        "learning_roadmap": learning_roadmap,
        "certifications": certifications
    }
