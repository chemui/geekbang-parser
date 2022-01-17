
Make htmls merged and transformed into a pdf.

## Preparation

1. Install Python dependencies
```shell
pip install beautifulsoup4
pip install lxml
```

2. Install `wkhtmltopdf`, which transforms html into pdf
```shell
brew install --cask wkhtmltopdf
```

## Usage
```shell
./main.py > out.html
wkhtmltopdf ./out.html Go语言核心36讲.pdf
```