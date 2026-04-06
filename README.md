# DATA 202 Course Website

Minimal GitHub Pages site for the DATA 202 Machine Learning course.

## Structure

- Markdown pages (`*.md`) for course content
- Shared layout in `_layouts/default.html`
- Styles in `assets/styles.css`

## Deploy on GitHub Pages

1. Push this repository to GitHub.
2. In repository settings, go to **Pages**.
3. Set **Build and deployment** source to **GitHub Actions**.
4. Ensure your default branch is `main` or update `.github/workflows/deploy-pages.yml`.
5. Push changes to `main`; the workflow will build and deploy automatically.
