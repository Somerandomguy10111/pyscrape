from __future__ import annotations

from bs4 import BeautifulSoup, NavigableString, Tag, PageElement


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
