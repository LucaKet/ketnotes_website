import os
import re
import markdown

BLOG_DIR = "blog"


def extract_title_and_body(md_content, post_folder):
    lines = md_content.split("\n")
    title = ""
    body = md_content
    for i, line in enumerate(lines):
        if line.startswith("# "):
            title = line[2:].strip()
            body = "\n".join(lines[i + 1:])
            break
    if not title:
        title = post_folder.replace("-", " ").replace("_", " ").title()
    return title, body


def convert_post(post_folder):
    md_path = os.path.join(BLOG_DIR, post_folder, "final.md")
    with open(md_path) as f:
        content = f.read()

    title, body = extract_title_and_body(content, post_folder)
    html_body = markdown.markdown(body, extensions=["extra"])

    post_html = f"""<!DOCTYPE html>
<html>
<head>
  <title>{title} - Ketnotes</title>
  <link rel="stylesheet" href="../../main_style.css">
</head>
<body>
  <div class="post">
    {html_body}
  </div>
</body>
</html>
"""

    post_dir = os.path.join(BLOG_DIR, post_folder)
    with open(os.path.join(post_dir, "index.html"), "w") as f:
        f.write(post_html)

    return title, post_folder


def generate_blog_index(posts):
    list_items = "\n".join(
        f'    <li><a href="{folder}/">{title}</a></li>'
        for title, folder in posts
    )

    index_html = f"""<!DOCTYPE html>
<html>
<head>
  <title>Blog - Ketnotes</title>
  <link rel="stylesheet" href="../main_style.css">
</head>
<body>
  <div class="blog-list">
    <h2>Blog</h2>
    <ul>
{list_items}
    </ul>
    <p><a href="../">&larr; Back to home</a></p>
  </div>
</body>
</html>
"""
    with open(os.path.join(BLOG_DIR, "index.html"), "w") as f:
        f.write(index_html)


def update_main_page(posts):
    lines = []
    for title, folder in posts:
        lines.append(
                f'    {title} <a href="blog/{folder}/index.html"><small>(link)</small></a>'
        )
    post_html = "\n".join(lines)

    with open("index.html") as f:
        content = f.read()

    pattern = r"(<!-- BLOG_POSTS_START -->\n).*?(\n\s*<!-- BLOG_POSTS_END -->)"
    new_content = re.sub(pattern, r"\1" + post_html + r"\2", content, count=1, flags=re.DOTALL)

    with open("index.html", "w") as f:
        f.write(new_content)


def sort_key(folder):
    try:
        return int(folder[:3])
    except ValueError:
        return -1


def main():
    post_folders = sorted(
        [
            d
            for d in os.listdir(BLOG_DIR)
            if os.path.isdir(os.path.join(BLOG_DIR, d))
            and os.path.exists(os.path.join(BLOG_DIR, d, "final.md"))
        ],
        key=sort_key,
        reverse=True,
    )

    posts = []
    for folder in post_folders:
        title, folder = convert_post(folder)
        posts.append((title, folder))

    generate_blog_index(posts)
    update_main_page(posts)
    print(f"Built {len(posts)} posts.")


if __name__ == "__main__":
    main()
