from django	import template

register = template.Library()

@register.simple_tag
def var_counter(var): 
	nm = 1996
	return var + 3

@register.filter
def to_int(value): 
	return int(value)

@register.simple_tag
class Counter:
    count = 0

    def inc(self): # Increment
        self.count += 1
        return ''

    def dec(self): # Decrement
        if self.count > 0: 
            self.count -= 1
        return ''

    def get(self): # Getter
        return self.count

