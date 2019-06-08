import unittest
import math

from app import functions


class TestGetLatAndLon(unittest.TestCase):
	def test_kingsmeadow_postcode(self):
		postcode = 'KT1 3PB'
		result = functions.get_lat_and_lon(postcode)
		self.assertEqual(result, (51.40605, -0.281429), 
			'wrong latitude or longitude returned - check api'
			)

	def test_twickenham_stadium_postcode(self):
		postcode = 'TW1 1DZ'
		result = functions.get_lat_and_lon(postcode)
		self.assertTrue(math.isnan(result[0]) and math.isnan(result[1]),
			'TW1 1DZ should return nan, check api '
			)

	def test_invalid_postcode(self):
		postcode = 123
		result = functions.get_lat_and_lon(postcode)
		self.assertTrue(math.isnan(result[0]) and math.isnan(result[1]),
			'invalid postcode should return nan'
			)


class TestCalcDistance(unittest.TestCase):
	def test_battersea_to_bognor_regis(self):
		lat1, lon1 = 51.469643, -0.176429
		lat2, lon2 = 50.798685, -0.667151
		result = functions.calc_distance(lat1, lon1, lat2, lon2)
		self.assertEqual(result, 82.09, 
			'distance does not match value calculated on movable-type.co.uk'
			) 

	def test_nan(self):
		lat1, lon1 = float('nan'), float('nan')
		lat2, lon2 = 50.798685, -0.667151
		result = functions.calc_distance(lat1, lon1, lat2, lon2)
		self.assertTrue(math.isnan(result), 'nan inputs should return nan') 


class TestFindStores(unittest.TestCase):
	def setUp(self):
		self.postcode = 'KT1 3PB'

	def test_kingsmeadow_postcode_with_radius_0(self):
		result = functions.find_stores(self.postcode, 0)
		self.assertEqual(len(result), 0, 
			'radius 0 should return 0 stores'
			)

	def test_kingsmeadow_postcode_with_radius_10(self):
		result = functions.find_stores(self.postcode, 10)
		self.assertEqual(len(result), 6, 
			'radius 10 should return 6 stores Brentford, Richmond, Feltham,' 
			+ ' Wimbledon, New Malden, Walton-on-Thames'
			)

	def test_north_south_ordering_kingsmeadow_radius_10(self):
		result = functions.find_stores(self.postcode, 10)
		test = (
			result[-1]['latitude'] 
			== min(store['latitude'] for store in result)
			)
		self.assertTrue(test, 'last store in result should have the lowest' 
			+ 'latitude'
			)

	def test_kingsmeadow_postcode_with_radius_1000(self):
		result = functions.find_stores(self.postcode, 1000)
		self.assertEqual(len(result), 94, 
			'radius 1000 should return all except Bagshot (has nan values)'
			)

	def test_north_south_ordering_all_stores(self):
		result = functions.find_stores(self.postcode, 1000)
		self.assertEqual(result[-1]['name'], 'Eastbourne', 
			'most southerly store should be Eastbourne'
			)

	def test_invalid_postcode(self):
		result = functions.find_stores('xyz', 25)
		self.assertEqual(result, 'Invalid postcode', 
			'invalid postcode should return error message'
			)

	def test_postcode_outside_of_local_area(self):
		result = functions.find_stores('M3 5AL', 50)
		self.assertEqual(len(result), 0, 
			'Manchester postcode should return 0 stores'
			)

if __name__ == '__main__':
	unittest.main()