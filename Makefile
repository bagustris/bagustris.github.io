DOCKER=docker
COMPOSE=docker-compose

# Docker image tag
TAG=jekyll-site

# Build the Docker image
build:
	$(DOCKER) build -t $(TAG) .

# Run the Jekyll site with docker-compose
serve:
	$(COMPOSE) up --build

# Run the Jekyll site in detached mode
serve-detached:
	$(COMPOSE) up --build -d

# Build the site for production
build-site:
	$(COMPOSE) --profile build run --rm build

# Stop the running containers
stop:
	$(COMPOSE) down

# Clean up containers and images
clean:
	$(COMPOSE) down --rmi all --volumes --remove-orphans

# Open a shell in the Jekyll container
shell:
	$(DOCKER) run --rm -it \
		-v $(PWD):/srv/jekyll \
		-w /srv/jekyll \
		$(TAG) \
		/bin/bash

# Install gems locally (useful for development)
bundle-install:
	$(DOCKER) run --rm \
		-v $(PWD):/srv/jekyll \
		-w /srv/jekyll \
		$(TAG) \
		bundle install

# Update gems
bundle-update:
	$(DOCKER) run --rm \
		-v $(PWD):/srv/jekyll \
		-w /srv/jekyll \
		$(TAG) \
		bundle update

.PHONY: build serve serve-detached build-site stop clean shell bundle-install bundle-update
