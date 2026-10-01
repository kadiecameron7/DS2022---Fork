# NoSQL Databases

The goal of this activity is to familiarize you with NoSQL database systems. These databases are essential for handling unstructured data, scaling horizontally, and working with modern application architectures that require flexible data models. The primary focus is MongoDB. The sections on Redis and DynamoDB are optional. 

## MongoDB

MongoDB helped popularize the NoSQL approach and remains a favorite choice among many developers because of its speed and relative simplicity.

**Insert/update data:**
You typically pass data as **JSON** (human-readable text). MongoDB stores each item as a **document** in a **collection**, using **BSON** (Binary JSON) on disk; BSON is a binary encoding of the same JSON-like structure. Do not confuse collections with SQL tables or documents with table rows (“records”): a collection is a group of documents, and each document is a self-contained JSON-like object. We refer to nested JSON objects inside documents as **subdocuments**. Documents in the same collection need not share the same fields or structure (no fixed schema by default).

**Retrieve data:**
Queries reverse that path. In `mongosh` you write **JavaScript** that includes human-readable **JSON-like** filters (for example `{ year: 2000 }`). MongoDB matches those filters against **BSON** documents in the collection, then converts the matches and returns them as **JSON** in the shell (or you can write that JSON out to a file).

![MongoDB Documents](https://media.geeksforgeeks.org/wp-content/uploads/20200726190757/subtractdatabase-648x660.jpg)

MongoDB lets you store different document shapes in the same collection, with a maximum of 16MB per document. Frequently accessed documents can be kept in memory for fast reads.

MongoDB's strongest features for data science are:

* Simple to use for storing varied datasets.
* Popularity in the community.
* Can be run locally, on a server, or in the cloud.
* Returns results quickly.

<a href="https://www.mongodb.com/" target="_blank" rel="noopener noreferrer"><strong>Learn more about MongoDB</strong></a>

## Set up your own MongoDB Atlas Cluster in the Cloud

This course will be using MongoDB Atlas, a cloud-based Mongo service, for hands-on exercises. Follow the [MongoDB Setup instructions](../../setup/mongodb.md).

## Viewing MongoDB in Cursor

You can browse databases, collections, and documents inside Cursor (or VS Code) instead of only using `mongosh`.

1. In [MongoDB Atlas](https://cloud.mongodb.com/), open your cluster and click **Connect**.
2. Choose **MongoDB for VS Code** and copy the connection string. It looks like:

```text
mongodb+srv://YOUR_USERNAME:<db_password>@YOUR_CLUSTER.mongodb.net/
```

3. In Cursor, go to **File** > **New Text File** and paste the connection string into it. Replace `<db_password>` with your real Atlas password (keep the rest of the string). Save that string for the next step.
4. Install **[MongoDB for VS Code](https://marketplace.visualstudio.com/items?itemName=mongodb.mongodb-vscode)** (`mongodb.mongodb-vscode`) from the Extensions view (`Cmd+Shift+X` / `Ctrl+Shift+X`).
5. Open the MongoDB sidebar (leaf icon) → **Add Connection** → **Connect with Connection String**. Paste the string from step 3 and press Enter.
6. Expand the connection to browse databases such as `sample_mflix` and `mypractice`, open collections, and inspect documents.


## In-class exercises

### Sync your local repo

Pull the latest course materials (including new examples and sample files for this activity) before you start. Follow the [Weekly sync](../../README.md#weekly-sync) steps.

### The `mongosh` CLI tool

`mongosh` is the MongoDB shell: a command-line program you use to connect to Atlas and run database commands interactively.

If you don't have it installed yet, follow [MongoDB Setup](../../setup/mongodb.md), then confirm:

```bash
mongosh --version
```

**1. Open a terminal** in Cursor (or your usual shell). On Windows, use a **WSL** terminal so `mongosh` and your Atlas environment variables match the Linux setup from the course docs.

**2. Go to this activity folder** before you start `mongosh`. File paths later in the lab (for example `data/fruit.json`) are relative to this directory:

```bash
cd class/05-nosql
```

**3. Confirm** your Atlas environment variables:
```bash
printenv | grep -i "mongo"
```

**Example:**
```text
MONGODB_ATLAS_URL=mongodb+srv://ds2022.tmwdrjn.mongodb.net/
MONGODB_ATLAS_USER=mst3k            
MONGODB_ATLAS_PWD=Pz8MvcN2apydHSZUq
```
The values of your url, username, and password will be different. **If you don't have these environment variables set, go back to [Get Connection String](../../setup/mongodb.md#3-get-connection-string-url) and [Save Connection String](../../setup/mongodb.md#4-save-connection-string).**

**4. Connect**

Use the connection string from [MongoDB Setup](../../setup/mongodb.md) (the host below is only an example; **yours will differ**). If you set `MONGODB_ATLAS_*` in `~/.bashrc` / `~/.zshrc`, open a **new** terminal or run `source ~/.bashrc` (or `~/.zshrc`) first. Off campus, make sure your current IP is on the Atlas IP Access List.

```bash
mongosh "mongodb+srv://ds2002.tmwdrjn.mongodb.net/" --apiVersion 1 --username <username>
```
or, using the environment variables from setup:
```bash
mongosh "$MONGODB_ATLAS_URL" --apiVersion 1 --username "$MONGODB_ATLAS_USER"
```

You will be prompted for your password. Enter it.

You should now be connected to the MongoDB cluster in the cloud.
```
Current Mongosh Log ID: 699e58dc0ab4a093557db299
Connecting to:          mongodb+srv://<credentials>@ds2002.tmwdrjn.mongodb.net/?appName=mongosh+1.8.0
Using MongoDB:          8.0.19 (API Version 1)
Using Mongosh:          1.8.0

For mongosh info see: https://docs.mongodb.com/mongodb-shell/

Atlas atlas-ct3ynp-shard-0 [primary] test>
```

Congrats, you're logged in to the Atlas cluster and you're ready to explore the CLI. Stay in `mongosh` for the exercises below. When you are ready for Python later, see [Exiting `mongosh`](#exiting-mongosh).

**5. Explore the `sample_mflix` database**

Most `mongosh` commands use JavaScript syntax: objects, methods, and **dot chaining** to call methods in sequence (e.g. `db.movies.find().limit(3)`). Semicolons are optional; the examples in this lab omit them.

List all databases:
```javascript
show dbs
```
You should see this list, and possibly a few other databases:
```
sample_mflix  174.90 MiB
admin         356.00 KiB
local          12.63 GiB
```

If you don't see the `sample_mflix` database, [load Atlas sample data](https://www.mongodb.com/docs/atlas/sample-data/).

**Select database and show collections**
Now, let's switch to the `sample_mflix` database and show all its collections.
```javascript
use sample_mflix
```
Note the change of your prompt to `Atlas ... sample_mflix>` indicating the active database.

```javascript
show collections
```

Output of available collections:
```
comments
embedded_movies
movies
sessions
theaters
users
```

**Find documents**

```javascript
db.movies.findOne()
db.movies.find().limit(3)
```

- `findOne()` returns a single document.
- With no filter (or several matches), that document is in **natural order** (roughly the first the server finds).
- Use a filter and/or `sort` when you need a specific document (see [Search with filters](#search-with-filters)).
- `find()` returns a **cursor** (a handle to zero or more matching documents).
- Current `mongosh` already prints cursor results as indented JSON, so `.pretty()` usually makes no visible difference.
- `.pretty()` is optional here; older tutorials still use it. Not every method supports it (do not chain it after `findOne()` or `countDocuments()`).

**Count and sort**

```javascript
db.movies.countDocuments()
db.movies.find().sort({ year: 1 }).limit(5)
db.movies.find().sort({ year: -1 }).limit(5)
```

- `countDocuments()` returns how many documents are in the collection.
- `.sort({ year: 1 })` orders by `year` ascending (`1`); use `-1` for descending.
- `.limit(5)` keeps only the first five results after sorting.

### Search with filters

The first argument to `find()` is the **filter** (which documents to return):

- Plain value: equality (e.g. `{ year: 1994 }`).
- `$gt`, `$lt`, `$gte`, `$lte`, `$ne`: comparisons.
- `$or` with an array: match any of several conditions.

**Equality** (movies from 1994):

```javascript
db.movies.find({ year: 1994 }).limit(3)
```

**Comparison** 

movies after 2000:
```javascript
db.movies.find({ year: { $gt: 2000 } }).limit(3)
```

**logical OR** 
movies from 1999 or 2000:
```javascript
db.movies.find({ $or: [ { year: 1999 }, { year: 2000 } ] }).limit(3)
```

### Project only some fields

The second argument to `find()` is a **projection** (which fields to return):

- `1` includes a field.
- `_id: 0` omits the default `_id` (included unless you turn it off).

Example: movies from 2000, returning only `title` and `year`:

```javascript
db.movies.find({ year: 2000 }, { title: 1, year: 1, _id: 0 }).limit(5)
```

**Try:** modify the command to return only `title`, `genres`, and `directors`. Non-existent field names are ignored without an error.

### More Operators

* **Comparison Operators** ($eq, $ne, $gt, $lt, $gte, $lte, $in): Filter documents by comparing field values.

* **Logical Operators** ($and, $or, $nor, $not): Combine or invert query conditions.

* **Update Operators** ($set, $inc, $unset, $push): Modify documents, such as changing, incrementing, or adding field values.

* **Array Operators** ($all, $size, $elemMatch): Query and manipulate data within array fields.

* **Evaluation Operators** ($regex, $text, $where): Enable complex searches, including pattern matching and full-text searches.
  
### Iterators with Functions

Use `.forEach()` to run a function over each document in the result. Example: print a field with a custom prefix (using the `sample_mflix` database):

```javascript
db.movies.find({ year: 2000 }).limit(3).forEach(function(doc) {
  print("Movie: " + doc.title + " (" + doc.year + ")")
})
```
Output:
```
Movie: In the Mood for Love (2000)
Movie: State and Main (2000)
Movie: April Captains (2000)
```

**Try:** update the `find().sort().forEach()` chain to find movies from years 2012-2016, sort by year (most recent to oldest) then title (ascending), with no limit, and print each line in this format:

```text
Movie: Some Title (2016), directors: Name One, Name Two
Movie: Another Title (2015), directors: Name Three
...
```

`sample_mflix` can contain more than one document with the same title (different `_id`s). That is expected; you are iterating documents, not unique titles.

<details>
<summary>Sample solution</summary>

```javascript
db.movies.find({ year: { $gte: 2012, $lte: 2016 } }).sort({ year: -1, title: 1 }).forEach(function(doc) {
  const directors = (doc.directors || []).join(", ")
  print("Movie: " + doc.title + " (" + doc.year + "), directors: " + directors)
})
```

- `.sort({ year: -1, title: 1 })` sorts by year descending, then by title ascending within the same year.
- `directors` is an array in `sample_mflix`; `.join(", ")` turns it into a readable string.

</details>

### Join related collections

Related data often lives in **different collections**. Instead of copying a whole movie into every comment, `sample_mflix` stores a **reference**: each comment has a `movie_id` field whose value is the `_id` of a document in `movies`.

The `text` on comments is **synthetic sample data** (placeholder prose, not real reviews). Use it to practice references and joins; do not treat the wording as authentic content.

This is not a SQL `JOIN`. You either look up the related document yourself, or use aggregation `$lookup` (MongoDB's server-side join).

**Start from a movie students know**, then find one of its comments (stay in `sample_mflix`):

```javascript
use sample_mflix
const movie = db.movies.findOne({ title: "The Godfather" }, { title: 1, year: 1 })
movie
const comment = db.comments.findOne({ movie_id: movie._id }, { name: 1, text: 1, movie_id: 1 })
comment
```

- `comment.movie_id` is an `ObjectId` that points at `movies._id` (here, The Godfather).

**Manual reference lookup** (follow the reference the other way: comment → movie):

```javascript
db.movies.findOne({ _id: comment.movie_id }, { title: 1, year: 1, _id: 0 })
```

- The filter uses the comment's `movie_id` as the movie `_id`.
- The projection returns only `title` and `year`.

**Server-side join with `$lookup`** (several comments on that same movie):

```javascript
db.comments.aggregate([
  { $match: { movie_id: movie._id } },
  { $limit: 3 },
  { $lookup: {
      from: "movies",
      localField: "movie_id",
      foreignField: "_id",
      as: "movie"
  }},
  { $project: { name: 1, text: 1, "movie.title": 1, "movie.year": 1, _id: 0 } }
])
```

- `$match` restricts to comments for The Godfather.
- `$lookup` matches `comments.movie_id` to `movies._id` and stores matches in an array field named `movie` (usually one element).
- `$project` keeps selected comment fields plus the joined movie title and year.
- Some other comments in `sample_mflix` have a `movie_id` with no matching movie (`movie: []`). That is an orphaned reference.

**Try:** change `{ title: "The Godfather" }` to another film that has comments (for example `"The Matrix"` or `"Pulp Fiction"`), or project `movie.genres` instead of `movie.year`. Some well-known titles in `sample_mflix` have **zero** comments (for example `"Casablanca"`); for those, `findOne` on comments returns `null` and the join steps will not work until you pick a title with comments.

**Embed the other way (movie root, comments array):** see [`09-mongo_embed.py`](09-mongo_embed.py). That script builds one document with The Godfather as the root and all of its comments nested under `comments`, then inserts it into `mypractice.movies_with_comments`.

### Create Operations

Let's switch gears and create your own database and collection in the Atlas Cluster. Insert operations add new documents to a collection. If the collection does not exist, MongoDB creates it. 

**Create a database and collection.** Switch to a new database; the collection is created when you first insert into it.

```javascript
use mypractice
```

**Insert one document** (`insertOne`). Use a simple document structure (e.g. `name` and `quantity`).

```javascript
db.fruit.insertOne({ name: "apple", quantity: 5 })
```
This creates a new collection `fruit` and inserts a new document into it. Let's confirm:

```javascript
show collections
db.fruit.find()
```
Output:
```
[
  {
    _id: ObjectId("699e8ab1ffd8068edd5647c6"),
    name: 'apple',
    quantity: 5
  }
]
```

Note the automatic creation of the `_id` field, containing a unique identifier for your new document.  

**Insert multiple documents** (`insertMany`). Pass an array of documents.

```javascript
db.fruit.insertMany([
  { name: "banana", quantity: 10 },
  { name: "orange", quantity: 3 }
])
```

Verify with `db.fruit.find()`. See *Read Operations* below for querying.

### Read Operations

Using the `mypractice` database and `fruit` collection from above:

```javascript
db.fruit.find()
db.fruit.findOne({ name: "apple" })
db.fruit.find({ quantity: { $gte: 5 } })
```

### Update Operations

Update one document with `updateOne`. The first object is the filter (which documents to update); the second uses `$set` to specify which field(s) to update and to what value(s). 

```javascript
db.fruit.updateOne({ name: "apple" }, { $set: { quantity: 8 } })
```

Update multiple documents with `updateMany`.
```javascript
db.fruit.updateMany({ quantity: { $lt: 10 } }, { $set: { restocked: true } })
db.fruit.find()
```

- Only documents matching `{ quantity: { $lt: 10 } }` get a `restocked` field (strictly less than 10, so a document with `quantity: 10` is unchanged).
- Other documents simply have no `restocked` field. **That uneven shape is normal in MongoDB: documents in a collection need not share the same fields.**

### Delete Operations

Remove documents with `deleteOne` (one match) or `deleteMany` (all matches). Use a filter to limit what is removed.

```javascript
db.fruit.deleteOne({ name: "apple" })
db.fruit.find()
```

You can use the same filter styles as in [Search with filters](#search-with-filters). Example with `$or`:

```javascript
db.fruit.deleteMany({ $or: [ { name: "orange" }, { name: "apple" } ] })
```

- `$or` takes an **array** of conditions; each condition is its own object.
- This deletes every document whose `name` is `"orange"` or `"apple"`.
- Equivalent shorter form: `{ name: { $in: ["orange", "apple"] } }`.
- The command result includes `deletedCount`, indicating how many documents were removed.

### Delete a collection

`deleteOne` / `deleteMany` remove **documents**. To remove the whole **collection** (all documents plus the collection itself), use `drop()`:

```javascript
use mypractice
show collections
db.fruit.drop()
show collections
```

- `db.fruit.drop()` deletes the `fruit` collection from the current database.
- The result is typically `true` if the collection existed and was dropped, or `false` if it did not exist.
- After a drop, `show collections` no longer lists `fruit`. Inserting again (for example in [Insert from file](#insert-from-file)) recreates the collection.

### Insert from file

So far you typed documents into the shell. You can also load JSON from a file (exports, downloads, or lab sample files).

Sample file: [`data/fruit.json`](data/fruit.json) (a JSON **array** of documents, ready for `insertMany`).

**1.** Still inside `mongosh`, confirm the file is visible from your current working directory:

```javascript
fs.existsSync("data/fruit.json")
```

- `true`: continue to step 2.
- `false`: you started `mongosh` from the wrong folder. Run `exit`, then in bash/zsh:

```bash
cd class/05-nosql
```

Reconnect with `mongosh` as before, and check `fs.existsSync("data/fruit.json")` again.

**2.** Insert the file into the `fruit` collection:

```javascript
use mypractice
const docs = JSON.parse(fs.readFileSync("data/fruit.json", "utf8"))
db.fruit.insertMany(docs)
db.fruit.find()
```

- `fs.readFileSync(...)` reads the file text from disk.
- `JSON.parse(...)` turns that text into an array of documents.
- `insertMany(docs)` writes those documents into `fruit`. If `fruit` does not exist yet, MongoDB creates the collection on this insert.
- Paths are relative to the directory where you launched `mongosh` (that is why step 1 matters).

### Exiting `mongosh`

Before you run the Python scripts, leave the MongoDB shell and return to bash/zsh:

```text
exit
```

- Type `exit` at the `mongosh` prompt (or press Ctrl+D).
- Your prompt should look like a normal shell again (`$` or `%`), not `Atlas ...>`.
- Confirm you are still in `class/05-nosql` with `pwd` before continuing.

### MongoDB + Python

**PyMongo** is the official MongoDB driver for Python. It lets you connect to Atlas, run the same insert / find / update / delete operations you used in the shell, and work with results as Python dicts and lists.

Manage the dependency with **`uv`** (same pattern as [class/03-scripting](../03-scripting/README.md) and [class/04-sql](../04-sql/README.md)), not `pip` or conda:

```bash
# lasting dependency in your course/lab project
uv add pymongo

# or one-off, without adding to a project
uv run --with pymongo python -c "import pymongo; print(pymongo.__version__)"
```

- All scripts below use the same Atlas env vars as `mongosh` (`MONGODB_ATLAS_URL`, `MONGODB_ATLAS_USER`, `MONGODB_ATLAS_PWD`). 
- Confirm they are set (`echo $MONGODB_ATLAS_USER`) before running. 
- Confirm that you are in `class/05-nosql` (execute `pwd`; the returned path should end with that).

**Shared connection:** [`database.py`](database.py) builds a shared `client`, `db` (`mypractice`), and `fruit` collection. [`02-mongo_setup.py`](02-mongo_setup.py) imports that module; the other scripts open their own client with the same env vars.

Shell and Python both use `mypractice.fruit` and the same starter names (apple, banana, orange). The **update/delete targets differ** so the Python scripts still change visible data if you already finished the mongosh exercises (mongosh: update/delete **apple**; Python: update **banana** / **orange**, delete **orange**).

**Numbered scripts (run in order 01 → 09):**

| Script | Purpose |
|--------|---------|
| [`01-sample_mflix.py`](01-sample_mflix.py) | Connect to `sample_mflix`, list collections and document counts |
| [`02-mongo_setup.py`](02-mongo_setup.py) | Use shared client from `database.py`; show server version, databases, and `mypractice` collection counts |
| [`03-mongo_create.py`](03-mongo_create.py) | Create `mypractice` / `fruit` and insert sample documents (apple, banana, orange) |
| [`04-mongo_read.py`](04-mongo_read.py) | Read documents: find one, find banana, count |
| [`05-mongo_update.py`](05-mongo_update.py) | Update banana quantity and set orange `restocked` (not the mongosh apple path) |
| [`06-mongo_delete.py`](06-mongo_delete.py) | Delete orange and show remaining |
| [`07-mongo_summary.py`](07-mongo_summary.py) | Log a final summary of `mypractice` collections and `fruit` |
| [`08-mongo_join.py`](08-mongo_join.py) | Join `comments` to `movies` via `movie_id` (`sample_mflix`; manual lookup and `$lookup`) |
| [`09-mongo_embed.py`](09-mongo_embed.py) | Embed comments into a movie document and save it in `mypractice.movies_with_comments` |

```bash
uv run --with pymongo 01-sample_mflix.py
uv run --with pymongo 02-mongo_setup.py
uv run --with pymongo 03-mongo_create.py
uv run --with pymongo 04-mongo_read.py
uv run --with pymongo 05-mongo_update.py
uv run --with pymongo 06-mongo_delete.py
uv run --with pymongo 07-mongo_summary.py
uv run --with pymongo 08-mongo_join.py
uv run --with pymongo 09-mongo_embed.py
```

If you already ran `uv add pymongo` in a project, plain `uv run 01-sample_mflix.py` (and so on) is enough. Scripts `08` and `09` use `sample_mflix` and do not depend on the `fruit` CRUD scripts (you can run them after `01`). Re-running `09` inserts another copy into `movies_with_comments` each time.

## Advanced Concepts (Optional)

### Redis

Think of Redis as an exceptionally fast, 2-column lookup table. It makes no use of schemas, relations, or indexes.

- The LEFT `key` column (metaphorically speaking) in a Redis DB stores keys. Keys can consist of any useful, unique identifier.
- The RIGHT `value` column in a Redis DB can consist of a variety of data types, such as strings, integers, lists, sets, hash tables, etc.

![Redis Data Types](https://keestalkstech.com/wp-content/uploads/2019/04/redis-data-structure-types1.jpeg)

Redis is "fast" despite its data storage capabilities being relatively large (the `value` half has a maximum capacity of 512MB),
while the database engine attempts to keep frequently-accessed data in memory for optimal return to requests.

Redis's strongest features for data science are:

1. Incredibly simple to use.
2. Stores large records.
3. Returns results quickly.
4. Useful for storing and retrieving lists, queues, tasks, items, orchestration, settings, etc.

<a href="https://redis.io/" target="_blank" rel="noopener noreferrer"><strong>Learn more about Redis</strong></a>

#### Run Redis & Connect

The fastest way to get started is via [Redis Cloud](https://redis.io/docs/latest/get-started/) without any local installation. [Register for Redis Cloud](https://redis.io/try-free/)

Local installation (optional): follow Redis’s install guides for [Linux](https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/install-redis-on-linux/), [macOS](https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/install-redis-on-mac-os/), or [Windows / WSL2](https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/install-redis-on-windows/).

#### Connect and Use Client Tools 

Once your Redis instance is running, connect to it using a client tool to issue commands manually. 

- **Redis CLI:** The command-line interface is a simple and powerful way to interact with Redis.
- **[Redis Insight](https://redis.io/insight/):** A visual client for creating, managing, and analyzing Redis data (including Redis Cloud).
- **IDE extension:** [Redis for VS Code](https://redis.io/docs/latest/develop/tools/redis-for-vscode/) also works in Cursor (Extensions marketplace; publisher **Redis**).

#### Redis Practice

1. List all keys:
```
KEYS *
```
2. Insert some keys using the firstnames and lastnames of people as keys and values:
```
SET jim ryan
SET tina fey
SET leonardo davinci
```
3. Fetch those values using their keys:
```
GET jim
GET leonardo
GET tina
```
4. Set 3 Key-Value pairs using integers as the value. Add expiration times in seconds:
```
SET counter1 10 EX 10 
SET counter2 472 EX 30 
SET counter3 984 EX 28 
```
Next retrieve these values by key, one by one. Repeat this process for the next minute. Can you continue to fetch these values?

5. Set up a counter and increment it. You can increment by any integer amount:
```
SET counter 1
INCRBY counter 5
INCRBY counter 5
INCRBY counter 5
GET counter
```
6. For more hands-on practice and advanced usage, see the <a href="https://redis.io/docs/develop/data-types/" target="_blank" rel="noopener noreferrer"><strong>Redis data types guide</strong></a> and <a href="https://redis.io/docs/" target="_blank" rel="noopener noreferrer"><strong>Redis docs</strong></a>. Pay particular
attention to commands like:

- `MSET` / `MGET` - setting multiple items
- `LPUSH` / `LSET` / `LRANGE` / `LREM` / `LPOP` - create and manage lists
- `ZADD` / `ZRANGE` / `ZREM` / `ZCOUNT` - create and manage sorted sets

### DynamoDB

Amazon DynamoDB is a key-value and document database that delivers single-digit millisecond performance at any scale. It's a fully managed, multi-region, multi-active, durable database with built-in security, backup and restore, and in-memory caching for internet-scale applications. DynamoDB can handle more than 10 trillion requests per day and can support peaks of more than 20 million requests per second.

DynamoDB's strongest features for data science are:

1. It "just works."
2. As a managed service there is nothing to provision or maintain.
3. Regardless of user requests it remains fast.
4. Scales to any load.

The maximum value of the `value` half of a row in DynamoDB is 400KB, which is considerably smaller than Redis or MongoDB.

#### DynamoDB Practice

For hands-on DynamoDB practice, use <a href="https://aws.amazon.com/dynamodb/getting-started/" target="_blank" rel="noopener noreferrer"><strong>AWS DynamoDB getting started</strong></a>.

## Resources

* <a href="https://www.ibm.com/think/topics/mongodb#1490489863" target="_blank" rel="noopener noreferrer">What is MongoDB</a>
* <a href="https://www.youtube.com/watch?v=5-tIfDCb-T4" target="_blank" rel="noopener noreferrer">Set up MongoDB Atlas</a>
* <a href="https://mongodb-devhub-cms.s3.us-west-1.amazonaws.com/Mongo_DB_Shell_Cheat_Sheet_1a0e3aa962.pdf" target="_blank" rel="noopener noreferrer">MongoDB CheatSheet</a>
* <a href="https://www.youtube.com/watch?v=ofme2o29ngU" target="_blank" rel="noopener noreferrer">MongoDB Crash Course</a>
* <a href="https://redis.io/docs/" target="_blank" rel="noopener noreferrer">Redis</a>
* <a href="https://aws.amazon.com/dynamodb/" target="_blank" rel="noopener noreferrer">DynamoDB</a>


