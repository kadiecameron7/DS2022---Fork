# Working with JSON Data

JSON (JavaScript Object Notation) is the most common format for exchanging data between APIs, apps, and data pipelines. In this short in-class activity you will:

1. Inspect and filter local JSON files with `jq`
2. Filter saved CoinMarketCap JSON responses with `jq`
3. Parse the same kind of data in Python

**Time:** about 20 minutes — **`jq` ~10 min** (Exercises 1–2), then **Python ~10 min** (Exercise 3). Work from this directory:

```bash
cd class/05-data
```

Sample files live in [`data/`](data/). Full practice kit (optional later): [nmagee/json-practice](https://github.com/nmagee/json-practice/).

---

## Setup

You should already have `uv` (Lab 03) and `jq` ([course setup](../../setup/GENERAL.md)). Confirm both:

```bash
jq --version
python3 -V
uv --version
```

### If `jq` is missing

`jq` is a small standalone command-line tool. Package managers are the usual install path, but **Homebrew often runs a slow self-update before `brew install`**, which is painful in class. Prefer these in order:

**1. Ubuntu / WSL (`apt`) — usually fast:**

```bash
sudo apt-get install -y jq
```

(Skip a full `apt update` unless `apt-get` cannot find the package.)

**2. macOS — Homebrew without the auto-update:**

```bash
HOMEBREW_NO_AUTO_UPDATE=1 brew install jq
```

**3. Download the binary (no package manager):** grab the latest release for your OS from [jqlang/jq releases](https://github.com/jqlang/jq/releases), make it executable, and put it on your `PATH` (for example `~/bin`). Details: [jq download](https://jqlang.github.io/jq/download/).

**In-class fallback:** if install is stuck, use [jqplay](https://jqplay.org/) in the browser for Exercise 1 (paste the JSON from `data/`), then return to the terminal when `jq` is installed.

### Running Python with a temporary package (`--with`)

In Lab 03 you used `uv init` / `uv add` to build a real project (`pyproject.toml`, `uv.lock`, `.venv`). For this short in-class activity you do **not** need that.

`uv run --with <package>` installs the package just for **that one command**. `uv` downloads it into a cache, makes it importable while the script runs, then you are done. It does **not** create a project, write `pyproject.toml` / `uv.lock`, or leave a `.venv` in this folder.

```bash
uv run book_parse.py
uv run crypto_fetch.py
uv run --with requests crypto_fetch_api.py
```

`book_parse.py` and `crypto_fetch.py` only need Python's built-in `json` module, so plain `uv run` is enough. `crypto_fetch_api.py` needs `requests`, so add `--with requests` for that one command.

Use `uv add` later when a package should be a lasting dependency of a project. Use `--with` for one-off classroom scripts like these. More detail: [Try a package once with `uv run --with`](../03-scripting/README.md#try-a-package-once-with-uv-run---with).

Useful playgrounds if you get stuck:

- [jqplay](https://jqplay.org/) — paste JSON and try filters live
- [JSONLint](https://jsonlint.com/) — validate / pretty-print JSON

---

## Warmup: JSON vs XML

Same menu as JSON:

```json
{
  "menu": {
    "id": "file",
    "value": "File",
    "popup": {
      "menuitem": [
        {"value": "New", "onclick": "CreateNewDoc()"},
        {"value": "Open", "onclick": "OpenDoc()"},
        {"value": "Close", "onclick": "CloseDoc()"}
      ]
    }
  }
}
```

Same idea as XML:

```xml
<menu id="file" value="File">
  <popup>
    <menuitem value="New" onclick="CreateNewDoc()" />
    <menuitem value="Open" onclick="OpenDoc()" />
    <menuitem value="Close" onclick="CloseDoc()" />
  </popup>
</menu>
```

JSON maps cleanly to Python dicts and lists. That is why web APIs often use it.

Peek at the local copy:

```bash
cat data/simple.list.json | jq .
```

---

## Exercise 1 — `jq` on local files

Spend about **10 minutes** on Exercises 1–2 together (local `jq`, one agent prompt, then the CoinMarketCap sample files). Skip optional parts if you run short.

`jq` reads JSON and prints filtered text. `-r` means "raw" (no quotes around strings).

### 1a. Nested object

`data/simple.single.json` is a nested glossary.

Print the entire data set:
```bash
cat data/simple.single.json | jq -r .
```

Print the glossary title:

```bash
cat data/simple.single.json | jq -r '.glossary.title'
```
Note how the nested keys `glossary` > `title` are chained with a `.` -> `.glossary.title`.

**Try:** print the acronym (`SGML`).

<details>
<summary>Hint: add the deeper level keys to the dot chain</summary>

```bash
cat data/simple.single.json | jq -r '.glossary.GlossDiv.GlossList.GlossEntry.Acronym'
```

</details>

### 1b. Book fields and an array

`data/book.json` is a single object:

```bash
cat data/book.json | jq -r '.title'
cat data/book.json | jq -r '.author'
cat data/book.json | jq -r '.genres[]'
```

**Try:** print only the first genre (`.genres[0]`).

### 1c. Array of objects

`data/employees.json` has an `employees` array. List every name:

```bash
cat data/employees.json | jq -r '.employees[].name'
```

**Try:** print only the `position` for the second employee (`.employees[1].position`).

### 1d. Put your agent to work

You can ask [Cursor Agent](https://cursor.com/docs/agent/overview) to write or fix `jq` filters for you. Treat it like a teammate: point it at the file, say what you want out of the JSON, and review the command before you trust it.

**How to use it (quick):**

1. Open the **Agent** panel in Cursor ([docs](https://cursor.com/help/ai-features/agent)):
   - **macOS:** `Cmd+I`
   - **Windows / Linux:** `Ctrl+I`
   - Or use the Command Palette (`Cmd+Shift+P` / `Ctrl+Shift+P`) and search for **Agent**.
   - If the panel opens in Chat/Ask mode, switch the mode dropdown to **Agent** (or press `Shift+Tab` to cycle modes).
2. **WSL:** Keep using the Cursor app on Windows (Remote – WSL). Agent shortcuts are still the **Windows** ones (`Ctrl+I`), not Linux terminal shortcuts. Open the folder inside WSL so `@data/...` paths match your Linux files; run `jq` / `uv` in the WSL terminal.
3. Attach context with `@` — for example `@data/employees.json` or `@data/book.json` — so the agent can see the real structure.
4. Ask for a concrete result (a field, a list, a filter). Prefer “give me the `jq` command” over “just run everything.”
5. Read the suggested command. Run it in your own terminal (or approve the agent’s terminal run) and check the output against the file.

Good prompts are specific about the **file**, the **shape of the answer**, and the **tool** (`jq`).

**Example prompts** — try **one** of these (paste into Agent; adjust names as you like):

```text
@data/employees.json show me jq command to get list of all keys
```

```text
@data/simple.single.json Write a jq command that prints the GlossEntry Acronym.
Explain the filter path in one sentence.
```

```text
@data/book.json Give me a jq one-liner that prints only the first genre.
Then give a second command that prints every genre on its own line.
```

```text
@data/employees.json I need jq to list each employee's name and position as "Name: role".
Show the command only — do not modify any files.
```

```text
@data/employees.json The filter `.employees[].name` works. Change it so I get only the
second employee's position. Explain the difference between [] and [1].
```

```text
I'm stuck on nested JSON. Using @data/simple.single.json, show me how to walk from
glossary down to GlossSeeAlso and print both SeeAlso strings with jq.
```

**Tip:** If the agent invents keys that are not in the file, reply with “re-read `@data/...` and use only keys that exist.” Agents are strong when the JSON is in context and weak when they guess the schema.

---

## Exercise 2 — CoinMarketCap sample JSON with `jq`

Pipe JSON into `jq` the same way as in Exercise 1. The files below are **saved responses** from [CoinMarketCap](https://coinmarketcap.com/api/documentation/pro-api-reference/keyless-public-api) (cryptocurrency prices). Use these in class so dozens of students are not blocked when the public API rejects too many requests from the same network.

Optional live requests (may fail in class with HTTP `403` or `429` — too many requests from a shared network):

```bash
curl -s "https://pro-api.coinmarketcap.com/public-api/v1/simple/price?ids=1,1027&convert=USD" | jq .
```
```bash
curl -s "https://pro-api.coinmarketcap.com/public-api/v3/cryptocurrency/listings/latest?limit=5&convert=USD" | jq .
```

If you get `403` or `429` errors, do not worry. Try again later outside class, or continue with `data/cmc_simple_price.json` and `data/cmc_listings.json` — they use the same structure as the live API responses.

### 2a. Nested object — cryptocurrency prices

CoinMarketCap numeric ids: `1` = Bitcoin, `1027` = Ethereum. Sample file: [`data/cmc_simple_price.json`](data/cmc_simple_price.json).

```bash
cat data/cmc_simple_price.json | jq .
```

Pull just Bitcoin's USD price:

```bash
cat data/cmc_simple_price.json | jq -r '.data[] | select(.id == 1) | .price'
```

**Try:** print Ethereum's USD price (select `.id == 1027`).

### 2b. Array of objects — top coins by market capitalization

Sample file: [`data/cmc_listings.json`](data/cmc_listings.json) (10 coins). Each coin's US dollar price fields are under `.quote[0]` (an array), not `.quote.USD`.

```bash
cat data/cmc_listings.json | jq -r '.data[].name'
```

Build smaller objects with name, price, and 24-hour percent change:

```bash
cat data/cmc_listings.json \
  | jq '[.data[] | {name, price: .quote[0].price, change_24h: .quote[0].percent_change_24h}]'
```

**Try:** keep only the first five coins (`.data[:5]`), or filter to coins whose price is above 100:

```bash
cat data/cmc_listings.json \
  | jq '[.data[] | select(.quote[0].price > 100) | {name, price: .quote[0].price}]'
```

### 2c. (Optional) Foreign currency exchange rates or local weather

USD to EUR / GBP / JPY ([Frankfurter](https://frankfurter.dev/)):

```bash
curl -s "https://api.frankfurter.dev/v1/latest?base=USD&symbols=EUR,GBP,JPY" | jq .
curl -s "https://api.frankfurter.dev/v1/latest?base=USD&symbols=EUR,GBP,JPY" | jq -r '.rates.EUR'
```

Current weather in Charlottesville ([Open-Meteo](https://open-meteo.com/); no API key required):

```bash
curl -s "https://api.open-meteo.com/v1/forecast?latitude=38.03&longitude=-78.48&current=temperature_2m,wind_speed_10m" \
  | jq '.current'
```

---

## Exercise 3 — Python (~10 min)

### 3a. Read a local file

Open [`book_parse.py`](book_parse.py) (or run the same code interactively in Python):

```python
import json

with open("data/book.json", "r") as f:
    data = json.load(f)

print(data["title"])
print(data["author"])
for genre in data["genres"]:
    print(genre)
```

Run it:

```bash
uv run book_parse.py
```

**Try:** load `data/employees.json` and print each employee's `name` and `position`.

<details>
<summary>Sample solution</summary>

```python
import json

with open("data/employees.json", "r") as f:
    data = json.load(f)

for emp in data["employees"]:
    print(f"{emp['name']}: {emp['position']}")
```

</details>

### 3b. Load a CoinMarketCap sample file

Open [`crypto_fetch.py`](crypto_fetch.py) — it reads the same CoinMarketCap sample used in Exercise 2:

```python
import json

with open("data/cmc_listings.json", "r") as f:
    data = json.load(f)

for coin in data["data"][:5]:
    quote = coin["quote"][0]
    print(f"{coin['name']}: ${quote['price']:.2f} ({quote['percent_change_24h']:.2f}%)")
```

```bash
uv run crypto_fetch.py
```

### 3c. (Optional) Fetch live JSON with `requests`

Outside class (or if the classroom network allows it), [`crypto_fetch_api.py`](crypto_fetch_api.py) downloads the same listings from CoinMarketCap:

```python
import requests

url = "https://pro-api.coinmarketcap.com/public-api/v3/cryptocurrency/listings/latest"
params = {"limit": 5, "convert": "USD"}
response = requests.get(url, params=params, timeout=10)
response.raise_for_status()

for coin in response.json()["data"]:
    quote = coin["quote"][0]
    print(f"{coin['name']}: ${quote['price']:.2f} ({quote['percent_change_24h']:.2f}%)")
```

```bash
uv run --with requests crypto_fetch_api.py
```

`--with requests` installs `requests` for this one command only (see [Running Python with a temporary package](#running-python-with-a-temporary-package---with)).

If this script fails with HTTP `403` or `429` (too many requests on a shared network), use `crypto_fetch.py` and the files in `data/` instead.

**Try:** change the script to download JSON from Frankfurter, then print each currency code and rate from `data["rates"]`.

### 3d. (Optional) Write JSON out

```python
import json

rows = [
    {"repo_name": "json-practice", "repo_url": "https://github.com/nmagee/json-practice/"},
    {"repo_name": "DS2022", "repo_url": "https://github.com/ksiller/DS2022"},
]
print(json.dumps(rows, indent=2))
```

---

## Checkpoint

You should be able to:

| Skill | Tool |
| --- | --- |
| Pretty-print / dig into nested keys | `jq '.path.to.field'` |
| Iterate arrays | `jq '.[].name'` or Python `for item in data:` |
| Load a file | `json.load(...)` |
| Filter CoinMarketCap sample JSON | `jq` on `data/cmc_*.json` (optional live `curl`) |

---

## Resources

- [JSON Introduction (MDN)](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Objects/JSON)
- [jq manual](https://jqlang.github.io/jq/manual/)
- [jqplay](https://jqplay.org/)
- [JSONLint](https://jsonlint.com/)
- [nmagee/json-practice](https://github.com/nmagee/json-practice/) : longer jq + Python drills
- [CoinMarketCap Public API](https://coinmarketcap.com/api/documentation/pro-api-reference/keyless-public-api) : cryptocurrency prices; class uses saved samples in `data/`
- [Frankfurter](https://frankfurter.dev/) : European Central Bank foreign-exchange rates as JSON
- [Open-Meteo](https://open-meteo.com/) : weather forecast API (no API key required)
