import instaloader
import csv
import os

USERNAME_TO_SCRAPE = os.getenv("robbinsarchitecture")
POST_LIMIT = 200

if not USERNAME_TO_SCRAPE:
    raise ValueError("IG_USERNAME environment variable not set")

L = instaloader.Instaloader(
    download_pictures=False,
    download_videos=False,
    download_video_thumbnails=False,
    download_comments=False,
    save_metadata=False,
)

profile = instaloader.Profile.from_username(L.context, USERNAME_TO_SCRAPE)

output_file = f"{USERNAME_TO_SCRAPE}_event_data.csv"

with open(output_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow([
        "post_date",
        "caption",
        "hashtags",
        "tagged_accounts",
        "location",
        "post_url"
    ])

    for i, post in enumerate(profile.get_posts()):
        if i >= POST_LIMIT:
            break

        writer.writerow([
            post.date_utc.strftime("%Y-%m-%d"),
            post.caption or "",
            ", ".join(post.caption_hashtags),
            ", ".join(post.caption_mentions),
            post.location.name if post.location else "",
            f"https://www.instagram.com/p/{post.shortcode}/"
        ])
