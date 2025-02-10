from urllib.parse import urlparse, urlunparse


def remove_credentials(url):
    # Parse the URL
    parsed_url = urlparse(url)

    # Reconstruct the URL without the username and password
    clean_url = urlunparse(
        (
            parsed_url.scheme,
            parsed_url.hostname + (f":{parsed_url.port}" if parsed_url.port else ""),
            parsed_url.path,
            parsed_url.params,
            parsed_url.query,
            parsed_url.fragment,
        )
    )

    return clean_url
