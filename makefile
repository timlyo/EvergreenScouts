directory = website/static

all:
	sass --watch sass/style.sass:${directory}/css/style.css --style compressed &
	sass --watch sass/form.sass:${directory}/css/form.css --style compressed &
	sass --watch sass/badges.sass:${directory}/css/badges.css --style compressed &
