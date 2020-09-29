ALL: deploy

docs := $(patsubst %.Rmd,%.html,$(shell find docs -iname '*.Rmd' -and -not -iname "*slides-common*"))
slide_pdfs := $(patsubst %.Rmd,%.pdf,$(shell find docs/slides -iname '*.Rmd' -and -not -iname "*slides-common*"))

%.html: %.Rmd
	Rscript -e "rmarkdown::render('"$<"')"

%.pdf: %.html
	decktape --pause 500 --chrome-arg=--allow-file-access-from-files "$<" "$@"

deploy: $(docs) $(slide_pdfs)
	rsync -rx --exclude="*.Rmd" --delete-after docs/ cs-prod:/webroot/courses/data/202/fa20
