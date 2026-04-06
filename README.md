# DATA202 - Introduction to Machine Learning

Minimal GitHub Pages site for DATA202 - Introduction to Machine Learning.

## Structure

- Markdown pages (`*.md`) for course content
- Shared layout in `_layouts/default.html`
- Styles in `assets/styles.css`

## Deploy on GitHub Pages

1. Push this repository to GitHub.
2. In repository settings, go to **Pages**.
3. Set **Build and deployment** source to **Deploy from a branch**.
4. Set the branch to `gh-pages` and folder to `/ (root)`.
5. Merge your content from `main` into `gh-pages`, then push `gh-pages`.
6. GitHub Pages will publish directly from the `gh-pages` branch.

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
