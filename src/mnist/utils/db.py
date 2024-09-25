import pymysql.cursors
import os


def get_db_connection():
    return pymysql.connect(
            #ip, port 설정은 어떻게 해야하지?
        host=os.getenv("DB_IP", "172.17.0.1"), #localhost = 127.0.0.1
        # docker network 에서 docker host를 설치한 후 host의 network interface를
        # 보면 docker0이라는 interface를 볼수 있다 `$ipconfig`
        # docker0 interface의 default ip 가 172.17.0.1 이다

        #결론적으로 container가 외부로 통신할 때는 무조건 docker0 interface를 지나야 한다.
        port=int(os.getenv("DB_PORT", "53306")),
        user=os.getenv("DB_USER", "mnist"),
        password=os.getenv("DB_PASSWORD", "1234"),
        database=os.getenv("DB_DATABASE", "mnistdb"),
    )
