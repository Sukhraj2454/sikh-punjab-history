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

## Design and accessibility

The buildless site uses a small local SVG landscape with architecture-inspired silhouettes. It is decorative scenery, not a reconstruction of a named historic place, and contains no portraits. There are no runtime JavaScript dependencies or image service requests.

Scroll parallax in the hero, lesson reading banner and timeline is clamped to 50px and updated using a passive scroll listener and a single animation frame. Off-screen sections skip updates. The operating system's reduced-motion setting disables parallax, smooth scrolling and hover movement. Navigation and lesson cards support keyboard focus; all four navigation links remain available on phones.

Preview locally with `python3 -m http.server 8080`, then visit `http://localhost:8080`. GitHub Pages must serve the repository root on `main`; all asset and lesson paths are relative to support the project URL. No build or new hosting service is required.
