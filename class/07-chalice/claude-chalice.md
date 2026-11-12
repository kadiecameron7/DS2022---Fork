# Understanding Chalice with Claude

Use Claude Code to understand what Chalice does, not just to get the app deployed. These prompts work for the [Chalice demo](README.md) (`textapp`) and for Part 2 of [Lab 07](https://github.com/ksiller/lab-07-ec2-lambda) (`book-analyzer`).

## Installing Claude and general resources

- [AI Coding Basics](https://github.com/uvasds-systems/ai-coding-basics): installing Claude Code, signing in with your UVA Anthropic account (`claude /login`), setting up a project, and checking your usage (`/usage`, `/stats`).
- [Coding with AI Tools](https://github.com/uvasds-systems/ai-coding-basics/blob/main/slides/coding-with-ai.pdf): slides.
- [Claude Code documentation](https://docs.claude.com/en/docs/claude-code/overview): the official guide, including installation and all commands.

## Start Claude Code in the right folder

Claude Code reads the files in the folder where you start it. Open a second terminal, so you can keep running your own commands in the first one.

For the Chalice demo, start in `chalice-demo/`, the folder with `pyproject.toml`, one level above the app folder `textapp/`:

```bash
cd ~/ds2022-fall2026/chalice-demo
claude
```

For Lab 07, start in the top folder of your cloned repository, the folder with `pyproject.toml`, one level above the app folder `book-analyzer/`:

```bash
cd ~/ds2022-fall-2026/lab-07-ec2-lambda
claude
```

The first time you start Claude Code in a folder, it asks whether you trust the files in this folder. Check that the path it shows is `chalice-demo` or `lab-07-ec2-lambda`, then choose **Yes**. Claude Code asks once per folder. Trust only folders you created yourself or cloned for this course: a trusted folder's settings and `CLAUDE.md` can tell Claude what to do.

In the lab repository, Claude Code reads `CLAUDE.md` and works as your teaching assistant: it explains and gives hints, but does not write the graded parts for you (the body of `analyze_new_book()`, your query function, and your answers in `KNOWLEDGE_CHECK.md`).

## Useful commands in Claude Code

| Command | What it does |
| --- | --- |
| `@` + file path | adds a file to your prompt, for example `Explain @textapp/app.py line by line` (in the lab: `@book-analyzer/app.py`) |
| `!` + command | runs a shell command in the session, so Claude sees its output, for example `! cd textapp && uv run chalice logs -n count_words` (in the lab: `! cd book-analyzer && uv run chalice logs -n analyze_new_book`) |
| **Esc** | stops Claude in the middle of an answer or a change |
| **Shift+Tab** | switches the mode; in plan mode, Claude explains what it would do without changing files |
| `/clear` | starts a fresh conversation, for example before you switch from the demo to the lab |
| `/help` | lists all commands |

## Prompts: understand the project

- "Explain what `chalice new-project` created in the app folder (`textapp/` or `book-analyzer/`) and what each file is for. Don't change anything."
- "What is the difference between `pyproject.toml` and `requirements.txt` in this project? Which one does Lambda use?"
- "Which files does `chalice deploy` upload to AWS, and which ones stay on my computer?"
- "Explain each setting in `.chalice/config.json`. Which ones would I see in the AWS Console, and where?"
- "Why does this app need `"manage_iam_role": false` in the AWS Academy Learner Lab?"

## Prompts: understand the handler

- "Explain `@app.on_s3_event` in `app.py`. What does it create in AWS when I run `chalice deploy`?"
- "My handler takes only `event`, but a Lambda handler takes `event` and `context`. Where does `context` go?"
- "What is in `event.bucket` and `event.key`? Show me the raw event dict that S3 sends, and where these two values come from."
- "How does Chalice build the Lambda function name from `config.json` and `app.py`? What would the name be with a stage `prod`?"
- "Compare `app.py` with a Lambda function created in the AWS Console. What does Chalice do for me?"

## Prompts: deploy, test, and debug

- "Before I run `uv run chalice deploy`, tell me what it will create or change in AWS."
- "My upload did not trigger the function. Give me the commands to check each step, from the S3 event notification to the function's log, one at a time."
- "Here is the output of `uv run chalice logs -n count_words`: [paste]. What is the cause? Explain it before you suggest a fix."
- "`chalice deploy` failed with: [paste]. Is this a problem in my code, in `.chalice/config.json`, or in the Learner Lab's permissions?"
- "Which AWS resources does `chalice delete` remove, and which ones do I have to delete myself?"

## Prompts: the optional exercises in the Chalice demo

- "I want a second handler that runs when a `.txt` file is deleted. Which event type do I need, and what can the handler still read about the deleted file?"
- "Why can a Lambda function that writes to the same bucket that triggers it run in an endless loop? How does a second bucket prevent it?"
- "Explain how `s3.put_object` saves the word count as a new object. What are `Bucket`, `Key`, and `Body`?"

## Prompts: Lab 07, Part 2

- "Why does my own code have to go into `chalicelib/`? What happens to files outside `app.py` and `chalicelib/`?"
- "Why does `requirements.txt` list `pymongo` but not `boto3`?"
- "Why does `book-analyzer` need 512 MB of memory and a 60-second timeout, when the demo works with the defaults?"
- "What does `logging.getLogger().setLevel(logging.INFO)` change in the function's CloudWatch log?"
- "I wrote `analyze_new_book` in `book-analyzer/app.py`. Check it against `analyze_book()` in `chalicelib/analyze.py` and tell me what is wrong, without fixing it."

## Check your understanding

After Claude explains something, ask it to test you:

- "Ask me three questions about how an S3 upload reaches my handler. Wait for my answer after each one."
- "I think `chalice deploy` [your explanation]. Is that correct? Tell me what is missing."

## Stay safe

- Never paste your AWS credentials, your Atlas password, or a `.pem` key into a prompt.
- Read every `aws` and `chalice` command before you let Claude run it. Say no to commands that delete something (`chalice delete`, `aws s3 rb`, `aws s3 rm`) unless you are ready to clean up.
