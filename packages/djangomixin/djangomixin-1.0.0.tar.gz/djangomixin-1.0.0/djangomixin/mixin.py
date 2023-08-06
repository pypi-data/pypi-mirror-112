import random, string, os


def bootstrap_visible_fields(visible_fields):
    for visible in visible_fields():
        widget = visible.field.widget
        class_name = widget.__class__.__name__

        if class_name == 'Select':
            widget.attrs['class'] = 'form-select'
        elif class_name == 'CheckboxInput':
            widget.attrs['class'] = 'form-check-input'
        else:
            widget.attrs['class'] = 'form-control'


def random_string(lenght=10):
	chars = string.ascii_lowercase + string.digits
	plus = ''.join(random.choice(chars) for _ in range(lenght))
	dig = range(0,9)
	plus = plus + str(random.randint(0,9))
	return plus


def filename(file):
	return os.path.basename(file)
