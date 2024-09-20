import time, logging
import grpc
import books_pb2
import books_pb2_grpc


logging.basicConfig(level=logging.INFO, format='Client | %(asctime)s - %(levelname)s - %(message)s')


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        
        logging.info('Успешное подключение к сервису')
        stub = books_pb2_grpc.BookServiceStub(channel)

        response = stub.getBookById(books_pb2.BookRequest(id=1))
        logging.info(f"Client | Книга: \nID: {response.id},\nНазвание: {response.title},\nАвтор: {response.author}")

        response = stub.getAllBooks(books_pb2.EmptyRequest())
        for book in response.books:
            logging.info(f"Client | Книга: \nID: {book.id},\nНазвание: {book.title},\nАвтор: {book.author}")


if __name__ == '__main__':
    run()
