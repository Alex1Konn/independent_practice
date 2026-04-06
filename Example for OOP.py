import requests
import time


class StockPortfolio:
    all_portfolios = []

    def __init__(self, owner_name, api_key):
        self._api_key = api_key
        self.owner = owner_name
        StockPortfolio.all_portfolios.append(self)

    # 🔥 РЕАЛЬНЫЙ ЗАПРОС К API
    def _fetch_price(self, ticker):
        url = "https://www.alphavantage.co/query"

        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": ticker,
            "apikey": self._api_key
        }

        print(f"📡 Запрос к API для {ticker}...")

        try:
            response = requests.get(url, params=params, verify=False)
            data = response.json()

            # Проверяем, пришла ли цена
            if "Global Quote" in data and "05. price" in data["Global Quote"]:
                price = float(data["Global Quote"]["05. price"])
                return price

            # Обработка ошибок API
            elif "Note" in data:
                print(f"⚠️ Лимит запросов превышен! Подождите минуту. ({data['Note']})")
                return None

            elif "Information" in data:
                print(f"ℹ️ Сообщение от API: {data['Information']}")
                return None

            else:
                print(f"❌ Не удалось найти цену для {ticker}. Ответ: {data}")
                return None

        except Exception as e:
            print(f"💥 Ошибка соединения: {e}")
            return None

    def add_stock(self, ticker, quantity):
        price = self._fetch_price(ticker)

        if price is None:
            print(f"❌ Не удалось добавить {ticker} (нет цены).")
            return

        # Пауза 12 секунд для соблюдения лимита бесплатного API (5 запросов в минуту)
        print("⏳ Ожидание 12 сек (лимит API)...")
        time.sleep(12)

        stock_data = {
            "quantity": quantity,
            "price": price,
            "total_value": price * quantity
        }

        setattr(self, ticker, stock_data)
        print(f"✅ Добавлено: {ticker} ({quantity} шт. по ${price:.2f})")

    def get_total_value(self):
        total = 0
        print(f"\n💼 Отчет для {self.owner}:")

        has_stocks = False
        for attr_name, attr_value in self.__dict__.items():
            # Ищем только словари с данными об акциях
            if isinstance(attr_value, dict) and "total_value" in attr_value:
                value = attr_value["total_value"]
                total += value
                print(f"   - {attr_name}: {attr_value['quantity']} шт. x ${attr_value['price']:.2f} = ${value:.2f}")
                has_stocks = True

        if not has_stocks:
            print("   (Портфель пуст)")

        print(f"💰 Общая стоимость: ${total:.2f}\n")
        return total

    @classmethod
    def create_demo(cls, owner_name):
        # Ключ уже встроен, но лучше использовать глобальную переменную
        return cls(owner_name, "DEMO_KEY")


# ==========================================
# 🚀 ЗАПУСК
# ==========================================

# 1. ТВОЙ КЛЮЧ
MY_API_KEY = "MY_SECRET_KEY"

# Проверка: если ключ равен твоему реальному ключу, то запускаем код!
# (Раньше было наоборот, поэтому код не запускался)
if MY_API_KEY == "MY_SECRET_KEY":
    print("✅ Ключ найден! Запускаем портфель...\n")

    # Создаем портфель
    my_portfolio = StockPortfolio("Alex", MY_API_KEY)

    # Добавляем акции
    # Внимание: между ними будет пауза 12 секунд из-за лимитов Alpha Vantage
    my_portfolio.add_stock("AAPL", 5)  # Apple
    my_portfolio.add_stock("MSFT", 3)  # Microsoft

    # Выводим отчет
    my_portfolio.get_total_value()

    print(f"🌍 Всего создано портфелей: {len(StockPortfolio.all_portfolios)}")

else:
    print("⚠️ Ошибка: Ключ не совпадает с ожидаемым.")