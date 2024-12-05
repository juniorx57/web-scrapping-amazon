import requests
from bs4 import BeautifulSoup
import lxml
import smtplib
import os
from dotenv import load_dotenv

dotenv = load_dotenv(
    dotenv_path=".env",
    verbose=True)


MEU_EMAIL = os.getenv("MEU_EMAIL")
SENHA = os.getenv("MINHA_SENHA")
DESTINATARIO = os.getenv("EMAIL_DESTINATARIO")
PRECO_ALVO = 100
PROD_URL="https://www.amazon.com/dp/B075CYMYK6?ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6&th=1"
HEADERS ={
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}

response = requests.get(url=PROD_URL, headers=HEADERS)
product_webpage = response.text
soup = BeautifulSoup(product_webpage,"lxml")

product = soup.find(name="span", class_="aok-offscreen")
current_price = float(product.getText().split("$")[1])

title = soup.find(name="span", id="productTitle", class_="a-size-large product-title-word-break")
current_title = title.getText().strip()


if current_price < PRECO_ALVO:
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=MEU_EMAIL, password=SENHA)
        connection.sendmail(
            from_addr=MEU_EMAIL,
            to_addrs=DESTINATARIO,
            msg=f"Assunto: Oferta Amazon! "
                f"\n\n {current_title} está por apenas {current_price}. "
                f"\n\nCompre agora: "
                f"\n\n{PROD_URL}".encode("utf-8")
        )