from PIL import Image

logo = Image.open(r"E:\GitHub Repositories\IconCreator\src\icons\app_icon_small.png")

logo.save(r"E:\GitHub Repositories\IconCreator\src\icons\app_icon.ico", format='ICO')