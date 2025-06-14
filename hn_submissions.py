from operator import itemgetter

import plotly.express as px
import requests


def main() -> None:
    """Main function to run this script.
    Makes calls to the Hacker Rank API.
    """
    # Make an API call and check the response.
    url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    r = requests.get(url)
    print(f"Status code: {r.status_code}")

    # Process information about each submission.
    submission_ids = r.json()
    submission_dicts = []
    for submission_id in submission_ids[:30]:
        # Make a new API call for each submission.
        url = f"https://hacker-news.firebaseio.com/v0/item/{submission_id}.json"
        r = requests.get(url)
        print(f"id: {submission_id}\tstatus: {r.status_code}")
        response_dict = r.json()

        # Build a dictionary for each article.
        try:
            submission_dict = {
                "title": response_dict["title"],
                "hn_link": f"https://news.ycombinator.com/item?id={submission_id}",
                "comments": response_dict["descendants"],
            }
            submission_dicts.append(submission_dict)
        except KeyError:
            # Ignore hiring posts submissions.
            pass

    # Sort each submission based on the total number of comments received.
    submission_dicts = sorted(
        submission_dicts,
        key=itemgetter("comments"),
        reverse=True,
    )

    # Create the list for the axes of the graph.
    submission_links, comments = [], []
    for submission_dict in submission_dicts:
        # Only take into account submissions with more than 10 comments.
        if (sub_comments := submission_dict["comments"]) > 10:
            # Turn the submission title into an active link.
            sub_title = submission_dict["title"]
            sub_url = submission_dict["hn_link"]
            sub_link = f"<a href='{sub_url}'>{sub_title}</a>"
            submission_links.append(sub_link)

            # Append the total number of comments.
            comments.append(sub_comments)

    # Make the visualization
    title = "Most Active Discussions in Hacker Rank"
    labels = {"x": "Submissions", "y": "Number of comments"}
    fig = px.bar(
        x=submission_links,
        y=comments,
        title=title,
        labels=labels,
    )

    # Change the font settings.
    fig.update_layout(
        title_font_size=28,
        xaxis_title_font_size=14,
        yaxis_title_font_size=14,
    )

    fig.show()


if __name__ == "__main__":
    main()
