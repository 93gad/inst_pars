import requests
import time
import logging


logging.basicConfig(filename='logging/debug_user_following_parser_old.log', level=logging.ERROR)


user_agent = 'Instagram 200.0.0.32.120 (iPhone; CPU iPhone OS 13_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E149'


session_id_proxy_mapping = {
    '61889963708%3A1r7x0gK4j15u9g%3A23%3AAYfeJHL4kZkf5AG91RLSpxxhC8bIk_binb12wjyMrA': 'temirlantokaev6:bNvmGjjcmT@109.61.89.1:10742',
    '62217821685%3Arj6cbXaP0nwF4U%3A8%3AAYfpniob4Qyvuwy5Yxju29RAdydB7Um-ZKUfB-FwEQ': 'temirlantokaev6:bNvmGjjcmT@109.61.89.1:10740',
    '62296562936%3A69y39v7yvfQAg7%3A23%3AAYcxmOVYAFPvwFh8z75MLcFMe1DWbgWPJTW4bWxr4w': 'temirlantokaev6:bNvmGjjcmT@109.61.89.1:10115',
    '62408066593%3ApCtc5bmivKcUOa%3A15%3AAYfc7j2enWbpRjQkVOCuJGMTQpuDAjEREbMmA-wDuA': 'temirlantokaev6:bNvmGjjcmT@109.61.89.1:10116',
    '62427708853%3ARQBOGMD7FB8fuq%3A3%3AAYfby3-X6D8y_voPr_zb7CPsXRqVUrapWfxYx6DcAQ': 'temirlantokaev6:bNvmGjjcmT@109.61.89.1:10117',
    '61901511544%3Au6SnfSjJ26wIrm%3A3%3AAYfMjZJMIMRw_msRjz3lvnt67GyLV1GKFO34PmCASw': 'temirlantokaev6:bNvmGjjcmT@109.61.89.1:10118',
    '62217821685%3AAX3V7zI1G4oOOz%3A4%3AAYfrYVuosYwmU3eDnPiuP3CfI7qAGG_douS0nvXSAw': 'temirlantokaev6:bNvmGjjcmT@109.61.89.1:12217',
    '62646790226%3AuYFJJAVIdXR4Fe%3A27%3AAYcmu5Uwuo16PXdMfhpddrRFWwWkj9NZHxCvXQSWGQ': 'temirlantokaev6:bNvmGjjcmT@109.61.89.1:10775',
    '62693984540%3AXAw4HZefCfwUqh%3A20%3AAYcZtPeifJYsQOUw0oA_kZjFvIGcpxiSFWTXV6Ek4w': 'temirlantokaev6:bNvmGjjcmT@109.61.89.1:10125',
    '62121359225%3ADeYR5MRhyFJsUa%3A10%3AAYfhvUP2Cd_2EIV5g1JAjWEYRWoB9UVgHEsTFoGg_w': 'temirlantokaev6:bNvmGjjcmT@109.61.89.1:10126',
    '62696320605%3AQeaYxJGNMPXNIQ%3A21%3AAYfeaDWtdYihOdT4d4HGKgDDGhB-4R6VD313GA064A': 'temirlantokaev6:bNvmGjjcmT@109.61.89.1:10119',
    '62682377861%3A6LaPrX7j5bxz7b%3A0%3AAYeIze98LhWBBshoOLLe1N26cmjesccCssa2I15CtQ': 'temirlantokaev6:bNvmGjjcmT@109.61.89.1:10127',
    '62686225480%3ApwT94zzUSevSfs%3A22%3AAYcZx-aBNpe58cEaHv1Z2S3GmV4aAo9PiFRPDN7M9w': 'temirlantokaev6:bNvmGjjcmT@109.61.89.1:10128',
    '62358472389%3AD7MnVpm8dsIEFG%3A21%3AAYe6b2IayI6Sywi_7q9zocOs4czfYk0mK3zgKPgKeQ': 'temirlantokaev6:bNvmGjjcmT@109.61.89.1:10129',
    '62476925820%3A4daeWxHaOMjDdu%3A21%3AAYfHlSbTldYF7AykyH0go7E2arUA4dgS1L-iZBgRzg': 'temirlantokaev6:bNvmGjjcmT@109.61.89.1:10727',
    '62324390017%3AzV9IUSnDv5WKAa%3A25%3AAYdPy_708f7U92hYHSZuOriOSqPjyOF9UTfhIIuk2Q': 'temirlantokaev6:bNvmGjjcmT@109.61.89.1:10741',
    
    
}



def get_user_following_(owner_id, following_count, session_id, proxies, max_id=None):
    if max_id is None:
        max_id = 0

    total_users = 0
    users_list = []

    while total_users < following_count:
        url = f'https://www.instagram.com/api/v1/friendships/{owner_id}/following/?count=200&max_id={max_id}'

        try:
            req = requests.get(url=url, headers={'User-Agent': user_agent}, cookies={'sessionid': session_id}, proxies=proxies, timeout=10)

            if req.status_code == 200:
                response_json = req.json()

                users = response_json.get('users', [])
                if not users:
                    print('Данные закончились')
                    break
                for user in users:
                    user_data = {
                        'pk': user.get('pk'),
                        'full_name': user.get('full_name'),
                        'username': user.get('username'),
                        'profile_pic_url': user.get('profile_pic_url'),
                        'is_private': user.get('is_private', False)
                    }
                    users_list.append(user_data)

                total_users += len(users)
                max_id += 200
            else:
                print('Ошибка запроса', req.text)
                break
        except requests.exceptions.RequestException as e:
            print(e)
            logging.error(f'Error in get_user_following_: {str(e)}, {owner_id}, {following_count}, {session_id}, {proxies},{req},{req.text}')
    return users_list

def get_user_following(owner_id, following_count):
    for session_id, proxy in session_id_proxy_mapping.items():
        username_password, ip_port = proxy.split('@')
        username, password = username_password.split(':')

        proxies = {
            'http': f'http://{username}:{password}@{ip_port}',
            'https': f'http://{username}:{password}@{ip_port}',
        }

        try:
            following_users = get_user_following_(owner_id, following_count, session_id, proxies)
            if len(following_users) > 0:
                print(f"Session ID: {session_id}, Количесто подписок пользователя: {len(following_users)}")
                return following_users
        except Exception as e:
            logging.error(f'Error in get_user_following: {str(e)}')


if __name__ == "__main__":
    get_user_following(202673987, 377)