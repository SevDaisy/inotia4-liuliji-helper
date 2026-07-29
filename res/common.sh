#!/usr/bin/bash

function walkDir() {
	# 避免无匹配时输出 *
	shopt -s nullglob
	for x in $1; do
		# 如果是普通文件才 cat
		if [[ -f "$x" ]]; then
			echo "${x##*/}: $(cat "$x")"
		fi
	done | sort | tr -d " "
}
function len() {
	bc=$(echo -n "$1" | wc -c)
	cc=$(echo -n "$1" | wc -m)
	echo $(((bc + cc) / 2))
}
function pad() {
	res=$(($2 - $(len "$1")))
	[[ "$res" -lt 1 ]] && res=1
	echo "$res"
}

function work() {
	target="${1:-point}"
	action="${2:-read}"

	case $action in
	r | R | read)
		walkDir "$(dirname $0)/$target/*"
		;;
	w | W | write)
		{
			echo "$data" | while IFS=: read -r name content; do
				# 如果 name 和 content 都不为空
				if [[ -n "$name" && -n "$content" ]]; then
					name="$(dirname $0)/$target/$name"
					content="$(echo "$content" | tr -d " ")"
					echo -n "$content" >"$name"
					# printf "Updated %s%$(pad $name 30)s: %s\n" "$name" "" "$content"
					printf "Updated ${name}: %s\n" "$content"
				fi
			done
		}
		;;
	*)
		{
			echo "unsupported action: $action" >&2
		}
		;;
	esac
}
