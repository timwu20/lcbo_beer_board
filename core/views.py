from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.cache import cache
import json, urllib2, urllib

def _get_beers_by_page(page=1):
	params = {
		'q': 'beer',
		'per_page' : 100,
		'page': page,
	}
	url = 'http://lcboapi.com/products/?%s' % (urllib.urlencode(params))
	try:
		data = urllib2.urlopen(url).read()
		data = json.loads(data)

		if data.has_key('status') and data['status'] == 200:
			return data
		else:
			return None
	except:
		return None

def _get_beers():
	data = cache.get('all_beers')
	if data:
		return data

	data = _get_beers_by_page()

	if data and data.has_key('pager') and data['pager'].has_key('final_page') and data.has_key('result'):
		final_page = data['pager']['final_page']
		beers = data['result']

		for i in range(2, final_page):
			pd = _get_beers_by_page(page=i)
			if pd:
				beers = beers + pd['result']

		beers = sorted(beers, key=lambda beer: beer['price_in_cents'])
		beers = sorted(beers, key=lambda beer: beer['name'])
		beers = sorted(beers, key=lambda beer: beer['limited_time_offer_savings_in_cents'], reverse=True)

		cache.set('all_beers', beers)
		return beers
	
	else:
		return None

def home(request):
	beer_data = _get_beers()
	
	context = {
		'beers': beer_data,
	}
	return render_to_response('index.html', context, context_instance=RequestContext(request))