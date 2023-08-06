# HDistill

HDistill is a Python CLI tool for exploring and parsing HTML

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install hdistill.

```bash
pip install hdistill
```

## Usage

```python
hdistill 'https://www.imdb.com/chart/top/?ref_=nv_mv_250' '//td[@class=\"titleColumn\"]/text() | //td[@class=\"titleColumn\"]//a/text() | //td[@class=\"titleColumn\"]//a/@title | //td[@class=\"titleColumn\"]//span[@class=\"secondaryInfo\"]/text()' 4 'Rank,Key People,Title,Year Released'
```

will output a list of the top 250 movies:

```
[   {   'Key People': 'Frank Darabont (dir.), Tim Robbins, Morgan Freeman',
        'Rank': '1.',
        'Title': 'The Shawshank Redemption',
        'Year Released': '(1994)'},
    {   'Key People': 'Francis Ford Coppola (dir.), Marlon Brando, Al Pacino',
        'Rank': '2.',
        'Title': 'The Godfather',
        'Year Released': '(1972)'},
    {   'Key People': 'Francis Ford Coppola (dir.), Al Pacino, Robert De Niro',
        'Rank': '3.',
        'Title': 'The Godfather: Part II',
        'Year Released': '(1974)'},
    {   'Key People': 'Christopher Nolan (dir.), Christian Bale, Heath Ledger',
        'Rank': '4.',
        'Title': 'The Dark Knight',
        'Year Released': '(2008)'},
    etc...
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
