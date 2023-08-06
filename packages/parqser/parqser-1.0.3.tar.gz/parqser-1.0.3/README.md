# parqser
Simple customizable scrapper and parser. Allows multithreading and proxies downloading

## Install

`pip3 install parqser`

## Simple example

This code scrapes given URLs in multithread mode and writes the length of html code in it to csv
```
from parqser.scrapper import BatchParallelScrapper
from parqser.parser import HTMLParser
from parqser.saver import CSVSaver
from parqser.web_component import BaseComponent


class CodeLength(BaseComponent):
    def parse(self, source: str) -> int:
        return len(source)


if __name__ == '__main__':
    urls = ['https://github.com',
            'https://github.com/mlsect-dojo',
            'https://github.com/GroupLe',
            'https://github.com/GroupLe/grouple-face-tagger',
            'https://github.com/GroupLe/grouple-face-tagger/actions']

    saver = CSVSaver('./parsed_info.csv')
    parser = HTMLParser([CodeLength()])
    scrapper = BatchParallelScrapper(n_jobs=2, interval_ms=1000)

    for url_batch in scrapper.batch_urls(urls):
        loaded = scrapper.load_pages(url_batch)

        print(' '.join([page.status.name for page in loaded]))
        parsed = [parser.parse(page) for page in loaded]
        parsed = [page.to_dict() for page in parsed]

        saver.save_batch(parsed)
``` 

## Exmaples

- launch simple exmaple like in `example/simple`
- Authenticate to account and parqse your private data with custom sessions like in `examples/authenticated_session`
- Subclass and define your own savers, components, scrappers, sessions and parsers
