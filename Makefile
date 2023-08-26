.PHONY: all check

all:
	quarto publish gh-pages --no-prompt

preview:
	quarto preview

check:
	rg '(^draft: |TODO)'
