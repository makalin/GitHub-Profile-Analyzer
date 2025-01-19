import os
import sys
from pathlib import Path

current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

# Check for required packages
required_packages = ['requests', 'matplotlib']
missing_packages = []

for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        missing_packages.append(package)

if missing_packages:
    print("Required dependencies are missing. Please run:")
    print(f"pip install {' '.join(missing_packages)}")
    sys.exit(1)

try:
    from github_profile_analyzer import GitHubProfileAnalyzer
except ImportError as e:
    print(f"Error importing GitHubProfileAnalyzer: {str(e)}")
    sys.exit(1)

# Initialize the analyzer with token from environment variable
github_token = os.getenv('GITHUB_TOKEN')
if not github_token:
    print("Error: GITHUB_TOKEN environment variable is not set")
    print("Please set your GitHub token using: export GITHUB_TOKEN='your_token_here'")
    sys.exit(1)

analyzer = GitHubProfileAnalyzer(github_token=github_token)

try:
    # Generate a report for a GitHub user
    #report, visualizations = analyzer.generate_report("octocat")
    report, visualizations = analyzer.generate_report("makalin")
    
    # Print the report
    print(report)
except KeyError as e:
    print(f"Failed to access data: {str(e)}")
    print("This might indicate an issue with the API response format.")
    print("Please check if the GitHub API is returning the expected data structure.")
    # Add more detailed debug information
    if hasattr(analyzer, 'last_response'):
        print("\nAPI Response Debug:")
        print(f"Status Code: {analyzer.last_response.status_code}")
        print("Response Data:")
        try:
            print(analyzer.last_response.json())
        except Exception:
            print("Could not parse response as JSON")
            print(analyzer.last_response.text)
except Exception as e:
    print(f"An error occurred: {str(e)}")
    print("Please ensure:")
    print("1. Your GitHub token is valid")
    print("2. The username exists")
    print("3. You have permission to access the user's data")
    print("\nDebug information:")
    print(f"Error type: {type(e).__name__}")
    if hasattr(e, '__context__') and e.__context__:
        print(f"Context: {e.__context__}")