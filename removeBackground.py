from rembg import remove
from PIL import Image

input_path = 'images/person.png'
output_path = 'images/output.png'

input = Image.open(input_path)
output = remove(input)
#reformate to 400x400 and make sure oriantation is correct
output.save(output_path)