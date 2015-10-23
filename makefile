directory = static

all:
	sass --watch sass/style.sass:${directory}/css/style.css --style compressed &
	sass --watch sass/landing.sass:${directory}/css/landing.css --style compressed &
	sass --watch sass/badges.sass:${directory}/css/badges.css --style compressed &
