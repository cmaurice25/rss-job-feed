import feedparser


def fetch_feed_entries(rss_url, limit=5):
    feed = feedparser.parse(rss_url)
    return feed.entries[:limit]
