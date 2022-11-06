from collections import namedtuple

Link = namedtuple("Link", "article_title article_link")

link = Link("gandalf", "penis")

print(link.article_link)
