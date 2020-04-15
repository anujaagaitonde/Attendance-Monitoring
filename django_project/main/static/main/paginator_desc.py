from django.core.paginator import paginator

posts = ['1', '2', '3', '4', '5'] # dummy object variable to see how pagination works

p = paginator(posts, 2) # (objects to paginate, number of objects per page)

p.num_pages # returns how many pages we have

for page in p.page_range:
    print(page) # prints page numbers in order

p1 = p.page(1) # extracts the first page as an object, returns "<Page 1 of 3>"

p1.object_list # returns list of objects in page 1 "['1','2']"
p.count # returns total number of objects on all pages

p1.has_previous() # returns whether p1 has a previous page "False"
p1.has_next() # returns whether p1 has a next page "True"
p1.next_page_number # returns next page as an integer
