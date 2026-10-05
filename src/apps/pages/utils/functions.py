from slugify import slugify


def make_slug(string: str) -> str:
    return slugify(string, max_length=60, word_boundary=True)
