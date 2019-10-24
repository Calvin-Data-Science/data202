%.html: %.md Makefile
	pandoc -s --toc --css=pandoc.css -o $@ $<

web/calendar.html: web/calendar.Rmd web/daily.txt
	Rscript -e "rmarkdown::render('"$<"')"

%.html: %.Rmd
	Rscript -e "rmarkdown::render('"$<"')"

deploy: web/index.html web/projects.html web/calendar.html web/resources.html
	rsync -Prx web/ cs-prod:/webroot/courses/data/202/ka37/
