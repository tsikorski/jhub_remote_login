import requests
import docker


def tests_auth_hub(hub_container):
    """
    Test that the client is able to,
    - Authenticate with the Remote-User header
    - Once auth'ed, Pass a Mig-Mount header to the jupyterhub
    """
    client = docker.from_env()
    containers = client.containers.list()
    assert len(containers) > 0
    session = requests.session()
    # Not allowed, -> not authed
    no_auth_response = session.get("http://127.0.0.1:8000/hub/home")
    assert no_auth_response.status_code == 401

    # Auth requests
    user_cert = '/C=DK/ST=NA/L=NA/O=NBI/OU=NA/CN=Rasmus ' \
                'Munk/emailAddress=rasmus.munk@nbi.ku.dk'
    cert_auth_header = {
        'Remote-User': user_cert
    }

    auth_response = session.get("http://127.0.0.1:8000/hub/login",
                                headers=cert_auth_header)
    assert auth_response.status_code == 200


def test_auth_mount(hub_container):
    client = docker.from_env()
    containers = client.containers.list()
    assert len(containers) > 0
    session = requests.session()

    no_auth_mount = session.get("http://127.0.0.1:8000/hub/mount")
    assert no_auth_mount.status_code == 401

    # Auth requests
    user_cert = '/C=DK/ST=NA/L=NA/O=NBI/OU=NA/CN=Rasmus ' \
                'Munk/emailAddress=rasmus.munk@nbi.ku.dk'

    cert_auth_header = {
        'Remote-User': user_cert
    }

    auth_response = session.get("http://127.0.0.1:8000/hub/login",
                                headers=cert_auth_header)
    assert auth_response.status_code == 200

    wrong_mig_dict = {'SESSIONS': 's324324234',
                      'WIE': 'dsfsdfs'}
    wrong_mig_header = {
        'Mig-Mount': str(wrong_mig_dict)
    }

    # Random key set
    correct_mig_dict = {'MOUNT_HOST': 'IDMC',
                        'SESSION_ID': 'randomstring_unique_string',
                        'USER_CERT': user_cert,
                        'TARGET_MOUNT_ADDR': '@host.localhost:',
                        'MOUNT_SSH_PRIVATE_KEY': '''-----BEGIN RSA PRIVATE KEY-----
    MIIEpAIBAAKCAQEA00VP99Nbg6AFrfeByzHtC4G2eLZGDCXP0pBG5tNNmaXKq5sU
    IrDPA7fJczwIfMNlqWeoYjEYg46vbMRxwIDXDDA990JK49+CrpwppxWgSE01WPis
    gtqfmaV16z8CS4WmkjSZnUKQf+2Yk9zdBXOOjWLiXBog7dGpUZQUV/j3u262DIl5
    oLGtoy/mljPx3rwGTSqVoavUW2zh7k0tFIhGt/T14E3TuATdUIDAsPmfLVXFFx76
    W0JxYv3uoCGAUOd2pFhqUXDPLYsSG5reWoQ8iXHJS84E8wHAImcLhYccRLg2AT3b
    TXmC1/BX3lfrwXjaBLfMZiUk/cdSLUh6hxtSPQIDAQABAoIBAQDP4SKHYmNohzsv
    axs+OXjZ2p8V9ZvE9iugLzBkjUOMzHI4GlZcsAZxzRQeG9LqGEVew80OGOra/7mi
    10RqOxveNVWzhnoz78ghUS0253OX0MiOK9lqw/1IbGMzvwLeFrrIn5MLBuUxyzJX
    Q3oClCqO+d5q65a9CpCE4aSGz0XLGKGe9iD5Rd1UjVJn/KvZnjObd0WJBAQCoNVU
    VCULblmR/1c+2lL/0Snv3j7w7G6+2H6o1MI3dbBQ0/SCGjw5cJOXYuGZq9YRXfnj
    3WxQW04j39gOtvZqJfCXK8lh+GE2BqgVG/ei9VGV27FshTM/3AkPACvzFZXTnjoP
    2uc5k8fBAoGBAO59ZzJyRYN+qOIRmM4e3ApZCfpUCaxMsksSDvvIVcJHENu4WcA3
    vPBVsnyDmgn5ZpEwXuoYhnMoDIQobob81jiVARG9RRS+4Kd71E2jOr5UBXFDD05R
    yvxh2deZ9T3hNWIE31T/37d3xLGdnkxQ+nqAyNjYAG7IemqxR877kw7tAoGBAOLI
    Tj7Aaa9cBzjmWVfJOExMT8PpDrGg4MGYh7nQFJB37A6SMrC1jXe6ZqwQtouOC+pG
    Jk310lMjAeC3Gokr769CHE40BY347wcMIBQHnKUW3elZx2APswETMyKYsNllnJWe
    j1f7gc5ZMr8bjWMPjRgIbazdrLCM3lv3ITMDNZaRAoGAXi13SxyFBuBFoMCCLyNQ
    kWWH4yq8hyXiYnLHJ/Z8pzOZHKs4Bgf8vIua6ECv27B5KGyJjrgQn/j4uFefDf9a
    OQ3eVjr/xKl73aewttf2oqJbY9avfKYgGnoppFJP3hfJFOQHrXE9zx2ktt8fW9O+
    lhG1PqxNv3G7pdZMHRiLgiECgYEAgyCazYHoGfM2YdofMrkwij1dqcOqMV76VjZh
    1DjSiy4sGcjC8pYndGEdWMRZKJw7m3xwTYej01pcjZiSCVqUPlwVjcpao9qaKxMB
    wVMdaf+s1G6K76pkMGzvlkN/jlRIk+KYs6DDT5MX2pSNzgeB57GH6PpMDdGGCNr+
    IUbrx2ECgYAck/GKM9grs2QSDmiQr3JNz1aUS0koIrE/jz4rYk/hIG4x7YFoPG4L
    D8rT/LeoFbxDarVRGkgu1pz13IQN2ItBp1qQVr4FqbN4emgj73wOWiFgrlRvasYV
    ojR4eIsIc//+fVpkr56fg2OUGhmI+jw87k9hG5uxgBCqOAJuWjEo7A==
    -----END RSA PRIVATE KEY-----'''}

    correct_mig_header = {
        'Mig-Mount': str(correct_mig_dict)
    }

    # Invalid mount header
    auth_mount_response = session.get("http://127.0.0.1:8000/hub/mount",
                                      headers=wrong_mig_header)
    assert auth_mount_response.status_code == 403

    # Valid mount header
    auth_mount_response = session.get("http://127.0.0.1:8000/hub/mount",
                                      headers=correct_mig_header)
    assert auth_mount_response.status_code == 200
