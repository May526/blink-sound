.PHONY : dev
dev :
	rm -rf docs/build/
	sphinx-apidoc  -f -o ./docs/source ./ozyamamushi
	sphinx-autobuild -b html --watch ozyamamushi/ docs/source/ docs/build/

.PHONY : build
build :
	rm -rf docs/build/
	sphinx-apidoc  -f -o ./docs/source ./ozyamamushi
	sphinx-build ./docs/source ./docs/build

.PHONY : clean
clean :
	rm -rf docs/build/
