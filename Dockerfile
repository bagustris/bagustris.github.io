# Use Ruby 3.2 with Ubuntu base for better compatibility
FROM ruby:3.2-slim

# Set environment variables
ENV LANG=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8 \
    LC_ALL=en_US.UTF-8 \
    DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    locales \
    curl \
    nodejs \
    npm \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && locale-gen en_US.UTF-8

# Set the working directory
WORKDIR /srv/jekyll

# Copy Gemfile first to leverage Docker cache
COPY Gemfile* ./

# Install bundler and gems
RUN gem install bundler && \
    bundle config set --local deployment 'false' && \
    bundle config set --local path 'vendor/bundle' && \
    bundle install

# Copy the rest of the site
COPY . .

# Create the Jekyll site directory if it doesn't exist
RUN mkdir -p _site

# Expose ports for Jekyll server and LiveReload
EXPOSE 4000 35729

# Default command to serve the site
CMD ["bundle", "exec", "jekyll", "serve", "--host=0.0.0.0", "--port=4000", "--livereload", "--force_polling"]
