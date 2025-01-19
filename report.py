import os
import sys
from pathlib import Path

current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

from github_profile_analyzer import GitHubProfileAnalyzer
github_token = os.getenv('GITHUB_TOKEN')

analyzer = GitHubProfileAnalyzer(github_token=github_token)

report, visualizations = analyzer.generate_report("makalin")

print(report)