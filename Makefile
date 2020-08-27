ALL: deploy

docs := $(patsubst %.Rmd,%.html,$(wildcard docs/*.Rmd))

%.html: %.Rmd
	Rscript -e "rmarkdown::render('"$<"')"

deploy: $(docs)
	rsync -Prx docs/ cs-prod:/webroot/courses/data/202/fa20
