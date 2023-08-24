.PHONY: all check

all:
	quarto publish gh-pages --no-prompt

check:
	rg '(^draft: |TODO)'
