# Web Server Using Thread Pool 
 A program that simulates a web server using a thread pool.

The program accepts requests from clients through a socket, and process them using a fixed number of worker threads.
• If the request is valid, the worker thread sends back a response with the content of the requested file, or a 404 error if the file does not exist.
• If the request is invalid, the worker thread sends back a response with a 400 error.
• If the thread pool is full, the program rejects new requests with a 503 error.
• If the program receives a SIGINT signal, it terminates all the threads and closes the socket.