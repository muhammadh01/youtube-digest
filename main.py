import sys
from summarizer import summarize


def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <youtube-url>")
        return 1

    url = sys.argv[1]
    print(f"Fetching and summarizing: {url}\n")

    try:
        summary = summarize(url)
    except Exception as exc:
        print(f"Error: {exc}")
        return 1

    print(summary)
    return 0


if __name__ == "__main__":
    sys.exit(main())
