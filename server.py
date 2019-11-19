import asyncio

class ClientServerProtocol(asyncio.Protocol):

    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print(f'Новое подключение {peername}')


        self.transport = transport

    def data_received(self, data):
        message = data.decode()

        answer = process_data(message)

        print(message)
        print(answer)
        self.transport.write(answer.encode())

        # self.transport.close() (?)

FOLDER = dict()

def process_data(data):
    if data.startswith('get'):
        try:
            return get_processor(*data.split()[1:])
        except Exception:
            return 'error\nwrong command\n\n'
    if data.startswith('put'):
        try:
            return put_processor(*data.split()[1:])
        except Exception:
            return 'error\nwrong command\n\n'
        #return put_processor(*data.split()[1:])
    return 'error\nwrong command\n\n'

def get_processor(key):

    res_str = 'ok\n'

    if key == '*':
        metrics = list()

        for key_ in FOLDER:
            for tup_ in FOLDER[key_]:
                string_data = [key_, *tup_]
                metrics.append(' '.join(map(str, string_data)))

        ending = '\n\n'
    elif key in FOLDER.keys():
        #string_data = [key, *tup_]
        metrics = list(' '.join(map(str, [key,*tup_])) for tup_ in FOLDER[key])
        ending = '\n\n'
    else:
        metrics, ending = list(), '\n'

    return res_str + '\n'.join(metrics) + ending

def put_processor(key, value, timestamp):


    if key not in FOLDER.keys():
        FOLDER[key] = []

    new_metrica = (float(value), int(timestamp))

    if new_metrica not in FOLDER[key]:
        FOLDER[key].append(new_metrica)

    return 'ok\n\n'


def run_server(host, port):

    loop = asyncio.get_event_loop()
    coro = loop.create_server(ClientServerProtocol, host, port)
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass


    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()

if __name__ == '__main__':
    run_server('127.0.0.1', 8888)
