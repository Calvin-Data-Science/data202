.PHONY: all deploy-all deploy-rmarkdown deploy-pdf book clean

ALL: deploy-all

docs := $(patsubst %.Rmd,%.html,$(shell find docs -iname '*.Rmd' -and -not -iname "*slides-common*" -and -not -iname "slide-setup.Rmd"))
slide_sources := $(wildcard docs/slides/*/*.Rmd)
slide_pdfs := $(patsubst %.Rmd,%.pdf,$(slide_sources))
#hw_sources := $(wildcard docs/*/hw/*.Rmd)
#hw_pdfs := $(patsubst %.Rmd,%.pdf,$(hw_sources))

WEB_DEST := csweb:/webroot/courses/data/202/23fa
#DELETE_OPTS := --delete-after --delete-excluded
DELETE_OPTS :=

%.html: %.Rmd
	Rscript -e "rmarkdown::render('"$<"')"

docs/slides/index.html: docs/slides/index.Rmd $(slide_sources)
	Rscript -e "rmarkdown::render('"$<"')"

$(slide_pdfs) : %.pdf: %.html
	decktape --pause 300 --chrome-arg=--allow-file-access-from-files "$<" "$@"

$(hw_pdfs) : %.pdf : %.html
	Rscript -e "pagedown::chrome_print('"$<"', '"$@"')"

deploy-rmarkdown: $(docs)
	rsync -rxi --copy-links --times --include="project/*" --exclude="*.Rmd" ${DELETE_OPTS} docs/ ${WEB_DEST}

deploy-pdf: $(slide_pdfs)# $(hw_pdfs)
	rsync -rxi --copy-links --times --include="project/*" --exclude="*.Rmd" ${DELETE_OPTS} docs/ ${WEB_DEST}

book:
	Rscript -e 'withr::with_dir("notes-raw", bookdown::render_book("."))'

deploy-all: deploy-rmarkdown deploy-pdf

clean:
	rm $(docs) $(slide_pdfs)
