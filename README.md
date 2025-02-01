# GitHub Profile Analyzer

A comprehensive Python tool for analyzing GitHub user profiles and generating detailed reports with visualizations. This tool helps you understand user activity patterns, repository statistics, and coding habits by analyzing public GitHub data.

## Features

- **Comprehensive User Analysis**
  - Basic profile information
  - Repository statistics
  - Activity patterns
  - Commit habits
  - Language preferences

- **Detailed Visualizations**
  - Programming language distribution
  - Commit time patterns
  - Quarterly activity timeline
  - Repository size distribution

- **Rich Analytics**
  - Repository metrics (stars, forks, watchers)
  - Code language analysis
  - License usage patterns
  - Commit frequency analysis
  - Time-based activity patterns

## Installation

1. Clone the repository:
```bash
git clone https://github.com/makalin/GitHub-Profile-Analyzer.git
cd GitHub-Profile-Analyzer
```

2. Install required dependencies:
```bash
pip install requests pandas numpy matplotlib seaborn
```

## Usage

### Basic Usage

```python
from github_profile_analyzer import GitHubProfileAnalyzer

# Initialize the analyzer
analyzer = GitHubProfileAnalyzer()

# Generate a report for a GitHub user
report, visualizations = analyzer.generate_report("octocat")

# Print the report
print(report)
```

### With GitHub Token (Recommended)

```python
# Initialize with GitHub token for higher rate limits
analyzer = GitHubProfileAnalyzer(github_token="your_github_token")
report, visualizations = analyzer.generate_report("octocat")
```

## Output

The analyzer generates two types of output:

1. **Text Report** including:
   - User information (name, bio, location, etc.)
   - Repository statistics
   - Language distribution
   - License usage
   - Activity patterns
   - Commit patterns

2. **Visualizations**:
   - Language distribution pie chart
   - Commit time distribution bar chart
   - Quarterly activity timeline
   - Repository size distribution histogram

## Configuration

The analyzer accepts a GitHub personal access token for increased API rate limits. To create a token:

1. Go to GitHub Settings → Developer Settings → Personal Access Tokens
2. Generate a new token with `repo` and `user` scopes
3. Pass the token when initializing the analyzer

## API Rate Limits

- Without authentication: 60 requests/hour
- With authentication: 5000 requests/hour

## Requirements

- Python 3.6+
- requests
- pandas
- numpy
- matplotlib
- seaborn

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- GitHub API for providing the data
- All contributors who participate in this project

## Error Handling

The analyzer includes robust error handling for common issues:
- Invalid usernames
- API rate limiting
- Network connectivity issues
- Empty repositories

## Known Limitations

- Analysis is limited to public repositories
- Some metrics may be affected by API rate limiting
- Large repositories might take longer to analyze
- Commit analysis is limited to the latest 5 repositories for performance

## Contact

For questions and feedback, please open an issue in the GitHub repository.
