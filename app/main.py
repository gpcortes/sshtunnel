import envconfiguration as config
from ssh import SSHTunnel

@SSHTunnel(
    config.TUNNEL_USERNAME,
    config.TUNNEL_PASSWORD,
    config.TUNNEL_GATEWAY,
    config.TUNNEL_GATEWAY_PORT,
    config.TUNNEL_REMOTE_HOST, 
    config.TUNNEL_REMOTE_PORT, 
    config.TUNNEL_LOCAL_HOST,
    config.TUNNEL_LOCAL_PORT
)
def connect():
    pass

if __name__ == '__main__':
    connect()