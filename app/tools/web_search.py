from ddgs import DDGS

def duckduckgo_search(query: str) -> str:
    try:
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=3)

        if not results:
            return "No results found."

        output = []
        for r in results:
            title = r.get("title", "(no title)")
            body = r.get("body", "(no description)")
            output.append(f"{title} — {body}")

        return "\n".join(output)

    except Exception as e:
        return f"Search error: {e}"
