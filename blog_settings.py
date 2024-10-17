import sqlite3
('/home/kulbache/construction/db/kulbachenko_blog.db')

def get_blog_posts(table_name, page, per_page=9, tag=None):
    offset = (page - 1) * per_page
    conn = sqlite3.connect('/Users/macbook/PycharmProjects/construction_site/db/kulbachenko_blog.db')
    cursor = conn.cursor()

    if tag:
        # Вибираємо кількість статей за тегом
        query = f'SELECT COUNT(*) FROM {table_name} WHERE category LIKE ?'
        cursor.execute(query, ('%' + tag + '%',))
        total_posts = cursor.fetchone()[0]

        # Вибираємо статті за тегом з урахуванням поточної сторінки
        cursor.execute(
            f'SELECT id, category, title, short_description, content, created_at, image_url, image_alt, post_page_link '
            f'FROM {table_name} WHERE category LIKE ? '
            f'ORDER BY id DESC LIMIT ? OFFSET ?',
            ('%' + tag + '%', per_page, offset))
    else:
        # Вибираємо всі статті, якщо тег не вибраний
        query = f'SELECT COUNT(*) FROM {table_name}'
        cursor.execute(query)
        total_posts = cursor.fetchone()[0]

        cursor.execute(
            f'SELECT id, category, title, short_description, content, created_at, image_url, image_alt, post_page_link '
            f'FROM {table_name} '
            f'ORDER BY id DESC LIMIT ? OFFSET ?',
            (per_page, offset))

    posts = cursor.fetchall()
    conn.close()
    return posts

def get_total_posts(table_name, tag=None):
    conn = sqlite3.connect('/Users/macbook/PycharmProjects/construction_site/db/kulbachenko_blog.db')
    cursor = conn.cursor()

    if tag:
        query = f'SELECT COUNT(*) FROM {table_name} WHERE category LIKE ?'
        cursor.execute(query, ('%' + tag + '%',))
    else:
        query = f"SELECT COUNT(*) FROM {table_name}"
        cursor.execute(query)

    total = cursor.fetchone()[0]
    conn.close()
    return total


def get_video_posts(table_name):
    conn = sqlite3.connect('/Users/macbook/PycharmProjects/construction_site/db/kulbachenko_blog.db')
    cursor = conn.cursor()

    # Fetch the two latest posts tagged with 'video', sorted by created_at from newest to oldest
    cursor.execute(
        f'SELECT * FROM {table_name} WHERE category LIKE ? OR category LIKE ? OR category LIKE ? OR category LIKE ? '
        f'ORDER BY id DESC LIMIT 2',
        ('%Video%', '%Videod%', '%Видео%', '%Відео%')
    )

    posts = cursor.fetchall()
    conn.close()

    return posts


def get_news_posts(table_name):
    conn = sqlite3.connect('/Users/macbook/PycharmProjects/construction_site/db/kulbachenko_blog.db')
    cursor = conn.cursor()

    # Fetch the one latest post tagged with 'video', sorted by created_at from newest to oldest
    cursor.execute(
        f'SELECT *'
        f'FROM {table_name} WHERE category LIKE ? OR category LIKE ? OR category LIKE ? OR category LIKE ? '
        f'ORDER BY id DESC LIMIT 1',
        ('%News%', '%Uudised%', '%Новини%', '%Новости%'))

    posts = cursor.fetchall()
    conn.close()

    return posts
