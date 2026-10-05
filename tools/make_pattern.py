from PIL import Image, ImageEnhance
src=Image.open('brand/profile-monogram.png').convert('RGB')
P=235
t=Image.new('RGB',(P,P))
t.paste(src.crop((0,100,190,100+P)),(0,0)); t.paste(src.crop((895,100,940,100+P)),(190,0))
t=ImageEnhance.Brightness(t).enhance(0.75)
t.save('images/blog/pattern.png')
