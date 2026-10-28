# Virasat — Sikh & Punjab History

A chronological, source-conscious Sikh and Punjab history library hosted on GitHub Pages.

Website: https://sukhraj2454.github.io/sikh-punjab-history/

## Updating lessons manually

Edit `lessons.json` on the `main` branch and append a new lesson object using the same schema as the existing entries:

- `id`: next consecutive integer
- `title`: lesson heading
- `period`: historical period
- `era`: section (e.g. Journeys)
- `intro`: historical background
- `record`: Gurbani and historical evidence, with exact Ang / book attributions
- `tradition`: relevant sakhi with traditional provenance and uncertainty explicitly marked
- `recap`: compact memory aid
- `questions`: exactly three review questions
- `references`: optional array of published source descriptions

Commit the file, and GitHub Pages will display the new lesson automatically when the static site updates. The HTML fetches `lessons.json` at runtime, so you do not need to edit `index.html` for each addition.

The website does not generate or publish lessons on a schedule. ChatGPT's twice-daily scheduled lessons, if enabled, remain separate from this repository. Any GitHub Pages deployment pipeline is configured independently under repository Settings → Pages.

## Sources

Prioritize Basics of Sikhi/WhyGuru, Sri Guru Granth Sahib Ji with precise Ang references, the Encyclopaedia of Sikhism, J. S. Grewal's *The Sikhs of the Punjab*, and Khushwant Singh's *A History of the Sikhs*. Attribute traditional accounts and historical evidence separately.
