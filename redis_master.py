from time import sleep
from redis import Redis
from rq import Queue
import numpy
from redis_modules import multiplica_linha_coluna, cria_matriz

if __name__ == "__main__":
  print "Initializing redis master"
  redis_conn = Redis(host='127.0.0.1',port=6379)
  queue_jobs = Queue('my_queue', connection=redis_conn)

  linhas, colunas = 2, 2

  matrizA = cria_matriz(linhas, colunas)
  matrizB = cria_matriz(linhas, colunas)

  matrizA = numpy.array(matrizA)
  matrizB = numpy.array(matrizB)

  matrizC = numpy.zeros(shape=(linhas, colunas))

  jobs = []
  for i in range(len(matrizA)):
    jobs_local = []
    for j in range(len(matrizA[0])):
      job = queue_jobs.enqueue(multiplica_linha_coluna, matrizA[i], matrizB[:, j])
      jobs_local.append(job)
    jobs.append(jobs_local)

  for i in range(len(matrizA)):
    for j in range(len(matrizA[0])):
      job = jobs[i][j]
      while job.result is None:
        sleep(2)
      matrizC[i][j] = job.result

  print matrizC