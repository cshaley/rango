from django.test import TestCase
from rango.models import Category, Page
from django.core.urlresolvers import reverse
from datetime import timedelta, datetime

def add_cat(name, views, likes):
    c = Category.objects.get_or_create(name=name)[0]
    c.views = views
    c.likes = likes
    c.save()
    return c

def add_page(title, views, first_visit, last_visit, cat):
    c = Page.objects.get_or_create(title=title, category=cat)[0]
    #c.category = cat
    c.views = views
    c.title = title
    c.first_visit = first_visit
    c.last_visit = last_visit
    c.save()
    return c


class CategoryMethodTests(TestCase):
    
    #ensure_views_are_positive should results True for categories where views are zero or positive
    def test_ensure_views_are_positive(self):
        cat = Category(name='test',catviews=-1, likes=0)
        cat.save()
        self.assertEqual((cat.catviews >= 0), True)

    #slug_line_creation checks to make sure that when we add a category an appropriate slug line is created
    #i.e. "Random Category String" -> "random-category-string"
    def test_slug_line_creation(self):
        cat = Category(name='Random Category String')
        cat.save()
        self.assertEqual(cat.slug, 'random-category-string')

class IndexViewTests(TestCase):

        #If no questions exist, an appropriate message should be displayed.
    def test_index_view_with_no_categories(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no categories present.")
        self.assertQuerysetEqual(response.context['categories'], [])

    #If no questions exist, an appropriate message should be displayed.
    def test_index_view_with_categories(self):
        add_cat('test',1,1)
        add_cat('temp',1,1)
        add_cat('tmp',1,1)
        add_cat('tmp test temp',1,1)

        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "tmp-test-temp")

        num_cats =len(response.context['categories'])
        self.assertEqual(num_cats , 4)

class PageViewTests(TestCase):
    
    #Make sure first visit and last visit are not in the future
    def test_page_view_visits_in_future(self):
        cat = add_cat('test',1,1)
        p1 = add_page('google', 1, datetime.now()+timedelta(1), datetime.now()+timedelta(1), cat)
        self.assertEqual((p1.first_visit<datetime.now()),True)
        self.assertEqual((p1.last_visit<datetime.now()),True)
    
    #Make sure last visit >= first visit
    def test_page_view_visits_in_future(self):
        cat = add_cat('test',1,1)
        p1 = add_page('google', 1, datetime.now()+timedelta(1), datetime.now()-timedelta(1), cat)
        self.assertEqual((p1.first_visit<=p1.last_visit),True)








