# DATA202 - Introduction to Machine Learning

Minimal GitHub Pages site for DATA202 - Introduction to Machine Learning.

## Structure

- Markdown pages (`*.md`) for course content
- Shared layout in `_layouts/default.html`
- Styles in `assets/styles.css`

## Deploy on GitHub Pages

1. Push this repository to GitHub.
2. In repository settings, go to **Pages**.
3. Set **Build and deployment** source to **GitHub Actions**.
4. Ensure your deployment branches match `.github/workflows/deploy-pages.yml`.
5. Push changes to `main` or `26fall`; the workflow will build and deploy automatically.

## Preview Locally (Without Deploying)

1. Install Ruby (with DevKit on Windows) so `ruby` and `bundle` are available in your terminal.
2. Install dependencies from this repository root:

	```powershell
	bundle install
	```

3. Start the local site server:

	```powershell
	bundle exec jekyll serve --livereload
	```

4. Open `http://127.0.0.1:4000` in your browser.
