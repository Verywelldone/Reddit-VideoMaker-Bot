from playwright.sync_api import sync_playwright
from pathlib import Path
from rich.progress import track
from utils.console import print_step, print_substep
import re


def download_screenshots_of_reddit_posts(reddit_object, screenshot_num):
    """Downloads screenshots of reddit posts as they are seen on the web.

    Args:
        reddit_object: The Reddit Object you received in askreddit.py
        screenshot_num: The number of screenshots you want to download.
    """
    print_step("Downloading Screenshots of Reddit Posts 📷")

    # ! Make sure the reddit screenshots folder exists


    old_thread_title = reddit_object["thread_title"];
    thread_title = ''.join(ch for ch in old_thread_title if ch.isalnum())
    path  = "assets/{}".format(thread_title)


    Path(path).mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        print_substep("Launching Headless Browser...")

        browser = p.chromium.launch()

        # Get the thread screenshot
        page = browser.new_page(is_mobile=True, color_scheme="dark",device_scale_factor=3)

        page.goto(reddit_object["thread_url"])
        

        if page.locator('[data-testid="content-gate"]').is_visible():
            # This means the post is NSFW and requires to click the proceed button.

            print_substep("Post is NSFW. You are spicy... :fire:")
            page.locator('[data-testid="content-gate"] button').click()


        titlePath = 'assets/{}/title.png'.format(thread_title)
        
        page.locator('[data-test-id="post-content"]').screenshot(
            path=titlePath
        )

        for idx, comment in track(
            enumerate(reddit_object["comments"]), "Downloading screenshots..."
        ):

            # Stop if we have reached the screenshot_num
            if idx >= screenshot_num:
                break

            if page.locator('[data-testid="content-gate"]').is_visible():
                page.locator('[data-testid="content-gate"] button').click()

            page.goto(f'https://reddit.com{comment["comment_url"]}')

            commentPath = "assets/{}/comment_{}.png".format(thread_title,idx)
            
            page.locator(f"#t1_{comment['comment_id']}").screenshot(
                path=commentPath
            )
        print_substep("Screenshots downloaded Successfully.", style="bold green")
