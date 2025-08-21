{ pkgs }: {
  deps = [
    pkgs.python39
    pkgs.python39Packages.pip
    pkgs.python39Packages.requests
    pkgs.python39Packages.beautifulsoup4
    pkgs.python39Packages.feedparser
    pkgs.python39Packages.aiohttp
    pkgs.python39Packages.pandas
    pkgs.python39Packages.openai
    pkgs.python39Packages.python-dotenv
    pkgs.python39Packages.lxml
    pkgs.python39Packages.newspaper3k
    pkgs.python39Packages.nltk
    pkgs.python39Packages.schedule
  ];
}
