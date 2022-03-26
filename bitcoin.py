#!/usr/bin/env python3
class Error(Exception):
    pass

class ParametroIncorreto(Error):
    def __init__(self, arg, msg):
        self.arg = arg

try:
    import sys
    import locale
    from requests import get

    args = sys.argv

    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    symbols = {
        "ETH": "Eth ",
        "USD": "$ ",
        "GBP": "£",
        "EUR": "€",
        "JPY": "¥",
        "CNY": "¥",
        "AUD": "$",
        "CAD": "$",
        "BRL": "R$ ",
        "DOT": "Dot "
    }


    RED = "\033[1;31m"
    BLUE = "\033[1;34m"
    CYAN = "\033[1;36m"
    GREEN = "\033[0;32m"
    RESET = "\033[0;0m"
    BOLD = "\033[;1m"
    REVERSE = "\033[;7m"
    NEGRITO = "\u001b[1m"
    FUNDO = "\u001b[37;1m"
    dashes = FUNDO + "--------------------------------------------------" + RESET
    moedasSuportadas = [
        "btc",
        "eth",
        "ltc",
        "bch",
        "bnb",
        "eos",
        "xrp",
        "xlm",
        "link",
        "dot",
        "yfi",
        "usd",
        "aed",
        "ars",
        "aud",
        "bdt",
        "bhd",
        "bmd",
        "brl",
        "cad",
        "chf",
        "clp",
        "cny",
        "czk",
        "dkk",
        "eur",
        "gbp",
        "hkd",
        "huf",
        "idr",
        "ils",
        "inr",
        "jpy",
        "krw",
        "kwd",
        "lkr",
        "mmk",
        "mxn",
        "myr",
        "ngn",
        "nok",
        "nzd",
        "php",
        "pkr",
        "pln",
        "rub",
        "sar",
        "sek",
        "sgd",
        "thb",
        "try",
        "twd",
        "uah",
        "vef",
        "vnd",
        "zar",
        "xdr",
        "xag",
        "xau",
        "bits",
        "sats"
    ]
    coingecko_api = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies="
    include_24hr_change = "&include_24hr_change=true"
    include_last_updated_at = "&include_last_updated_at=true"

    def formatarValor(cripto, btc):
        if(cripto == "eth"):
            amount = locale.format_string(
                "%20.6f", round(float(btc[cripto]), 8), grouping=True
            ).strip()
            if len(amount.split(".")[0]) == 1:
                amount += "000000000"
        elif(cripto == "dot"):
            amount = locale.format_string(
                    "%10.2f", round(float(btc[cripto]), 2), grouping=True
                ).strip()
            if len(amount.split(".")[1]) == 1:
                amount += "0"
        else:
            amount = locale.format_string(
                "%10.2f", round(float(btc[cripto]), 2), grouping=True
            ).strip()
            if len(amount.split(".")[1]) == 1:
                amount += "0"
        return amount

    def bitcoin(**kwargs):
        try:
            cripto = kwargs.get("currency").lower()
            if(not(moedasSuportadas.__contains__(cripto))):
                raise ParametroIncorreto(cripto, " - Opção de moeda inválida")
            btc = get(f"{coingecko_api}{cripto}{include_24hr_change}")
            btc = btc.json()["bitcoin"]
            amount = formatarValor(cripto,btc)
            symbol = symbols.get(cripto.upper()) or ""
            preco24f = str(round(btc[f'{cripto}_24h_change'], 2)).replace('-', '')
            preco24 = btc[f'{cripto}_24h_change']
            print(dashes)
            print(NEGRITO + BLUE + f"Preço Bitcoin em {cripto.upper()}:")
            print(f"{CYAN+symbol}{amount+RESET}")
            print(dashes)
            print(BLUE + "Variação de preço em 24h")
            if preco24 >= 0:
                print(GREEN + NEGRITO + "+ " + f"{preco24f} % ")
            else:
                print(RED + NEGRITO +   "- " + f"{preco24f} % ")
            print(dashes)  
        except KeyError as error:
            print(error.__str__())
        except NameError as error:
            print(error.__str__())
        except TypeError as error:
            print(error.__str__())
        except ParametroIncorreto as error:
            print("Parametro inválido" + error.__str__())
    try:
        currency = args[1]
    except IndexError:
        currency = "brl"
    finally:
        bitcoin(currency=currency)
except KeyboardInterrupt:
    print(" Exiting...")
