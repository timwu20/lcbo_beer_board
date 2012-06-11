from django.test import TestCase
from lcbo_beer_board.core.views import _get_beers, _get_beers_by_page, home
from lcbo_beer_board.core.templatetags.beer_tags import currency
from django.core.cache import cache


class ViewTests(TestCase):

    def test_get_beers(self):
    	'''
    	Tests the _get_beers function by making sure it returns a list of beers
    	and ensures that the list is not an empty list
    	'''
    	beers = _get_beers()
    	self.assertTrue( type(beers) == type([]) )
    	self.assertTrue( len(beers) > 0 )

    	#test that the beers have the attributes I'm looking for
    	self.assertTrue( beers[0].has_key('name') )
    	self.assertTrue( beers[0].has_key('price_in_cents') )

    def test_home(self):
    	'''
    	Tests the homepage
    	'''
    	resp = self.client.get('/')
    	self.assertEqual(resp.status_code, 200)
    	self.assertTrue('beers' in resp.context)


class TemplateTagTests(TestCase):

    def test_currency_tag(self):
    	'''
    	Tests the currency templatetags
    	'''
    	self.assertEqual( currency(0), '0.00' )
    	self.assertEqual( currency(0000), '0.00' )
    	self.assertEqual( currency(9999999), '99,999.99' )
    	self.assertEqual( currency(-3095), '-30.95' )


