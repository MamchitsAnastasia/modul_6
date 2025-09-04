from http.server import HTTPServer, BaseHTTPRequestHandler
import os


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        # Читаю HTML-файл контактов
        try:
            with open('./templates/contacts.html', 'r', encoding='utf-8') as file:
                html_content = file.read()

            # Отправляю ответ
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(html_content.encode('utf-8'))

        except FileNotFoundError:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write('Файл contacts.html не найден'.encode('utf-8'))

    def do_POST(self):
        # Получаю длину содержимого
        content_length = int(self.headers.get('Content-Length', 0))

        # Читаю данные POST-запроса
        post_data = self.rfile.read(content_length)

        # Декодирую данные (предполагаем UTF-8)
        try:
            decoded_data = post_data.decode('utf-8')
        except UnicodeDecodeError:
            decoded_data = str(post_data)

        # Печатаю данные в консоль
        print("=" * 50)
        print("POST-запрос получен:")
        print(f"Путь: {self.path}")
        print(f"Заголовки: {dict(self.headers)}")
        print(f"Данные: {decoded_data}")
        print("=" * 50)

        # Отправляю ответ
        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write('POST-запрос успешно обработан'.encode('utf-8'))


def run_server(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Сервер запущен на порту {port}')
    print('Для остановки сервера нажмите Ctrl+C')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('\nСервер остановлен')
        httpd.shutdown()


if __name__ == '__main__':
    # Проверяю, существует ли файл contacts.html
    if not os.path.exists('./templates/contacts.html'):
        print("Ошибка: Файл contacts.html не найден")
    else:
        run_server()