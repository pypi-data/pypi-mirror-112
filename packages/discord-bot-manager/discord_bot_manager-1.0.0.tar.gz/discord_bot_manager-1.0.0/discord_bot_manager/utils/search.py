import requests


def search(query):
    resp = requests.get(
        f"https://api.duckduckgo.com/?q={query}&format=json&pretty=1"
    ).json()

    if answer := resp.get("Answer"):
        return answer
    elif definition := resp.get("Definition"):
        return definition
    elif abstract := resp.get("Abstract"):
        return abstract
    elif related_topics := resp.get("RelatedTopics"):
        return related_topics[0].get("Text")
    else:
        return f"Couldn't find anything related to `{query}`"
