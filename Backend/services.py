import requests

def parse_url(url: str) -> str:
    # Download the page
    response = requests.get(url)

    # Save the page to an HTML file
    with open("page.html", "w", encoding="utf-8") as f:
        f.write(response.text)

    # Return a success message
    return "Page downloaded successfully"
