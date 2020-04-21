#! /bin/bash

declare -a results=()

run_tests() {
	local rv
	for name in token tokenizer ah3 ah4 type;
	do
		echo "Running test test-$name.py"
		python test-$name.py
		rv=$?
		results+=(
		"$name":::"$rv"
		)
	done
}

print_summary() {
	for name__rv in "${results[@]}"
	do
		local name="${name__rv%:::*}"
		local rv="${name__rv#*:::}"
		echo "For test-${name}, rv is ${rv}"
	done
}

greppy() {
	grep '[^a-z]set(' -- *.py | grep -v utils.py
}

main() {
	run_tests
	print_summary
	# greppy
}

main "$@"
