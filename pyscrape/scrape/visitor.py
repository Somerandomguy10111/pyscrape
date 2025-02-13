from __future__ import annotations

import re

import requests
# noinspection PyProtectedMember
from bs4 import BeautifulSoup, Tag, PageElement, NavigableString


# ---------------------------------------------------------

class Scraper:
    def __init__(self, max_wait_time : float = 10):
        self.response_timeout : float = max_wait_time

    def scrape_mail_addresses(self, url : str) -> list[str]:
        html_code = self.scrape_html(url=url)
        return self.get_mail_addresses_in_text(text=html_code)

    def scrape_text(self, url: str, with_links : bool = False) -> str:
        page_html = self.scrape_html(url=url)
        return self._extract_text(page_html=page_html, with_links=with_links)

    def scrape_html(self, url: str) -> str:
        try:
            response = requests.get(url, timeout=self.response_timeout)
            return response.content
        except requests.exceptions.Timeout:
            raise requests.exceptions.Timeout(f'Timeout after {self.response_timeout} seconds')

    @staticmethod
    def site_exists(url : str, verbose : bool = False) -> bool:
        try:
            requests.get(url, timeout=10)
            return True
        except requests.exceptions.RequestException as e:
            if verbose:
                print(f"Error: {e}")
        return False

    @staticmethod
    def _extract_text(page_html : str, with_links : bool = False) -> str:
        SoupType = LinkSoup if with_links else BeautifulSoup
        soup = SoupType(page_html, 'html.parser')
        for script in soup(["script", "style"]):
            script.decompose()
        site_text = soup.get_text()
        lines = (line.strip() for line in site_text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        return '\n'.join(chunk for chunk in chunks if chunk)


    @staticmethod
    def get_mail_addresses_in_text(text: str) -> list[str]:
        username_part = r'[A-Za-z0-9._%+-]+'
        domain_part = r'[A-Za-z0-9.-]+'
        tld_part = r'[A-Z|a-z]{2,}'
        at_symbol = r'(?:@|\[at\]| \[at\] )'  # Non-capturing group

        email_pattern = fr'\b{username_part}{at_symbol}{domain_part}\.{tld_part}\b'

        mail_addresses = re.findall(email_pattern, text)
        mail_addresses = [address.replace(' [at] ', '@') for address in mail_addresses]
        mail_addresses = [address.replace('[at]', '@') for address in mail_addresses]

        return mail_addresses



class LinkSoup(BeautifulSoup):
    # noinspection PyUnresolvedReferences
    def _all_strings(self, strip=False, types=PageElement.default):
        _ = strip

        if types is self.default:
            types = self.interesting_string_types

        for descendant in self.descendants:
            if isinstance(descendant, Tag) and descendant.name == 'a':
                link_text = descendant.text.strip()
                link_text = link_text.replace('\n', ' ')
                yield str(f"<({link_text})[{descendant.get('href')}]> ")
            if isinstance(descendant, NavigableString) and descendant.parent.name == 'a':
                continue

            if types is None and not isinstance(descendant, NavigableString):
                continue
            descendant_type = type(descendant)
            if isinstance(types, type):
                if descendant_type is not types:
                    continue
            elif types is not None and descendant_type not in types:
                continue
            if strip:
                descendant = descendant.strip()
                if len(descendant) == 0:
                    continue
            yield descendant
