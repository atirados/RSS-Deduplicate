# RSS-Deduplicate
RSS Parser that removes redundancy

## Requirements
Python feedparser: `pip install feedparser`

## Usage
For the single-thread version:
`./deduplicate.py [input_feed_list.tsv] [output_feed_list.tsv]`

For the multi-thread version:
`./dedup_concurrency.py [input_feed_list.tsv] [output_feed_list.tsv]`