#!/usr/bin/make

PYTHON_DEPENDENCIES = Jinja2 markdown
NODE_DEPENDENCIES = less minimist

pythonenv:
	virtualenv --python=python3 pythonenv
	pythonenv/bin/pip install $(PYTHON_DEPENDENCIES)

node_modules:
	npm install $(NODE_DEPENDENCIES)

dependencies: pythonenv node_modules

VERSION=0.1.1
deb:
	mkdir -p anvil_$(VERSION)
	mkdir -p anvil_$(VERSION)/DEBIAN
	mkdir -p anvil_$(VERSION)/usr
	mkdir -p anvil_$(VERSION)/usr/bin
	mkdir -p anvil_$(VERSION)/etc/anvil

	cp anvil.sh anvil_$(VERSION)/usr/bin/anvil
	cp render_html.py anvil_$(VERSION)/etc/anvil/
	cp render_styles.js anvil_$(VERSION)/etc/anvil/

	cp packaging/postinst anvil_$(VERSION)/DEBIAN/postinst
	chmod 0755 anvil_$(VERSION)/DEBIAN/postinst
	echo "Package: anvil" > anvil_$(VERSION)/DEBIAN/control
	echo "Version: $(VERSION)" >> anvil_$(VERSION)/DEBIAN/control
	echo "Section: base" >> anvil_$(VERSION)/DEBIAN/control
	echo "Priority: optional" >> anvil_$(VERSION)/DEBIAN/control
	echo "Architecture: amd64" >> anvil_$(VERSION)/DEBIAN/control
	echo "Depends: python3 (>=3.6), python3-dev (>=3.6)" >> anvil_$(VERSION)/DEBIAN/control
	echo "Description: Always at your service!" >> anvil_$(VERSION)/DEBIAN/control
	echo "Maintainer: Christian Kokoska (info@softcreate.de)" >> anvil_$(VERSION)/DEBIAN/control
	cat anvil_$(VERSION)/DEBIAN/control
	dpkg-deb --build anvil_$(VERSION)

clean:
	rm -rf pythonenv
	rm -rf node_modules
	rm -rf anvil_*
