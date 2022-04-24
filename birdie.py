import requests
import curses
import time
from bs4 import BeautifulSoup

def get_news_page_raw(url):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36"
    header = {'User-Agent': user_agent}
    #print("[INFO] Fetching link : ", url)
    page = requests.get(url, headers=header, timeout=50)
    if page.status_code == 200:
        #print("-> GET Success")
        return page

def parse_newswirelk_site(page):
    ret_items = []
    soup = BeautifulSoup(page.content, "html.parser")
    #latest_news_section = soup.find("section", id_="hootkit-posts-list-5")
    news_columns = soup.find_all("div", class_="posts-list-columns")
    news_items = []
    req_news_columns = 2 if len(news_columns) > 5 else len(news_columns)
    for i in range(req_news_columns):
        nc = news_columns[i]
        nt = nc.find_all("div", class_="posts-listunit-content")
        for t in nt:
            news_items.append(t)
    max_news_items = 5 if len(news_items) > 5 else len(news_items)
    for i in range(max_news_items):
        news_entry = ["[NW]"]
        item = news_items[i]
        heading = item.find("h4", class_="posts-listunit-title")
        heading_val = heading.text.strip()
        #print("Heading : ", heading_val)
        news_entry.append(heading_val)
        link_val = item.find("a", href=True)['href']
        #print("Link : ", link_val)
        news_entry.append(str(link_val))
        ret_items.append(news_entry)
    return ret_items

def parse_ftlk_site(page):
    ret_items = []
    soup = BeautifulSoup(page.content, "html.parser")
    ## Get Breaking News
    br_post = soup.find("div", class_="card cardb")
    news_entry= ["[FT]"]
    heading = br_post.find("h3", class_="newsch")
    heading_val = heading.text.strip()
    #print(heading_val)
    news_entry.append(heading_val)
    link_val = br_post.find("a", href=True)['href']
    #print(link_val)
    news_entry.append(link_val)
    ret_items.append(news_entry)
    ## Get Other News
    news_posts = soup.find_all("div", class_="card cardbs")
    max_news_items = 4 if len(news_posts) > 4 else len(news_posts)
    for i in range(max_news_items):
        news_entry= ["[FT]"]
        post = news_posts[i]
        heading = post.find("h3", class_="newschs")
        heading_val = heading.text.strip()
        #print(heading_val)
        news_entry.append(heading_val)
        link_val = post.find("a", href=True)['href']
        #print(link_val)
        news_entry.append(link_val)
        ret_items.append(news_entry)
    return ret_items

def parse_newsfirstlk_site(page):
    ret_items = []
    soup = BeautifulSoup(page.content, "html.parser")
    ## Get main news
    news_entry = ["[NF]"]
    mn_post = soup.find("div", class_="main-news-heading")
    heading = mn_post.find("h1", class_="text-center")
    heading_val = heading.text.strip()
    #print(heading_val)
    news_entry.append(heading_val)
    link_val = mn_post.find("a", href=True)['href']
    #print(link_val)
    news_entry.append(link_val)
    ret_items.append(news_entry)
    ## Get Second Main News
    news_posts = soup.find_all("div", class_="sub-1-news-block")
    max_news_items = 2 if len(news_posts) > 2 else len(news_posts)
    for i in range(max_news_items):
        news_entry= ["[NF]"]
        post = news_posts[i]
        heading = post.find("h2", class_="text-center")
        heading_val = heading.text.strip()
        #print(heading_val)
        news_entry.append(heading_val)
        link_val = post.find("a", href=True)['href']
        #print(link_val)
        news_entry.append(link_val)
        ret_items.append(news_entry)
    ## Get Other News
    # news_column = soup.find("div", "col-md-4  no-padding hidden-xs hidden-sm ff-stack-w")
    # news_posts = news_column.find_all("a")
    # max_news_items = 3 if len(news_posts) > 3 else len(news_posts)
    # for i in range(max_news_items):
    #     news_entry= ["[NF]"]
    #     post = news_posts[i]
    #     print(post)
    #     heading = post.find("h2", class_="alert-news-heding")
    #     heading_val = heading.text.strip()
    #     print(heading_val)
    #     news_entry.append(heading_val)
    #     link_val = post.find("a", href=True)['href']
    #     print(link_val)
    #     news_entry.append(link_val)
    #     ret_items.append(news_entry)
    return ret_items

def parse_dailymirrorlk_site(page):
    ret_items = []
    soup = BeautifulSoup(page.content, "html.parser")
    news_columns = soup.find("div", class_="top-header-sub")
    news_posts = news_columns.find_all("div", class_="header lineg")
    req_news_posts = 5 if len(news_posts) > 5 else len(news_posts)
    for i in range(req_news_posts):
        news_entry = ["[DM]"]
        item = news_posts[i]
        heading = item.find("h3", class_="news-hd-tx")
        heading_val = heading.text.strip()
        #print("Heading : ", heading_val)
        news_entry.append(heading_val)
        link_val = item.find("a", href=True)['href']
        #print("Link : ", link_val)
        news_entry.append(str(link_val))
        ret_items.append(news_entry)
    return ret_items

def get_news_latest_news_items():
    ret_items = []
    ## News Site 1
    page = get_news_page_raw("https://www.newswire.lk")
    items = parse_newswirelk_site(page)
    ret_items = ret_items + items
    ## News Site 2
    page = get_news_page_raw("https://www.ft.lk/")
    items = parse_ftlk_site(page)
    ret_items = ret_items + items
    ## News Site 3
    page = get_news_page_raw("https://www.newsfirst.lk/")
    items = parse_newsfirstlk_site(page)
    ret_items = ret_items + items
    ## News Site 4
    page = get_news_page_raw("https://www.dailymirror.lk/")
    items = parse_dailymirrorlk_site(page)
    ret_items = ret_items + items
    return ret_items

if __name__ == "__main__":
    # news_entries = get_news_latest_news_items()
    screen = curses.initscr()
    num_rows, num_cols = screen.getmaxyx()
    max_display_items = num_rows // 3
    screen.addstr("Birdie : Loading Content ...")

    try:
        while True:
            news_entries = get_news_latest_news_items()
            screen.clear()
            max_display_items = min(max_display_items, len(news_entries))
            for i in range(max_display_items):
                entry = news_entries[i]
                line_1 = entry[0] + " " + entry[1] + "\n"
                screen.addstr(line_1)
                line_2 = entry[2] + " \n\n"
                screen.addstr(line_2)
            screen.refresh()
            time.sleep(60)
    except KeyboardInterrupt:
        pass