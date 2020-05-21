# https://gist.github.com/klmr/575726c7e05d8780505a
# Inspired by
# <http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html>
# sed script explained:
# /^##/:
# 	* save line in hold space
# 	* purge line
# 	* Loop:
# 		* append newline + line to hold space
# 		* go to next line
# 		* if line starts with doc comment, strip comment character off and loop
# 	* remove target prerequisites
# 	* append hold space (+ newline) to line
# 	* replace newline plus comments by
# 	* print line
# Separate expressions are necessary because labels cannot be delimited by
# semicolon; see <http://stackoverflow.com/a/11799865/1968>
.PHONY: help
## Print this help message
help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) == Darwin && echo '--no-init --raw-control-chars')

.PHONY: clean
## Clean up all pyc files
clean:
	find . -name '*.pyc' -exec rm {} \+

.PHONY: test-p2
## Run test under python2.7
test-p2: shell-p2.nix
	nix-shell $< --command 'make test'

.PHONY: test-p3
## Run test under python3 (default: 3.8)
test-p3: test-p38

.PHONY: test-p35
## Run test under python3.5
test-p35: shell-p35.nix
	nix-shell $< --command 'make test'

.PHONY: test-p36
## Run test under python3.6
test-p36: shell-p36.nix
	nix-shell $< --command 'make test'

.PHONY: test-p37
## Run test under python3
test-p37: shell-p37.nix
	nix-shell $< --command 'make test'

.PHONY: test-p38
## Run test under python3.8
test-p38: shell-p38.nix
	nix-shell $< --command 'make test'

.PHONY: test-all-pythons
## Run test under python 2.7, 3.5, 3.6, 3.7 and 3.8
test-all-pythons: test-p2 test-p35 test-p36 test-p37 test-p38

.PHONY: test
## Run test under system python
test:
	# pytest
	python -m pytest
