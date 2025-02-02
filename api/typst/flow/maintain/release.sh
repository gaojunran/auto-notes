#!/usr/bin/env nix-shell
#!nix-shell -i bash -p bash gh tomlq rsync
set -eux
source `dirname $0`/common

clone-index() {
	gh auth status
	if [[ ! -d packages ]]; then
		gh repo fork $index --clone
	fi

	target="`pwd`/packages/packages/preview/$name/$version"
}

copy-to-index() {
	pushd $repo
		mkdir -p $target
		rsync -vv -r \
			--include thumbnail/page-1.png \
			--exclude-from $repo/.gitignore \
			--exclude '.git*' \
			--exclude /thumbnail/generate \
			--exclude /MAINTAIN.md \
			--exclude /maintain \
			--exclude /doc \
			$repo/ $target/
	popd
}

push-to-repo() {
	# cleanup potentially previous runs on the same release
	git tag --delete $version || true
	git push origin :$version || true

	git commit --allow-empty --message "release: $version"
	git tag $version
	git push
	git push --tags
}

push-to-index() {
	pushd $target
		git switch -C "$name-$version"

		git add .
		git commit --message "$name:$version"
		git push -f -u origin @

		git switch main
	popd
}

clone-index
copy-to-index
push-to-repo
push-to-index
