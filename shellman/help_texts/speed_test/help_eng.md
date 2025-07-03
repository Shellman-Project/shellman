🌐 **speed_test – Internet Speed Measurement**

Run a quick download/upload/ping test. Requires either the Ookla `speedtest`
binary on PATH *or* the pure-python `speedtest-cli` package (installed
automatically on first run).

#### Options
| option | description |
|--------|-------------|
| `--json`        | Print raw JSON result |
| `--only` dl/ul/ping | Show a single metric |
| `--lang-help`   | Show help in Polish / English |

shellman speed_test                 # all metrics
shellman speed_test --only ping     # just ping
shellman speed_test --json          # machine-readable
