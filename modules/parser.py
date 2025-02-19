import json
import logging

async def save_links(links, output_file):
    """Save links to a text file."""
    with open(output_file, "w") as f:
        for link in sorted(links):
            f.write(link + "\n")

async def export_json(links, output_json):
    """Export links to a JSON file."""
    with open(output_json, "w") as f:
        json.dump(sorted(links), f, indent=2)
    logging.info(f"Exported data to {output_json}")

async def generate_sitemap(links, output_sitemap):
    """Generate a Sitemap XML from crawled URLs."""
    sitemap_template = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{}
</urlset>"""
    url_entries = "\n".join(f"  <url><loc>{link}</loc></url>" for link in sorted(links))
    sitemap_content = sitemap_template.format(url_entries)

    with open(output_sitemap, "w") as f:
        f.write(sitemap_content)

    logging.info(f"Sitemap saved to {output_sitemap}")
