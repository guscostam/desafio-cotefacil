import scrapy
from scrapy.utils.response import open_in_browser
import json


class ServimedSpiderSpider(scrapy.Spider):
    name = "servimed_spider"
    number = "511082"

    def start_requests(self):
        data = {
            "usuario":"juliano@farmaprevonline.com.br",
            "senha":"a007299A"
        }
        yield scrapy.FormRequest(
            url='https://peapi.servimed.com.br/api/usuario/login',
            formdata=data,
            callback=self.login
        )

    def login(self, response):
        yield scrapy.Request(
            url='https://pedidoeletronico.servimed.com.br/',
            callback=self.after_login
        )

    def after_login(self, response):
        session_cookie = None
        for cookie in response.request.headers.getlist('Cookie'):
            if b'session' in cookie:
                session_cookie = cookie.decode('utf-8')
                break

        yield scrapy.FormRequest(
            url='https://peapi.servimed.com.br/api/Pedido',
            headers={'cookie': session_cookie, 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36', 'sec-ch-ua-plataform': 'Windows', 'origin': 'https://pedidoeletronico.servimed.com.br', 'referer': 'https://pedidoeletronico.servimed.com.br/'},
            formdata={
                "dataInicio":"",
                "dataFim":"",
                "filtro":"",
                "pagina":bytes(1),
                "registrosPorPagina":bytes(10),
                "codigoExterno":bytes(267511),
                "codigoUsuario":bytes(22850),
                "kindSeller":bytes(0),
                "users":[bytes(267511),bytes(518565)]
            },
            callback=self.order
        )
    def order(self, response):
        print('ok')