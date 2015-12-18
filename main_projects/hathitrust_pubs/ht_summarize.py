from htpubsummarizer import HTPubSummarizer


def main():
    summarizer = HTPubSummarizer("ht_data.json")
    summarizer.summarize()


if __name__ == "__main__":
    main()
