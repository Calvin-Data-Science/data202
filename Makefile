%.html: %.md Makefile
	pandoc -s --toc --css=pandoc.css -o $@ $<
#--metadata=title:"DATA 202" 
deploy: web/index.html
	rsync -Prx web/ cs-prod:/webroot/courses/data/202/fa19/
