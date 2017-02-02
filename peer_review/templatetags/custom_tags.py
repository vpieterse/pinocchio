from django	import template

register = template.Library()

counter_var = 0 # Global count variable

@register.simple_tag
def counter_inc(): # Increment
	global counter_var
	counter_var += 1
	return ''

@register.simple_tag
def counter_dec(): # Decrement
	global counter_var
	if counter_var > 0: 
		counter_var -= 1
	return ''

@register.simple_tag
def counter_get(): # Getter
	global counter_var
	return int(counter_var)

@register.simple_tag
def counter_reset(): # Resest Count Variable
	global counter_var
	counter_var = 0
	return ''

@register.inclusion_tag('peer_review/rounditem.html')
def round_load(teamData):
	return {'team': teamData}

