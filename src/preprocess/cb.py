def dict_to_list(object):
	if type(object[0]) == dict:
		object[0] = [object[0]]

	return object