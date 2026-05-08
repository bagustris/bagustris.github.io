---
layout: archive
title: "Blog"
description: "Blog posts and articles"
permalink: /blog/
author_profile: true
order: 1
---

{% include base_path %}

{% for post in site.posts %}
  {% include archive-single.html %}
{% endfor %}
