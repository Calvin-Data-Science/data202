ALL: deploy-all

docs := $(patsubst %.Rmd,%.html,$(shell find docs -iname '*.Rmd' -and -not -iname "*slides-common*" -and -not -iname "slide-setup.Rmd"))
slide_sources := $(shell find docs/slides -iname '*.Rmd' -and -not -iname "*slides-common*" -and -not -iname "slide-setup.Rmd" -and -not -path "*/slides/index.Rmd")
slide_pdfs := $(patsubst %.Rmd,%.pdf,$(slide_sources))



%.html: %.Rmd
	Rscript -e "rmarkdown::render('"$<"')"

docs/slides/index.html: docs/slides/index.Rmd $(slide_sources)
	Rscript -e "rmarkdown::render('"$<"')"

%.pdf: %.html
	decktape --pause 500 --chrome-arg=--allow-file-access-from-files "$<" "$@"

deploy-rmarkdown: $(docs)
	rsync -rxi --copy-links --times --exclude="*.Rmd" --delete-after --delete-excluded docs/ cs-prod:/webroot/courses/data/202/21fa

deploy-pdf: $(slide_pdfs)
	rsync -rxi --copy-links --times --exclude="*.Rmd" --delete-after docs/ cs-prod:/webroot/courses/data/202/21fa

book:
	Rscript -e 'withr::with_dir("notes-raw", bookdown::render_book("."))'

deploy-all: deploy-rmarkdown deploy-pdf
