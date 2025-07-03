🌐 **speed_test – Pomiar prędkości Internetu**

Szybki test pobierania, wysyłania i pinga. Wymaga narzędzia `speedtest`
(Ookla) lub modułu `speedtest-cli` (instaluje się automatycznie przy
pierwszym uruchomieniu).

#### Opcje
| opcja | opis |
|-------|------|
| `--json`        | Zwróć surowy JSON |
| `--only` dl/ul/ping | Pokaż tylko jeden parametr |
| `--lang-help`   | Pokaż pomoc PL / ENG |

```bash
shellman speed_test                 # wszystkie metryki
shellman speed_test --only ping     # tylko ping
shellman speed_test --json          # do dalszego przetwarzania
```
