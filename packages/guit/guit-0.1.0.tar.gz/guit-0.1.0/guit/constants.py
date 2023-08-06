from typing import Dict

GIT_URL_PATTERNS: Dict[str, str] = {
    "https": "https://{domain}/{owner}/{repo}.git",
    "ssh": "git@{domain}:{owner}/{repo}.git",
}
