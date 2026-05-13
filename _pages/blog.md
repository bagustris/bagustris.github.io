---
layout: archive
title: "Blog"
description: "Blog posts and articles"
permalink: /blog/
author_profile: true
order: 1
---

{% include base_path %}
> Writing is a way to think, to learn, and to share.

{% for post in site.posts %}
  {% include archive-single.html %}
{% endfor %}
