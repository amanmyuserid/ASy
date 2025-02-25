import trafilatura


def extract_website_content(url: str, output_file: str) -> bool:
    """
    Yeh function static websites se main content extract karta hai using Trafilatura.
    Agar extraction successful hoti hai, toh content ko output_file mein save karke True return karega.
    Agar koi issue aaye ya content extract na ho, toh False return karega.
    Note: Yeh function JavaScript-rendered content ko handle nahi karta.
    """
    try:
        # URL se HTML content fetch karo
        downloaded = trafilatura.fetch_url(url)
        if downloaded is None:
            print(f"Failed to fetch content from {url}")
            return False

        # Trafilatura se main content extract karo
        text_content = trafilatura.extract(downloaded)
        if text_content is None:
            print(f"Failed to extract content from {url}")
            return False

        # Extracted content ko specified text file mein save karo
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(text_content)
        
        return True

    except Exception as e:
        print("Error occurred:", e)
        return False
