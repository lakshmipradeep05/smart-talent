"""
Skill taxonomy — maps every alias to a canonical skill name and category.
Rule-based, no AI needed.
"""

SKILL_TAXONOMY = {
    # ── Programming Languages ────────────────────────────────────────────────
    "python": ["python", "python3", "python2", "py"],
    "javascript": ["javascript", "js", "es6", "ecmascript"],
    "typescript": ["typescript", "ts"],
    "java": ["java", "jvm", "openjdk"],
    "csharp": ["c#", "csharp", ".net", "asp.net", "dotnet"],
    "cpp": ["c++", "cpp"],
    "go": ["golang", "go lang"],
    "kotlin": ["kotlin"],
    "swift": ["swift"],
    "ruby": ["ruby", "rails", "ruby on rails"],
    "php": ["php", "laravel"],
    "scala": ["scala"],
    "r": ["r programming", "rstudio"],

    # ── Frontend ─────────────────────────────────────────────────────────────
    "react": ["react", "reactjs", "react.js", "react native", "nextjs", "next.js"],
    "vue": ["vue", "vuejs", "vue.js", "nuxt"],
    "angular": ["angular", "angularjs"],
    "html": ["html", "html5"],
    "css": ["css", "css3", "scss", "sass", "tailwind", "bootstrap"],
    "svelte": ["svelte"],
    "redux": ["redux", "zustand", "mobx"],

    # ── Backend Frameworks ───────────────────────────────────────────────────
    "fastapi": ["fastapi"],
    "django": ["django"],
    "flask": ["flask"],
    "express": ["express", "expressjs", "express.js", "node.js", "nodejs"],
    "spring": ["spring", "spring boot"],
    "streamlit": ["streamlit"],

    # ── Databases ────────────────────────────────────────────────────────────
    "sql": ["sql", "mysql", "postgresql", "postgres", "sqlite"],
    "nosql": ["nosql", "mongodb", "dynamodb"],
    "redis": ["redis"],

    # ── Machine Learning / AI ────────────────────────────────────────────────
    "machine_learning": [
        "machine learning", "ml", "supervised learning",
        "unsupervised learning", "scikit-learn", "sklearn", "scikit learn"
    ],
    "deep_learning": [
        "deep learning", "neural network", "neural networks",
        "cnn", "rnn", "lstm", "transformer"
    ],
    "pytorch": ["pytorch", "torch"],
    "tensorflow": ["tensorflow", "keras"],
    "nlp": [
        "nlp", "natural language processing", "text mining",
        "nltk", "spacy", "bert", "gpt"
    ],
    "data_science": [
        "data science", "data analysis", "pandas",
        "numpy", "matplotlib", "seaborn", "jupyter"
    ],

    # ── Cloud & DevOps ───────────────────────────────────────────────────────
    "aws": ["aws", "amazon web services", "ec2", "s3", "lambda"],
    "azure": ["azure", "microsoft azure"],
    "gcp": ["gcp", "google cloud"],
    "docker": ["docker", "containerization"],
    "kubernetes": ["kubernetes", "k8s"],
    "git": ["git", "github", "gitlab", "version control"],
    "linux": ["linux", "unix", "bash", "shell scripting"],

    # ── Core CS ──────────────────────────────────────────────────────────────
    "dsa": ["data structures", "algorithms", "dsa", "data structures and algorithms"],
    "oop": ["object oriented", "oop", "object-oriented programming"],
    "api_design": ["rest api", "restful", "graphql", "api design"],
    "system_design": ["system design", "microservices", "distributed systems"],
}

# Skill → its parent category
# Used for partial matching: "pytorch" also counts as "machine_learning"
SKILL_HIERARCHY = {
    "pytorch":       "machine_learning",
    "tensorflow":    "machine_learning",
    "deep_learning": "machine_learning",
    "nlp":           "machine_learning",
    "data_science":  "machine_learning",
    "scikit_learn":  "machine_learning",
    "react":         "javascript",
    "vue":           "javascript",
    "angular":       "javascript",
    "fastapi":       "python",
    "django":        "python",
    "flask":         "python",
    "streamlit":     "python",
    "spring":        "java",
    "docker":        "devops",
    "kubernetes":    "devops",
    "aws":           "cloud",
    "azure":         "cloud",
    "gcp":           "cloud",
    "sql":           "databases",
    "nosql":         "databases",
    "redis":         "databases",
}