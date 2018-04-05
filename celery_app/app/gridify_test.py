import random
from service import gridify, ServiceError

class ServiceError(Exception):
    """Custom exception for service errors"""
    pass

if __name__ == '__main__':

    iterations = 1000
    x_max = 700000
    y_max = 1300000

    for task_execution in range(iterations):

        x = random.randint(0, x_max)
        y = random.randint(0, y_max)

        try:
            gridify(x, y)
        except ServiceError as se:
            pass
        except Exception as e:
            print(e)





