import textwrap

import plotly.express as px
import requests


def main() -> None:
    """Run and show the repositories graph."""
    # Ask the user for a programming language to search.
    language = input("Which programming language? ")

    status_code, response_dict = get_github_data(language)
    print(f"Status code: {status_code}")
    print(f"Complete results: {not response_dict['incomplete_results']}")

    # Process repository information.
    repo_dicts = response_dict["items"]
    repo_links, stars, hover_texts = [], [], []
    for repo_dict in repo_dicts:
        # Turn repo names into active links.
        repo_name = repo_dict["name"]
        repo_url = repo_dict["html_url"]
        repo_link = f"<a href='{repo_url}'>{repo_name}</a>"
        repo_links.append(repo_link)

        stars.append(repo_dict["stargazers_count"])

        # Build hover texts.
        owner = repo_dict["owner"]["login"]
        if repo_dict["description"]:
            description = "<br />".join(
                textwrap.wrap(
                    repo_dict["description"],
                    width=45,
                    max_lines=10,
                )
            )
        else:
            description = "No Description."

        hover_text = f"<i>{owner}</i><br />{description}"
        hover_texts.append(hover_text)

    # Make visualization.
    title = f"Most-Starred {language.capitalize()} Projects on GitHub"
    labels = {"x": "Repository", "y": "Stars"}
    fig = px.bar(
        x=repo_links,
        y=stars,
        title=title,
        labels=labels,
        hover_name=hover_texts,
    )

    fig.update_layout(
        title_font_size=28,
        xaxis_title_font_size=20,
        yaxis_title_font_size=20,
    )

    fig.update_traces(marker_color="SteelBlue", marker_opacity=0.6)

    fig.show()


def get_github_data(language: str) -> tuple[int, dict]:
    """Get the GitHub data for the current language.

    Returns a tuple with the status code and the JSON dictionary.
    """
    # Make an API call to GitHub.
    url = "https://api.github.com/search/repositories"
    url += f"?q=language:{language}+sort:stars+stars:>10000"

    headers = {"Accept": "application/vnd.github.v3+json"}
    r = requests.get(url, headers=headers)

    # Process overall results.
    response_dict = r.json()

    return (r.status_code, response_dict)


if __name__ == "__main__":
    # Execute the program.
    main()
