import re
from requests_html import HTMLSession


def main():
    session = HTMLSession()
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'}

    url_us = 'https://www.newegg.com/seagate-barracuda-2tb-st2000lm015/p/N82E16822179107'
    index = url_us.find('.com/') + 5
    url_uy = url_us[:index] + 'global/uy-en/' + url_us[index:]
    url_cotizacion = 'https://www.brou.com.uy/cotizaciones'

    response_us = session.get(url_us, headers=header)
    response_uy = session.get(url_uy, headers=header)
    response_cotizacion = session.get(url_cotizacion, headers=header)
    response_cotizacion.html.render(sleep=.1)

    product_title = re.search("product_title:\\['(.+?)'\\]", response_us.html.html).group(1)

    selector = 'meta[itemprop=price][content]'
    price_us = float(response_us.html.find(selector, first=True).attrs['content'])
    price_uy = float(response_uy.html.find(selector, first=True).attrs['content'])

    shipping_uy = float(re.search("product_default_shipping_cost:\\['(.+?)'\\]", response_uy.html.html).group(1))
    shipping_us = float(re.search("product_default_shipping_cost:\\['(.+?)'\\]", response_us.html.html).group(1))
    if shipping_us <= 0.01:
        shipping_us = 0

    cotizacion = float(re.findall('"valor"> (.+?) <', response_cotizacion.html.html)[1].replace(',', '.'))
    price_us_to_uy = round(price_us * cotizacion, 2)

    print(f'Producto: {product_title}')
    print(f'Precio USA: USD {price_us} ($ {price_us_to_uy} a cotizacion {cotizacion})\n\tShipping: {shipping_us}\n\tTotal: {price_us + shipping_us}')
    print(f'Precio UY: $ {price_uy} Diferencia: $ {round(price_uy - price_us_to_uy, 2)}\n\tShipping: {shipping_uy}\n\tTotal: {price_uy + shipping_uy}')


if __name__ == "__main__":
    main()
