---
layout: default
---

<ul id="post-list">
    {\% for post in site.categories.카테고리이름 \%}
        {\% include 리스트레이아웃.html \%}
    {\% endfor \%}
</ul>
{\% include pagination.html \%}