#!/bin/bash

declare -a results=()

run_tests() {
	local total_rv=0
	local run_as_module=0
	if [[ "$1" = -m ]]
	then
		shift
		run_as_module=1
	fi

	local test_dir="tests"

	if ((run_as_module))
	then
		local test_mod_init="${test_dir}/__init__.py"
		touch "${test_mod_init}"
	fi

	local rv
	for name in "$@"
	do
		local file="${test_dir}/test_$name.py"
		echo "Running test ${file}"

		if ((run_as_module))
		then
			local modname="${file%.py}"
			local modname="${modname//\//.}"
			python -m "${modname}"
		else
			python "${file}"
		fi

		rv=$?

		if ((rv))
		then
			total_rv="${rv}"
		fi

		results+=(
			"$name":::"$rv"
		)
	done

	if ((run_as_module))
	then
		rm -f "${test_mod_init}"{,c} || :
	fi

	return "${total_rv}"
}

run_tests_m() {
	run_tests -m "$@"
}

print_summary() {
	for name__rv in "${results[@]}"
	do
		local name="${name__rv%:::*}"
		local rv="${name__rv#*:::}"
		local result_string

		if [[ "$rv" = 0 ]]
		then
			result_string="\e[32mPASS\e[m"
		else
			result_string="\e[31mFAIL\e[m"
		fi
		printf "%10s - %10b\n" "${name}" "${result_string}"
	done
}

greppy() {
	grep '[^a-z]set(' -- *.py | grep -v utils.py
}

main() {
	local -a tests=(
		token
		tokenizer
		ah3
		ah4
		type
		# ah
		# ah2
	)

	if [[ $# -ne 0 ]]
	then
		tests=("$@")
	fi

	run_tests_m "${tests[@]}"
	local rv=$?
	print_summary
	# greppy
	return "${rv}"
}

main "$@"
