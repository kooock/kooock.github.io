---
layout: default
---

<ul id="post-list">
    {% for post in site.categories.DeveloperSeries %}
       <li><a href="{{ post.url }}">{{ post.title }}</a></li>
    {% endfor %}
</ul>