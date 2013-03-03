prefix=/usr/local/

ui:
	cd frontend; \
	python build.py
all: ui

install:
	mkdir $(prefix)tractorDrive
	cp -r . $(prefix)tractorDrive
	cp tractorDrive $(prefix)bin/
	install -m 0644 arduino/udev/90-tractor-wheel.rules /lib/udev/rules.d

uninstall:
	rm -rf $(prefix)tractorDrive
	rm $(prefix)/bin/tractorDrive
	rm /lib/udev/rules.d/90-tractor-wheel.rules

clean:
	rm frontend/ui_*
