def biggest(my_dict):
	'''Returns the key corresponding to the entry with the longest list attached to it'''

	if len(my_dict) == 0:
		return None

	else:
	
		max_length = 0

		#Finds the length of the longest list among the elements in my_dict

		for l in my_dict.keys():
			if len(my_dict[l]) > max_length:
				max_length = len(my_dict[l])
		
	
		# Extracts a list of keys in my_dict which are attached to lists which length is maxlength
		keys_to_longest_element = [x for x in my_dict.keys() if len(my_dict[x]) == max_length]

		return keys_to_longest_element

weather = { 'a': ['stormy'], 'b': ['sunny'], 'c': ['rainy']}

weather['d'] = ['snowy']
weather['d'].append('windy')
weather['d'].append('cloudy')

print biggest(weather)