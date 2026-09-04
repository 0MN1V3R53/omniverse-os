from PIL import Image
import glob

def remove_white_background(img_path):
    try:
        img = Image.open(img_path)
        img = img.convert("RGBA")
        datas = img.getdata()
        
        newData = []
        for item in datas:
            # Change all white (also shades of white)
            # to transparent
            if item[0] > 240 and item[1] > 240 and item[2] > 240:
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)
                
        img.putdata(newData)
        img.save(img_path, "PNG")
        print(f"Processed {img_path}")
    except Exception as e:
        print(f"Failed to process {img_path}: {e}")

if __name__ == '__main__':
    paths = [
        "./sky_next/out/assets/images/logo.png",
        "./sky_next/public/assets/images/logo.png",
        "./hostinger_site/public_html/assets/images/logo.png",
        "./assets/images/logo.png",
        "./public_html_local/assets/images/logo.png"
    ]
    for p in paths:
        remove_white_background(p)
