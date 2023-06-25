#from gunicorn.workers.base import Worker
#
#class CustomWorker(Worker):
#    def handle_request(self, listener, req, client, addr):
#        req.MEMFILE_MAX = 50 * 1024 * 1024  # リクエストの最大サイズを設定
#        super().handle_request(listener, req, client, addr)

# gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -c ../gunicorn_conf.py