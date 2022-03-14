from rembg import remove
from PIL import Image

input_path = 'images/person.png'
output_path = 'images/output.png'

input = Image.open(input_path)
output = remove(input)
output.save(output_path)