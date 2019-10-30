from re import search, findall
from requests_html import HTMLSession
from sys import argv


def main():
    session = HTMLSession()
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'
    }

    url = argv[1]
    url_us = search('(https://www.newegg.com/.+?/p/.+?)\\?', url).group(0)
    index = url_us.find('.com/') + 5
    url_uy = url_us[:index] + 'global/uy-en/' + url_us[index:]
    url_cotizacion = 'https://www.brou.com.uy/cotizaciones'

    response_us = session.get(url_us, headers=header)
    response_uy = session.get(url_uy, headers=header)
    response_cotizacion = session.get(url_cotizacion, headers=header)
    response_cotizacion.html.render(sleep=.5)

    product_title = search("product_title:\\['(.+?)'\\]", response_us.html.html).group(1)

    selector = 'meta[itemprop=price][content]'
    price_us = float(response_us.html.find(selector, first=True).attrs['content'])
    price_uy = float(response_uy.html.find(selector, first=True).attrs['content'])

    shipping_us = float(search("product_default_shipping_cost:\\['(.+?)'\\]", response_us.html.html).group(1))
    shipping_uy = float(search("product_default_shipping_cost:\\['(.+?)'\\]", response_uy.html.html).group(1))
    if shipping_us <= 0.01:
        shipping_us = 0

    total_us = round(price_us + shipping_us, 2)
    total_uy = round(price_uy + shipping_uy, 2)

    cotizacion = float(findall('"valor"> (.+?) <', response_cotizacion.html.html)[1].replace(',', '.'))
    price_us_to_uy = round(total_us * cotizacion, 2)
    difference_us_to_uy = round(total_uy - price_us_to_uy, 2)

    print(f'Producto: {product_title}')
    print(f'Precio USA: USD {price_us}\n\tShipping: USD {shipping_us}\n\tTotal: USD {total_us} ($ {price_us_to_uy} a cotizacion {cotizacion})')
    print(f'Precio UY: $ {price_uy}\n\tShipping: $ {shipping_uy}\n\tTotal: $ {total_uy}')
    print(f'Diferencia total: {difference_us_to_uy}')


if __name__ == "__main__":
    main()
