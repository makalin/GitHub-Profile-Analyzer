import requests
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple, Any
import calendar
from io import BytesIO
import base64

class GitHubProfileAnalyzer:
    def __init__(self, github_token: str = None):
        """
        Initialize the GitHub Profile Analyzer.
        
        Args:
            github_token (str, optional): GitHub Personal Access Token for increased rate limits
        """
        self.headers = {}
        if github_token:
            self.headers = {'Authorization': f'token {github_token}'}
        self.base_url = 'https://api.github.com'

    def get_user_info(self, username: str) -> Dict[str, Any]:
        """Previous implementation remains the same"""
        response = requests.get(f'{self.base_url}/users/{username}', headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_user_repos(self, username: str) -> List[Dict[str, Any]]:
        """Previous implementation remains the same"""
        repos = []
        page = 1
        while True:
            response = requests.get(
                f'{self.base_url}/users/{username}/repos',
                params={'page': page, 'per_page': 100},
                headers=self.headers
            )
            response.raise_for_status()
            page_repos = response.json()
            if not page_repos:
                break
            repos.extend(page_repos)
            page += 1
        return repos

    def get_repo_commits(self, username: str, repo_name: str) -> List[Dict[str, Any]]:
        """
        Get commits for a specific repository.
        
        Args:
            username (str): GitHub username
            repo_name (str): Repository name
            
        Returns:
            list: List of commits
        """
        commits = []
        page = 1
        while True:
            response = requests.get(
                f'{self.base_url}/repos/{username}/{repo_name}/commits',
                params={'page': page, 'per_page': 100},
                headers=self.headers
            )
            if response.status_code == 409:  # Empty repository
                return []
            response.raise_for_status()
            page_commits = response.json()
            if not page_commits:
                break
            commits.extend(page_commits)
            page += 1
        return commits

    def analyze_profile(self, username: str) -> Dict[str, Any]:
        """
        Perform a comprehensive analysis of a GitHub profile.
        
        Args:
            username (str): GitHub username
            
        Returns:
            dict: Comprehensive profile analysis
        """
        # Get basic user information
        user_info = self.get_user_info(username)
        repos = self.get_user_repos(username)

        # Analyze repositories
        total_stars = sum(repo['stargazers_count'] for repo in repos)
        total_forks = sum(repo['forks_count'] for repo in repos)
        total_watchers = sum(repo['watchers_count'] for repo in repos)
        languages = Counter(repo['language'] for repo in repos if repo['language'])
        
        # Repository size analysis
        repo_sizes = [repo['size'] for repo in repos]
        
        # License analysis
        licenses = Counter(repo.get('license', {}).get('name') for repo in repos if repo.get('license'))
        
        # Analyze commit patterns
        commit_times = []
        commit_days = []
        for repo in repos[:5]:  # Analyze top 5 repos for performance
            commits = self.get_repo_commits(username, repo['name'])
            for commit in commits:
                if commit.get('commit', {}).get('author', {}).get('date'):
                    commit_date = datetime.strptime(
                        commit['commit']['author']['date'],
                        '%Y-%m-%dT%H:%M:%SZ'
                    )
                    commit_times.append(commit_date.hour)
                    commit_days.append(commit_date.weekday())

        # Calculate activity patterns
        creation_dates = [datetime.strptime(repo['created_at'], '%Y-%m-%dT%H:%M:%SZ') 
                         for repo in repos]
        update_dates = [datetime.strptime(repo['updated_at'], '%Y-%m-%dT%H:%M:%SZ') 
                       for repo in repos]
        
        # Calculate quarterly activity
        quarters = Counter()
        for date in update_dates:
            quarters[f"{date.year}-Q{(date.month-1)//3 + 1}"] += 1
        
        # Enhanced analysis results
        analysis = {
            'user_info': {
                'name': user_info.get('name'),
                'bio': user_info.get('bio'),
                'followers': user_info.get('followers'),
                'following': user_info.get('following'),
                'public_repos': user_info.get('public_repos'),
                'account_created': user_info.get('created_at'),
                'location': user_info.get('location'),
                'company': user_info.get('company'),
                'blog': user_info.get('blog')
            },
            'repository_stats': {
                'total_repos': len(repos),
                'total_stars': total_stars,
                'total_forks': total_forks,
                'total_watchers': total_watchers,
                'top_languages': dict(languages.most_common(10)),
                'avg_stars_per_repo': total_stars / len(repos) if repos else 0,
                'avg_repo_size': np.mean(repo_sizes) if repo_sizes else 0,
                'median_repo_size': np.median(repo_sizes) if repo_sizes else 0,
                'licenses': dict(licenses.most_common(5))
            },
            'activity_patterns': {
                'newest_repo': max(creation_dates).strftime('%Y-%m-%d'),
                'oldest_repo': min(creation_dates).strftime('%Y-%m-%d'),
                'last_update': max(update_dates).strftime('%Y-%m-%d'),
                'updates_per_quarter': dict(quarters.most_common()),
                'favorite_commit_hours': Counter(commit_times).most_common(3),
                'favorite_commit_days': Counter(commit_days).most_common(),
                'commit_frequency': {
                    'morning': len([h for h in commit_times if 5 <= h < 12]),
                    'afternoon': len([h for h in commit_times if 12 <= h < 17]),
                    'evening': len([h for h in commit_times if 17 <= h < 22]),
                    'night': len([h for h in commit_times if h >= 22 or h < 5])
                }
            }
        }
        
        return analysis

    def generate_visualizations(self, analysis: Dict[str, Any]) -> Dict[str, str]:
        """
        Generate visualizations based on the analysis data.
        
        Args:
            analysis (dict): Analysis data from analyze_profile
            
        Returns:
            dict: Dictionary of base64 encoded plot images
        """
        plots = {}
        
        # Set style for all plots
        plt.style.use('seaborn')
        
        # 1. Language Distribution Pie Chart
        plt.figure(figsize=(10, 6))
        languages = analysis['repository_stats']['top_languages']
        plt.pie(languages.values(), labels=languages.keys(), autopct='%1.1f%%')
        plt.title('Repository Language Distribution')
        plots['language_distribution'] = self._fig_to_base64()

        # 2. Commit Time Heatmap
        plt.figure(figsize=(12, 4))
        commit_hours = analysis['activity_patterns']['commit_frequency']
        times = ['Morning\n(5-12)', 'Afternoon\n(12-17)', 'Evening\n(17-22)', 'Night\n(22-5)']
        plt.bar(times, [commit_hours['morning'], commit_hours['afternoon'], 
                       commit_hours['evening'], commit_hours['night']])
        plt.title('Commit Activity by Time of Day')
        plt.ylabel('Number of Commits')
        plots['commit_time_distribution'] = self._fig_to_base64()

        # 3. Quarterly Activity Timeline
        plt.figure(figsize=(12, 4))
        quarters = analysis['activity_patterns']['updates_per_quarter']
        plt.plot(list(quarters.keys()), list(quarters.values()), marker='o')
        plt.title('Repository Updates by Quarter')
        plt.xticks(rotation=45)
        plt.ylabel('Number of Updates')
        plots['quarterly_activity'] = self._fig_to_base64()

        # 4. Repository Size Distribution
        plt.figure(figsize=(10, 6))
        sns.histplot(data=[repo['size'] for repo in analysis['repository_stats']['repos']], bins=30)
        plt.title('Repository Size Distribution')
        plt.xlabel('Size (KB)')
        plt.ylabel('Count')
        plots['repo_size_distribution'] = self._fig_to_base64()

        return plots

    def _fig_to_base64(self) -> str:
        """Convert matplotlib figure to base64 string"""
        buf = BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        plt.close()
        buf.seek(0)
        return base64.b64encode(buf.getvalue()).decode('utf-8')

    def generate_report(self, username: str) -> Tuple[str, Dict[str, str]]:
        """
        Generate a formatted report and visualizations of the profile analysis.
        
        Args:
            username (str): GitHub username
            
        Returns:
            tuple: (Formatted report string, Dictionary of visualization images)
        """
        analysis = self.analyze_profile(username)
        visualizations = self.generate_visualizations(analysis)
        
        report = f"""GitHub Profile Analysis for {username}
{'=' * 50}

User Information:
----------------
Name: {analysis['user_info']['name']}
Bio: {analysis['user_info']['bio']}
Location: {analysis['user_info']['location']}
Company: {analysis['user_info']['company']}
Blog: {analysis['user_info']['blog']}
Followers: {analysis['user_info']['followers']}
Following: {analysis['user_info']['following']}
Public Repositories: {analysis['user_info']['public_repos']}
Account Created: {analysis['user_info']['account_created']}

Repository Statistics:
-------------------
Total Repositories: {analysis['repository_stats']['total_repos']}
Total Stars: {analysis['repository_stats']['total_stars']}
Total Forks: {analysis['repository_stats']['total_forks']}
Total Watchers: {analysis['repository_stats']['total_watchers']}
Average Stars per Repository: {analysis['repository_stats']['avg_stars_per_repo']:.1f}
Average Repository Size: {analysis['repository_stats']['avg_repo_size']:.1f} KB
Median Repository Size: {analysis['repository_stats']['median_repo_size']:.1f} KB

Top Languages:
------------
{self._format_dict(analysis['repository_stats']['top_languages'])}

License Usage:
------------
{self._format_dict(analysis['repository_stats']['licenses'])}

Activity Patterns:
---------------
Newest Repository: {analysis['activity_patterns']['newest_repo']}
Oldest Repository: {analysis['activity_patterns']['oldest_repo']}
Last Update: {analysis['activity_patterns']['last_update']}

Commit Patterns:
-------------
Favorite Commit Hours: {', '.join(f"{hour}:00 ({count} commits)" for hour, count in analysis['activity_patterns']['favorite_commit_hours'])}
Favorite Commit Days: {', '.join(f"{calendar.day_name[day]} ({count} commits)" for day, count in analysis['activity_patterns']['favorite_commit_days'])}

Time of Day Distribution:
----------------------
Morning (5-12): {analysis['activity_patterns']['commit_frequency']['morning']} commits
Afternoon (12-17): {analysis['activity_patterns']['commit_frequency']['afternoon']} commits
Evening (17-22): {analysis['activity_patterns']['commit_frequency']['evening']} commits
Night (22-5): {analysis['activity_patterns']['commit_frequency']['night']} commits
"""
        return report, visualizations

# Example usage
if __name__ == "__main__":
    analyzer = GitHubProfileAnalyzer()
    try:
        report, visualizations = analyzer.generate_report("octocat")
        print(report)
        # Visualizations can be displayed or saved as needed
    except requests.exceptions.RequestException as e:
        print(f"Error accessing GitHub API: {e}")
