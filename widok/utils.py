def link_check(path):
    from PIL import Image
    import requests
    from io import BytesIO

    if path.startswith('https://') and path.endswith(('.jpg', '.png', '.jpeg')):
        try:
            response = requests.get(path)
            img = Image.open(BytesIO(response.content))

        except:
            error = "Nie można pobrać obrazu (link jest niepoprawny)"
            return False, error
        w, h = img.size
        if w >= 640 and h >= 480:
            return True, False
        else:
            error = 'obraz ma za niską rozdzielczość (min 640x480px)'


    else:
        error = "Link jest niepoprawny lub niebezpieczny"

    return False, error