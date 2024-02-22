"""
String preprocessing for articles
"""


def lead_paragraph(content, max_size=800):
    """ Extract lead paragraph from article.

    Args:
        content (str): the article content
        max_size (int): the maximum size of the paragraph
    """

    clean_content = content.strip("Copyright (c) 2023 CercleFinance.com.").strip("(CercleFinance.com) - ")
    lead_paragraph = clean_content.split("\n", 1)[0]

    if len(lead_paragraph) > max_size:
        splitted_text_content = clean_content[:max_size].split(". ")

        if len(splitted_text_content) > 1:
            return ". ".join(splitted_text_content[:-1]).strip("\n") + "."

        else:
            return lead_paragraph[:max_size] + "..."

    return lead_paragraph


def title_lead(title, lead):
    """Aggregate title and lead paragraph, remove "\n"

    Args:
        title (str)
        lead (str)
    """

    title_lead = title + " " + lead

    return title_lead.replace("\n", " ")
