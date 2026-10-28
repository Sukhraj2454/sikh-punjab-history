# Virasat — Sikh & Punjab History

A source-conscious chronological Sikh and Punjab history lesson library, designed for GitHub Pages.

## Publish

In **Settings → Pages**, select **Deploy from a branch**, `main`, `/ (root)`. The intended URL is https://sukhraj2454.github.io/sikh-punjab-history/ .

GitHub Pages availability on a private repository depends on your GitHub plan. For free public hosting, make this repository public.

## Lessons

The site currently includes six lessons covering Guru Nanak Sahib's early life and the first journeys. Historical traditions are labeled distinctly from scripture and independently dated events.

## Updates

The twice-daily ChatGPT lesson reminders do not independently commit to GitHub. New lessons must be added to the site's content through GitHub or an authenticated automation. This site does not imply those updates are already automated.

## Twice daily publishing (GitHub Actions)

Workflow: `.github/workflows/publish-lessons.yml`. Runs at 02:30 and 14:30 UTC (08:00 and 20:00 IST), and can also be triggered manually from the Actions tab. GitHub scheduled runs may be delayed and are not precise alerts.

### Required activation

1. Visit **Settings → Secrets and variables → Actions → New repository secret**.
2. Add a secret named `OPENAI_API_KEY` with an OpenAI API key from your own API account. ChatGPT subscriptions do **not** include API credits. Never commit or share the key.
3. In **Settings → Actions → General**, ensure actions are enabled and workflow permissions include **Read and write permissions**. The workflow also declares `contents: write`.
4. Run **Actions → Publish Sikh history lessons twice daily → Run workflow** once to test.

A scheduled run requests one new lesson, appends it to `lessons.json`, and commits to main. The website reads that JSON so new lessons appear in the library without changing the HTML each time. The publisher validates structure, rejects duplicate slots and duplicates by title, and stops on API errors or insufficient content. It **does not** verify every historical assertion: AI-generated lessons are labeled **draft — verify sources**. This is not a substitute for reviewing scripture quotations, dates and citations before relying on them.

Your existing ChatGPT morning and evening lessons remain separate: the GitHub Action makes its own new content and can incur OpenAI API usage charges. It cannot copy ChatGPT scheduled lesson output without additional integration.
