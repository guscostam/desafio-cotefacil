import scrapy


class CompraSpider(scrapy.Spider):
    name = "compra"
    start_urls = [
        "http://compra-agora.com/loja/alimentos/800",
        "http://compra-agora.com/loja/bazar/344",
        "http://compra-agora.com/loja/bebidas/778",
        "http://compra-agora.com/loja/bomboniere/183",
        "http://compra-agora.com/loja/carnes-e-congelados/1321",
        "http://compra-agora.com/loja/cuidados-pessoais/180",
        "http://compra-agora.com/loja/laticinios/771",
        "http://compra-agora.com/loja/naturais-e-nutricao/1399"
    ]

    def login(self, response):
        yield scrapy.FormRequest.from_response(
            response,
            formdata={
                "username": "04.502.445/0001-20",
                "password": b'$argon2id$v=19$m=65536,t=2,p=1$LVx3/uxO5Z7qIJk3O21mAw$REqARv6Rk1244FvkpWbd4pra8J5eJDwB0nrsDmGG07Q'
            },
            callback=self.after_login
        )

    def after_login(self, response):
        if b'session_id' in response.headers.getlist(b'Set-Cookie'):
            self.log("Login bem sucedido!")
            yield scrapy.Request(callback=self.parse)
        else:
            self.log("Falha no login!")

    def parse(self, response, **kwargs):
        for i in response.css(".box-produto"):
            description = i.css('.produto-nome::text').get().strip()
            manufacturer = i.css('.produto-marca::text').get()
            image_url = i.css('.img-fluid::attr(src)').getall().pop(1)

            yield {
                "description": description,
                "manufacturer": manufacturer,
                "image_url": image_url
            }

