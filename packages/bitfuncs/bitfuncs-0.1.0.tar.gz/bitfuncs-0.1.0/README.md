# BitFuncs

Some async funcs for trading.

## Install

```bash
(pyenv)$ pip install bitfuncs
```

## Migrate

```bash
(pyenv)$ ASYNCSQL_SQL_DIR=bitfuncs/sql python -m asyncsql.migrate schema_0.1.0
```

## Run Backtest

```bash
(pyenv)$ chamallow examples/crypto_backtest.yml
```

## Get Some Results

Best found params and position status as json:

```bash
$ cat var/BTC.json
{
  "macd_fastperiod": 16.0,
  "macd_slowperiod": 30.0,
  "macd_signalperiod": 11.0,
  "position": "none"
}
```

## Backtesting html page

```bash
$ xdg-open var/BTC.html
.
```

## License

MIT
