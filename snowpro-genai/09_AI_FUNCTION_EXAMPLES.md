# AI function examples: one clear example per function

This file mirrors the **AI Functions** group in Snowflake's [SQL function reference](https://docs.snowflake.com/en/sql-reference-functions) sidebar (checked 2026-10-09): 18 `AI_` entries, the legacy `SNOWFLAKE.CORTEX` entries `FINETUNE` and `SENTIMENT`, and the **Helper functions** group. Every function in the sidebar has a section below.

**How to use it:** read the one-line purpose, run the example in a test account, then answer the "Exam trap" from memory. Examples were adapted from the linked reference pages and **have not been executed in a Snowflake account**. Replace stage, table and model names with your own, and check [regional availability](https://docs.snowflake.com/en/user-guide/snowflake-cortex/aisql-regional-availability), because models and some functions vary by region. Every function needs the `SNOWFLAKE.CORTEX_USER` database role, or a narrower role where the page names one (embedding functions also accept `SNOWFLAKE.CORTEX_EMBED_USER`).

**Error handling common to most functions:** a failing row returns `NULL` and the query keeps running. Most functions accept a final optional `return_error_details` BOOLEAN; when `TRUE` the result becomes an object with `value` and `error`.

**Sample table used below** (create once):

```sql
CREATE OR REPLACE TEMP TABLE reviews AS
SELECT * FROM VALUES
  (1, 'The pizza was excellent and the staff were lovely.'),
  (1, 'Great food, but we waited 50 minutes for a table.'),
  (2, 'Terrible quality ingredients. I would avoid this place.'),
  (2, 'Mediocre food and mediocre service.')
AS t(product_id, review);
```

## Contents

| # | Function | Task |
| ---: | --- | --- |
| 1 | [`AI_COMPLETE`](#1-ai_complete) | General generation, structured output, images |
| 2 | [`AI_CLASSIFY`](#2-ai_classify) | Label text/images/documents |
| 3 | [`AI_EXTRACT`](#3-ai_extract) | Pull named fields from text or a file |
| 4 | [`AI_FILTER`](#4-ai_filter) | Boolean predicate in `WHERE`/`JOIN` |
| 5 | [`AI_AGG`](#5-ai_agg) | Instruction-driven aggregate across rows |
| 6 | [`AI_SUMMARIZE`](#6-ai_summarize) | Summarize one text or file |
| 7 | [`AI_SUMMARIZE_AGG`](#7-ai_summarize_agg) | Summarize many rows |
| 8 | [`AI_SENTIMENT`](#8-ai_sentiment) | Overall and aspect sentiment |
| 9 | [`AI_TRANSLATE`](#9-ai_translate) | Translate text |
| 10 | [`AI_REDACT`](#10-ai_redact) | Redact or detect PII |
| 11 | [`AI_EMBED`](#11-ai_embed) | Vector for text or image |
| 12 | [`AI_MULTI_EMBED`](#12-ai_multi_embed) | Vectors for text/image/audio/video |
| 13 | [`AI_SIMILARITY`](#13-ai_similarity) | Cosine similarity of two inputs |
| 14 | [`AI_PARSE_DOCUMENT`](#14-ai_parse_document) | OCR or layout parsing of a document |
| 15 | [`AI_TRANSCRIBE`](#15-ai_transcribe) | Speech to text |
| 16 | [`AI_COUNT_TOKENS`](#16-ai_count_tokens) | Estimate input tokens |
| 17 | [`AI_FUNCTION_EVALUATION`](#17-ai_function_evaluation-preview) | Score a function against labeled data |
| 18 | [`AI_FUNCTION_OPTIMIZATION`](#18-ai_function_optimization-preview) | Search for a better prompt/model |
| 19 | [`SNOWFLAKE.CORTEX.FINETUNE`](#19-snowflakecortexfinetune-preview) | Fine-tune a base model |
| 20 | [`SNOWFLAKE.CORTEX.SENTIMENT`](#20-snowflakecortexsentiment) | Older numeric sentiment score |
| 21 | [Helper functions](#21-helper-functions) | `TO_FILE`, `PROMPT`, split-text, agent helpers |

---

## 1. `AI_COMPLETE`

**Purpose:** general text generation, analysis of supported images/documents, and constrained JSON output. [Reference](https://docs.snowflake.com/en/sql-reference/functions/ai_complete)

There are three forms: [single string](https://docs.snowflake.com/en/sql-reference/functions/ai_complete-single-string), [single file](https://docs.snowflake.com/en/sql-reference/functions/ai_complete-single-file) and [prompt object](https://docs.snowflake.com/en/sql-reference/functions/ai_complete-prompt-object).

```sql
-- Basic: model first, then prompt.
SELECT AI_COMPLETE('llama3.3-70b', 'Explain RAG in one sentence.');

-- Tuning options and token usage. show_details => TRUE returns a JSON object
-- (choices, created, model, usage) instead of a plain string.
SELECT AI_COMPLETE(
  model            => 'llama3.3-70b',
  prompt           => 'Give three tips for writing SQL.',
  model_parameters => {'temperature': 0, 'max_tokens': 200},
  show_details     => TRUE
);

-- Structured output: a response_format with a JSON schema returns an object
-- that matches it. Asking for "JSON" in the prompt text does not enforce this.
SELECT AI_COMPLETE(
  model           => 'llama3.3-70b',
  prompt          => 'Extract the city and country: "I flew from Paris, France to Sydney."',
  response_format => {
    'type': 'json',
    'schema': {
      'type': 'object',
      'properties': {
        'city':    {'type': 'string'},
        'country': {'type': 'string'}
      },
      'required': ['city', 'country']
    }
  }
);

-- Prompt object: PROMPT() with a FILE placeholder analyzes an image per row.
SELECT AI_COMPLETE('claude-sonnet-4-6',
         PROMPT('Classify the input image {0} in no more than 2 words.',
                TO_FILE('@MY_DB.MY_SCHEMA.IMG_STAGE', img_path))) AS label
FROM image_table;
```

**Exam traps:** `max_tokens` defaults to 4096 and small values truncate silently; `temperature` defaults to 0. `guardrails: TRUE` (Cortex Guard) adds input-token charges. The schema keywords `minLength`, `maxLength`, `minimum`, `maximum`, `minItems`, `maxItems` and `format` are **unsupported** and cause an error. OpenAI models need `additionalProperties: false` and every property listed in `required`. Set `temperature` to 0 for the most consistent structured output.

---

## 2. `AI_CLASSIFY`

**Purpose:** assign one or more labels from a list you supply. [Reference](https://docs.snowflake.com/en/sql-reference/functions/ai_classify)

```sql
-- Single label (default). Returns {"labels": ["travel"]}.
SELECT AI_CLASSIFY('One day I will see the world', ['travel', 'cooking']);

-- Multi-label, with a task description to sharpen the decision.
SELECT AI_CLASSIFY(
  'One day I will see the world and learn to cook my favorite dishes',
  ['travel', 'cooking', 'reading', 'driving'],
  {'output_mode': 'multi',
   'task_description': 'Classify the hobbies the writer wants to pursue'}
);

-- Labels with descriptions, applied to a column. Read the label with ['labels'][0].
SELECT review,
       AI_CLASSIFY(review,
         [{'label': 'food',    'description': 'taste, ingredients, menu'},
          {'label': 'service', 'description': 'staff, waiting time'}]):labels[0]::STRING AS topic
FROM reviews;
```

**Exam traps:** at least **two unique, case-sensitive** categories. `output_mode` is `'single'` (default) or `'multi'`; for documents it must be `'single'`. `examples` (few-shot) are not supported for documents. Descriptions and examples add input tokens to the bill. The output is an object with a `labels` array, not a bare string.

---

## 3. `AI_EXTRACT`

**Purpose:** pull named facts out of text or a staged file as structured data. [Reference](https://docs.snowflake.com/en/sql-reference/functions/ai_extract)

```sql
-- Text input, object map of label -> question.
SELECT AI_EXTRACT(
  text => 'John Smith lives in San Francisco and works for Snowflake',
  responseFormat => {'name': 'What is the first name of the employee?',
                     'city': 'Where does the employee live?'}
);
-- {"error": null, "response": {"city": "San Francisco", "name": "John"}}

-- File input, array of [label, question] pairs.
SELECT AI_EXTRACT(
  file => TO_FILE('@MY_DB.MY_SCHEMA.DOC_STAGE', 'invoice.pdf'),
  responseFormat => [['vendor', 'What is the vendor name?'],
                     ['total',  'What is the total amount due?']]
);

-- JSON schema with a list field and per-field confidence scores.
SELECT AI_EXTRACT(
  file => TO_FILE('@MY_DB.MY_SCHEMA.DOC_STAGE', 'report.pdf'),
  responseFormat => {'schema': {'type': 'object', 'properties': {
    'employees': {'description': 'What are the surnames of employees?', 'type': 'array'}}}},
  scores => TRUE
);
```

**Exam traps:** the result is always an object with `error` and `response`. Text and file inputs cannot be mixed in one call. A file must be under 100 MB and at most **125 pages** (compare `AI_PARSE_DOCUMENT`'s 2,000). Limits: 100 entity questions or 10 table questions per call, and one table question counts as 10 entity questions. `config`, `scores` and `file` are named-argument forms. You cannot mix the JSON-schema format with the other `responseFormat` styles.

---

## 4. `AI_FILTER`

**Purpose:** a natural-language yes/no that returns a BOOLEAN, usable in `WHERE` and `JOIN`. [Reference](https://docs.snowflake.com/en/sql-reference/functions/ai_filter)

```sql
-- Scalar.
SELECT AI_FILTER('Is Canada in North America?');

-- Row filter. PROMPT() fills {0} from the column.
SELECT product_id, review
FROM reviews
WHERE AI_FILTER(PROMPT('The reviewer liked the restaurant: {0}', review));

-- Semantic join across two tables.
SELECT r.name, j.title
FROM resumes r
JOIN jobs j
  ON AI_FILTER(PROMPT('Does this resume {0} suit this job description {1}?', r.contents, j.jd));

-- Image predicate.
SELECT TO_FILE(file_url) AS img
FROM DIRECTORY(@MY_DB.MY_SCHEMA.IMG_STAGE)
WHERE AI_FILTER('Is this a picture of a cat?', TO_FILE(file_url));
```

**Exam traps:** every row is a model call, so put cheap filters first to cut cost. Phrase the input as a question with full context and avoid `NULL` inputs. A semantic `JOIN` multiplies calls (rows × rows).

---

## 5. `AI_AGG`

**Purpose:** aggregate text across rows with **your own instruction**; it works beyond a single model context window. [Reference](https://docs.snowflake.com/en/sql-reference/functions/ai_agg)

```sql
SELECT product_id,
       AI_AGG(review, 'Summarize the recurring complaints and praise for potential diners') AS insight
FROM reviews
GROUP BY product_id;

-- Combine columns with || or CONCAT.
SELECT AI_AGG(product_id::STRING || ': ' || review, 'List the products with problems')
FROM reviews;
```

**Exam traps:** `AI_AGG` has a custom `instruction`; `AI_SUMMARIZE_AGG` does not. Write a declarative instruction that describes the text and the intended use. It returns text, and may say the data lacks the answer if the instruction is vague.

---

## 6. `AI_SUMMARIZE`

**Purpose:** summarize a single text value or a single file. [Reference](https://docs.snowflake.com/en/sql-reference/functions/ai_summarize)

```sql
SELECT AI_SUMMARIZE('Long product review text goes here ...');

-- Image or document from a stage.
SELECT AI_SUMMARIZE(TO_FILE('@MY_DB.MY_SCHEMA.DOC_STAGE', 'cartoon_image.jpeg')) AS image_summary;

-- One summary per row of a table.
SELECT review, AI_SUMMARIZE(review) AS short_version FROM reviews;
```

**Exam traps:** one input, one summary. To summarize *across* rows use `AI_SUMMARIZE_AGG`. File limits and context windows vary by region (for example 272K tokens in `ANY_REGION`, 1M on `GCP_GLOBAL`), and `AZURE_GLOBAL` supports images but not documents.

---

## 7. `AI_SUMMARIZE_AGG`

**Purpose:** one general summary across many rows. [Reference](https://docs.snowflake.com/en/sql-reference/functions/ai_summarize_agg)

```sql
SELECT product_id,
       AI_SUMMARIZE_AGG(review) AS summarized_review
FROM reviews
GROUP BY product_id;
```

**Exam traps:** an aggregate, so it works with `GROUP BY` and takes a single argument (no instruction). Need a custom instruction? Use `AI_AGG`.

---

## 8. `AI_SENTIMENT`

**Purpose:** overall sentiment, plus optional aspect-level sentiment. [Reference](https://docs.snowflake.com/en/sql-reference/functions/ai_sentiment)

```sql
-- Overall only.
SELECT AI_SENTIMENT('The room was clean but the service was painfully slow.');

-- Aspect-based: pass up to 10 categories.
SELECT AI_SENTIMENT(
  'Cheap, tasty, but the wait was long and the portions small.',
  ['Cost', 'Quality', 'Wait Time']
);
```

Output shape (values are illustrative):

```json
{"categories": [
  {"name": "overall",   "sentiment": "mixed"},
  {"name": "Cost",      "sentiment": "positive"},
  {"name": "Quality",   "sentiment": "positive"},
  {"name": "Wait Time", "sentiment": "negative"}]}
```

**Exam traps:** `sentiment` is one of `positive`, `negative`, `neutral`, `mixed` or `unknown`. **`unknown` means the aspect was not mentioned; it is not `neutral`.** The `overall` entry is always returned. Limits: up to 10 categories of up to 30 characters, and a 2,048-token context. It supports English, French, German, Hindi, Italian, Spanish and Portuguese. Do not confuse it with the older `SNOWFLAKE.CORTEX.SENTIMENT`, which returns a number (section 20).

---

## 9. `AI_TRANSLATE`

**Purpose:** translate text between languages. [Reference](https://docs.snowflake.com/en/sql-reference/functions/ai_translate)

```sql
-- English to German, per row.
SELECT AI_TRANSLATE(review, 'en', 'de') FROM reviews LIMIT 10;

-- Automatic source detection: an EMPTY STRING in the source slot.
SELECT AI_TRANSLATE('Voy a likear tus fotos en Insta.', '', 'en');
```

**Exam traps:** exactly **three** required arguments: text, source, target. `AI_TRANSLATE(text, 'en')` is not valid. Auto-detection is `''` in the *second* argument. Input is limited to 100,000 tokens.

---

## 10. `AI_REDACT`

**Purpose:** replace PII with placeholders, or return where it is. [Reference](https://docs.snowflake.com/en/sql-reference/functions/ai_redact)

```sql
-- Redact everything detected.
SELECT AI_REDACT('My name is Jane Doe and I live at 12 Main Street, Boston.');
-- My name is [NAME] and I live at [ADDRESS].

-- Redact only chosen categories.
SELECT AI_REDACT('Email jane@example.com or call 555-0100. I am Jane.', ['EMAIL', 'PHONE_NUMBER']);

-- Detect mode returns spans instead of redacted text.
SELECT AI_REDACT('Contact Jane at jane@example.com', mode => 'detect');
-- {"spans": [{"category": "NAME", "start": 8, "end": 12, "text": "Jane"}, ...]}
```

**Exam traps:** categories include `NAME`, `EMAIL`, `PHONE_NUMBER`, `DATE_OF_BIRTH`, `GENDER`, `AGE`, `ADDRESS`, `NATIONAL_ID`, `PASSPORT`, `TAX_IDENTIFIER`, `PAYMENT_CARD_DATA`, `DRIVERS_LICENSE` and `IP_ADDRESS`; an unsupported category is an error. Input plus output is capped at 4,096 tokens (output 1,024), so chunk long text first (section 21). Detection is best-effort, **not a substitute for RBAC or masking policies**.

---

## 11. `AI_EMBED`

**Purpose:** turn text or an image into a `VECTOR`. [Reference](https://docs.snowflake.com/en/sql-reference/functions/ai_embed)

```sql
-- Text.
SELECT AI_EMBED('snowflake-arctic-embed-l-v2.0', 'refund policy');

-- Image from a stage (the only image model is voyage-multimodal-3).
SELECT AI_EMBED('voyage-multimodal-3', TO_FILE('@MY_DB.MY_SCHEMA.IMG_STAGE', 'CITY_WALKING1.PNG'));

-- Store embeddings, then search with a vector function.
CREATE OR REPLACE TEMP TABLE review_vecs AS
SELECT review, AI_EMBED('snowflake-arctic-embed-l-v2.0', review) AS v FROM reviews;

SELECT review
FROM review_vecs
ORDER BY VECTOR_COSINE_SIMILARITY(v, AI_EMBED('snowflake-arctic-embed-l-v2.0', 'slow service')) DESC
LIMIT 2;
```

**Exam traps:** model first, then input. Compare vectors only from the **same model and dimension**. Higher cosine similarity = closer; lower L2 distance = closer. `AI_EMBED` replaces `EMBED_TEXT_768` and `EMBED_TEXT_1024`. Images must be JPEG, WEBP, PNG or BMP, up to 10 MB.

---

## 12. `AI_MULTI_EMBED`

**Purpose:** embeddings for text, images, audio and **video**, with per-segment results. [Reference](https://docs.snowflake.com/en/sql-reference/functions/ai_multi_embed)

```sql
-- Text (model: twelvelabs-marengo-embed-3-0 is the only listed model).
SELECT AI_MULTI_EMBED('twelvelabs-marengo-embed-3-0', 'a dog catching a frisbee');

-- Video, first 30 seconds only, fixed 5-second clips, visual embedding only.
SELECT AI_MULTI_EMBED(
  'twelvelabs-marengo-embed-3-0',
  TO_FILE('@MY_DB.MY_SCHEMA.MEDIA_STAGE', 'lecture.mp4'),
  {'start_sec': 0, 'end_sec': 30,
   'use_fixed_length_sec': 5,
   'embedding_options': ['visual']}
);
```

The result is an object `{"error": ..., "value": [ {embedding, embedding_option, embedding_scope, start_sec, end_sec}, ... ]}`. Cast an embedding with `VECTOR(FLOAT, 512)`.

**Exam traps:** `AI_EMBED` returns a bare `VECTOR`; `AI_MULTI_EMBED` returns an **object with an array of segment embeddings**. Timing options apply to audio and video only and are ignored for text and images. Limits: 4 hours or 6 GB for media, 500 tokens for text. Check region availability first.

---

## 13. `AI_SIMILARITY`

**Purpose:** cosine similarity (FLOAT, -1 to 1) between two inputs, without storing vectors. [Reference](https://docs.snowflake.com/en/sql-reference/functions/ai_similarity)

```sql
SELECT AI_SIMILARITY('The weather is nice today', 'It is sunny outside');

-- Choose another embedding model.
SELECT AI_SIMILARITY('Quarterly revenue grew', 'Sales increased this quarter', {'model': 'e5-base-v2'});

-- Rank rows against a search phrase.
SELECT review
FROM reviews
ORDER BY AI_SIMILARITY(review, 'long wait for a table') DESC
LIMIT 3;

-- Two images.
SELECT AI_SIMILARITY(TO_FILE('@MY_DB.MY_SCHEMA.IMG_STAGE', 'dog.jpg'),
                     TO_FILE('@MY_DB.MY_SCHEMA.IMG_STAGE', 'puppy.jpg'));
```

**Exam traps:** both inputs must be text **or** both images; text-vs-image is unsupported. It is billed under the `AI_EMBED` line item. Use `AI_EMBED` plus a stored vector column when you will query the same data repeatedly (one embedding call per row, not per comparison).

---

## 14. `AI_PARSE_DOCUMENT`

**Purpose:** extract the full text (and optionally structure) of a staged document, typically before chunking. [Reference](https://docs.snowflake.com/en/sql-reference/functions/ai_parse_document)

```sql
-- OCR (default): plain text.
SELECT PARSE_JSON(AI_PARSE_DOCUMENT(TO_FILE('@MY_DB.MY_SCHEMA.DOC_STAGE', 'contract.pdf'))):content::STRING;

-- LAYOUT: Markdown with headings and tables, one entry per page.
SELECT PARSE_JSON(AI_PARSE_DOCUMENT(
         TO_FILE('@MY_DB.MY_SCHEMA.DOC_STAGE', 'contract.pdf'),
         {'mode': 'LAYOUT', 'page_split': TRUE})) AS parsed;

-- Only pages 0-2 (zero-indexed, end is exclusive), with embedded images.
SELECT AI_PARSE_DOCUMENT(
         TO_FILE('@MY_DB.MY_SCHEMA.DOC_STAGE', 'report.pdf'),
         {'mode': 'LAYOUT', 'extract_images': TRUE,
          'page_filter': [{'start': 0, 'end': 3}]});
```

**Exam traps:** `OCR` (default) = text only; `LAYOUT` = text plus structure as Markdown. `extract_images` needs `LAYOUT`. `page_split` supports PDF, PPTX and DOCX and changes the output to a `pages` array with `content` and `index` (starting at 0); `page_filter` implies `page_split`. The output is a JSON **string**, so use `PARSE_JSON` to query it. It is **page-billed**, not token-billed. Limits: 100 MB and 2,000 pages. Use `AI_EXTRACT` instead when you want specific named fields.

---

## 15. `AI_TRANSCRIBE`

**Purpose:** speech-to-text for staged audio and video. [Reference](https://docs.snowflake.com/en/sql-reference/functions/ai_transcribe)

```sql
-- Whole transcript as one text value.
SELECT AI_TRANSCRIBE(TO_FILE('@MY_DB.MY_SCHEMA.AUDIO_STAGE', 'consultation.wav'));

-- Word-level timestamps.
SELECT AI_TRANSCRIBE(TO_FILE('@MY_DB.MY_SCHEMA.AUDIO_STAGE', 'consultation.wav'),
                     {'timestamp_granularity': 'word'});

-- One segment per speaker turn, with SPEAKER_00, SPEAKER_01 ... labels.
SELECT AI_TRANSCRIBE(TO_FILE('@MY_DB.MY_SCHEMA.AUDIO_STAGE', 'meeting.wav'),
                     {'timestamp_granularity': 'speaker'});
```

**Exam traps:** the only documented option is `timestamp_granularity` (`'word'` or `'speaker'`). The result is a JSON string with `audio_duration` and either `text` or `segments`. Maximum 700 MB; 60 minutes **with** a granularity, 120 minutes without.

---

## 16. `AI_COUNT_TOKENS`

**Purpose:** estimate **input** tokens for a given function before you run it. [Reference](https://docs.snowflake.com/en/sql-reference/functions/ai_count_tokens)

```sql
-- Function name is a lowercase string starting with ai_.
SELECT AI_COUNT_TOKENS('ai_sentiment',
  'This place makes the best truffle pizza in the world! Too bad I cannot afford it');

-- Functions that take a model need it in the second position.
SELECT AI_COUNT_TOKENS('ai_complete', 'llama3.3-70b', 'Draft a short lesson on RAG.');

-- Budget a whole table before a large AI_COMPLETE run.
SELECT SUM(AI_COUNT_TOKENS('ai_complete', 'llama3.3-70b', review)) AS input_tokens FROM reviews;
```

**Exam traps:** it returns an INTEGER and **excludes output tokens**, so it underestimates generation cost. It does not call the model to generate. A model name is required for functions such as `AI_COMPLETE` and `AI_EMBED`.

---

## 17. `AI_FUNCTION_EVALUATION` (preview)

**Purpose:** measure the **quality** of an AI function call against a labeled dataset. It measures only; it never changes the function. [Reference](https://docs.snowflake.com/en/sql-reference/functions/ai_function_evaluation)

This is an **experiment**, not a scalar function: you create it from a YAML specification, then execute it.

```sql
CREATE OR REPLACE EXPERIMENT my_db.my_schema.sentiment_eval
  TYPE = 'AI_FUNCTION_EVALUATION'
  FROM SPECIFICATION $$
    function:
      query_text: <the AI function expression under test, e.g. an AI_COMPLETE call>
    metrics:
      - name: exact_match
    dataset:
      name: <snowflake_dataset_name>
      version: <dataset_version>
      ground_truth: <label_column>
  $$;

EXECUTE EXPERIMENT my_db.my_schema.sentiment_eval;

-- Read the results.
SHOW RUNS IN EXPERIMENT my_db.my_schema.sentiment_eval;
SHOW RUN METRICS IN EXPERIMENT my_db.my_schema.sentiment_eval RUN EVAL_1;     -- aggregate score, 0 to 1
SHOW RUN PARAMETERS IN EXPERIMENT my_db.my_schema.sentiment_eval RUN EVAL_1;  -- model, rows_evaluated ...
```

The YAML above is a **skeleton** built from the reference's field names; fill the placeholders from the live page before running.

**Exam traps:** metrics are `exact_match`, `fuzzy_match`, `contains_match`, `redaction_match`, `llm_judge` (needs `judge_model`) and `custom` (needs `custom_udf`). The dataset must be a Snowflake **dataset** object, not a plain table or view. Privileges: `CREATE EXPERIMENT` on the schema, `SNOWFLAKE.CORTEX_USER` or `SNOWFLAKE.AI_FUNCTIONS_USER`, and `USAGE` on the dataset's database and schema. Billing is two parts: serverless compute metered as `SERVERLESS_EXPERIMENTS`, plus Cortex inference tokens for every AI call.

---

## 18. `AI_FUNCTION_OPTIMIZATION` (preview)

**Purpose:** search for a **better implementation** (prompt and model settings) of an existing AI function, scored against a labeled dataset. The original is never changed. [Reference](https://docs.snowflake.com/en/sql-reference/functions/ai_function_optimization)

```sql
CREATE OR REPLACE EXPERIMENT my_db.my_schema.classify_opt
  TYPE = 'AI_FUNCTION_OPTIMIZATION'
  FROM SPECIFICATION $$
    function:      # the existing AI function to improve
      ...
    metrics:       # one metric per run
      ...
    dataset:       # versioned labeled dataset, up to 1,000 rows
      ...
    optimization:  # candidate models, reflection model, budget
      ...
  $$;

EXECUTE EXPERIMENT my_db.my_schema.classify_opt;

-- After reviewing the quality-versus-cost results, promote the chosen run:
-- CREATE AI FUNCTION ... FROM EXPERIMENT ...   (see the reference for exact syntax)
```

The four YAML section names come from the reference; their inner fields are deliberately left out here because they were not verified. Open the live page before building one.

**Exam traps:** only for functions that make **exactly one `AI_COMPLETE` call**; datasets up to 1,000 rows; one metric per run. It reports each candidate's quality **and cost** (a quality-versus-cost frontier), and larger budgets or more candidate models raise cost. It still says "rolling out to accounts" in places, so confirm availability. Same privileges and billing as evaluation (`SERVERLESS_EXPERIMENTS` plus tokens).

**Evaluation vs optimization in one line:** evaluation *scores* what you have; optimization *searches* for something better and then you promote a winner.

---

## 19. `SNOWFLAKE.CORTEX.FINETUNE` (preview)

**Purpose:** create and manage fine-tuning jobs that train an adapter on a base model. [Reference](https://docs.snowflake.com/en/sql-reference/functions/finetune-snowflake-cortex) · [CREATE](https://docs.snowflake.com/en/sql-reference/functions/finetune-create) · [Fine-tuning guide](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-finetuning)

```sql
-- Start a job. Returns a job ID such as ft_6556e15c-...
SELECT SNOWFLAKE.CORTEX.FINETUNE(
  'CREATE',
  'my_tuned_model',                                   -- name in the model registry
  'llama3.1-8b',                                      -- base model
  'SELECT prompt, completion FROM train',             -- training query
  'SELECT prompt, completion FROM validation',        -- optional validation query
  '{"max_epochs": 3}'                                 -- optional JSON options (1 to 10)
);

-- List jobs (id, status, base_model, created_on).
SELECT SNOWFLAKE.CORTEX.FINETUNE('SHOW');

-- Inspect one job; when status is SUCCESS the object's `model` field names the tuned model.
SELECT SNOWFLAKE.CORTEX.FINETUNE('DESCRIBE', 'ft_6556e15c-8f12-4d94-8cb0-87e6f2fd2299');

-- Cancel a running job (returns a confirmation string).
SELECT SNOWFLAKE.CORTEX.FINETUNE('CANCEL', 'ft_194bbea4-1208-42f3-88c6-cfb202086125');

-- Once the job succeeds, call the tuned model by its name (see the fine-tuning guide for access grants).
SELECT AI_COMPLETE('my_tuned_model', 'A prompt like those in the training data');
```

**Exam traps:** the commands are `CREATE`, `SHOW`, `DESCRIBE` and `CANCEL`. The training query must return **`prompt` and `completion`** columns. If you omit validation data, the training data is split automatically. The documented base model is `llama3.1-8b`, and the feature is in preview in limited regions (AWS US West 2, AWS US East 1, AWS Europe Central 1, Azure East US 2 at the time of checking). Fine-tuning fits stable behavior or style; it does **not** refresh changing facts (use Search/RAG). Training and later inference are billed separately.

---

## 20. `SNOWFLAKE.CORTEX.SENTIMENT`

**Purpose:** the older sentiment function; returns a single **number**. [Reference](https://docs.snowflake.com/en/sql-reference/functions/sentiment-snowflake-cortex)

```sql
SELECT SNOWFLAKE.CORTEX.SENTIMENT('The food was wonderful but the service was awful.');
-- a FLOAT between -1 and 1 (example value shape: 0.54)

-- Compare with the newer function on the same input.
SELECT SNOWFLAKE.CORTEX.SENTIMENT(review) AS score,
       AI_SENTIMENT(review)               AS detail
FROM reviews;
```

**Exam traps:** it returns a FLOAT from -1 to 1 (0.5 to 1 positive, -0.5 to 0.5 neutral, -0.5 to -1 negative), **English only**, and only an overall score. `AI_SENTIMENT` returns an object with `overall` and optional per-aspect labels. The reference page lists `AI_SENTIMENT` as related content but does not mark this function deprecated, so prefer `AI_SENTIMENT` for new work without claiming the older one is removed.

---

## 21. Helper functions

The sidebar's **Helper functions** group lists `PROMPT`, `TO_FILE`, `SPLIT_TEXT_RECURSIVE_CHARACTER`, `AGENT_RUN`, `DATA_AGENT_RUN` and `THREAD_MESSAGES`. Only the first three are exercised here; the agent helpers are listed so you recognize them, and their syntax was not checked for this file.

```sql
-- TO_FILE: build a FILE object from a staged path. A local path is NOT a FILE.
SELECT TO_FILE('@MY_DB.MY_SCHEMA.DOC_STAGE', 'invoice.pdf');

-- PROMPT: a template with {0}, {1} ... placeholders; accepts strings and FILEs.
SELECT PROMPT('Hello, {0}! Today is {1}.', 'Alice', 'Monday');

SELECT AI_COMPLETE('claude-sonnet-4-6',
         PROMPT('Compare {0} with {1} in one sentence.',
                TO_FILE('@MY_DB.MY_SCHEMA.IMG_STAGE', 'a.png'),
                TO_FILE('@MY_DB.MY_SCHEMA.IMG_STAGE', 'b.png')));

-- SPLIT_TEXT_RECURSIVE_CHARACTER: (text, format, chunk_size [, overlap] [, separators]).
SELECT SNOWFLAKE.CORTEX.SPLIT_TEXT_RECURSIVE_CHARACTER('hello world are you here', 'none', 15, 10);
-- ['hello world are', 'world are you', 'are you here']

-- Typical RAG chunking: parse, split, one row per chunk.
SELECT c.value::STRING AS chunk
FROM (SELECT PARSE_JSON(AI_PARSE_DOCUMENT(
              TO_FILE('@MY_DB.MY_SCHEMA.DOC_STAGE', 'policy.pdf'), {'mode': 'LAYOUT'})):content::STRING AS txt) d,
     LATERAL FLATTEN(SNOWFLAKE.CORTEX.SPLIT_TEXT_RECURSIVE_CHARACTER(d.txt, 'markdown', 1500, 200)) c;
```

**Exam traps:** `format` is `'none'` (only your separators) or `'markdown'` (also splits on headers, code blocks and tables). `overlap` must be smaller than `chunk_size`. The chunk size is in **characters**, not tokens. The function returns an array, so `FLATTEN` it into rows.

---

## Quick chooser

| You want to... | Use |
| --- | --- |
| Generate or reason over text/images freely | `AI_COMPLETE` |
| Pick from labels you define | `AI_CLASSIFY` |
| Pull named fields from a document | `AI_EXTRACT` |
| Get the whole text or layout of a document | `AI_PARSE_DOCUMENT` |
| Keep or drop rows by a natural-language rule | `AI_FILTER` |
| Summarize one item / many rows / many rows with your instruction | `AI_SUMMARIZE` / `AI_SUMMARIZE_AGG` / `AI_AGG` |
| Overall or per-aspect sentiment | `AI_SENTIMENT` |
| Translate | `AI_TRANSLATE` (`''` source = auto) |
| Remove or locate PII | `AI_REDACT` |
| Store vectors / compare two things once | `AI_EMBED` / `AI_SIMILARITY` |
| Embed audio or video | `AI_MULTI_EMBED` |
| Turn audio into text | `AI_TRANSCRIBE` |
| Estimate input cost first | `AI_COUNT_TOKENS` |
| Measure function quality | `AI_FUNCTION_EVALUATION` |
| Improve an `AI_COMPLETE`-based function | `AI_FUNCTION_OPTIMIZATION` |
| Teach a base model a stable style | `SNOWFLAKE.CORTEX.FINETUNE` |
