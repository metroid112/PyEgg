from re import search, findall
from requests_html import HTMLSession
from sys import argv


def main():
    session = HTMLSession()
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
        'Connection': 'close'
    }

    url = argv[1]
    response_offer = session.get(url, headers=header)
    cotizacion = 0

    products_id = findall('https://www.newegg.com/Product/Product.aspx\\?Item=(.+?)&', str(response_offer.html.absolute_links))
    for product_id in products_id:
        url_us = f'https://www.newegg.com/p/{product_id}'
        index = url_us.find('.com/') + 5
        url_uy = url_us[:index] + 'global/uy-en/' + url_us[index:]
        url_cotizacion = 'https://www.brou.com.uy/cotizaciones'

        response_us = session.get(url_us, headers=header)
        response_uy = session.get(url_uy, headers=header)
        if cotizacion == 0:
            response_cotizacion = session.get(url_cotizacion, headers=header)
            response_cotizacion.html.render(sleep=1, retries=1)

        try:
            title_pattern = "product_title:\\['(.+?)'\\]"
            warning_pattern = '<div class="errorMsgWarning"'
            warning2_pattern = '<div class="flags-body has-icon-left fa-star"'

            product_title = search(title_pattern, response_us.html.html).group(1)

            warning = search(warning_pattern, response_uy.html.html)
            warning2 = search(warning2_pattern, response_uy.html.html)
            if warning is None and warning2 is None:
                price_pattern = '"price":"(.+?)",'
                shipping_pattern = "product_default_shipping_cost:\\['(.+?)'\\]"

                price_us = float(search(price_pattern, response_us.html.html).group(1))
                price_uy = float(search(price_pattern, response_uy.html.html).group(1))

                shipping_us = float(search(shipping_pattern, response_us.html.html).group(1))
                shipping_uy = float(search(shipping_pattern, response_uy.html.html).group(1))
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
            else:
                print(f'Producto {url_uy} no disponible en Uruguay')
        except AttributeError:
            print(f'Producto {url_uy} no disponible en Uruguay')


if __name__ == "__main__":
    main()
