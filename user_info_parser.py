import requests
import json
import logging
import datetime


logging.basicConfig(filename='logging/debug_user_info_parser.log', level=logging.ERROR)



proxies_list = [
    '7b5b502df6:57507db76b@195.123.212.74:40514',
    'temirlantokaev6:bNvmGjjcmT@109.61.89.1:10115',
    'temirlantokaev6:bNvmGjjcmT@109.61.89.1:10116',
    'temirlantokaev6:bNvmGjjcmT@109.61.89.1:10117',
    'temirlantokaev6:bNvmGjjcmT@109.61.89.1:10118',
    'temirlantokaev6:bNvmGjjcmT@109.61.89.1:10119',
    'temirlantokaev6:bNvmGjjcmT@109.61.89.1:10125',
    'temirlantokaev6:bNvmGjjcmT@109.61.89.1:10126',
    'temirlantokaev6:bNvmGjjcmT@109.61.89.1:10127',
    'temirlantokaev6:bNvmGjjcmT@109.61.89.1:10128',
    'temirlantokaev6:bNvmGjjcmT@109.61.89.1:10129',
    'temirlantokaev6:bNvmGjjcmT@109.61.89.1:10727',
    'temirlantokaev6:bNvmGjjcmT@109.61.89.1:10740',
    'temirlantokaev6:bNvmGjjcmT@109.61.89.1:10741',
    'temirlantokaev6:bNvmGjjcmT@109.61.89.1:10742',
    'temirlantokaev6:bNvmGjjcmT@109.61.89.1:10775',
    'temirlantokaev6:bNvmGjjcmT@109.61.89.1:12216',
    'temirlantokaev6:bNvmGjjcmT@109.61.89.1:12217',
    'temirlantokaev6:bNvmGjjcmT@109.61.89.1:12218',
    'temirlantokaev6:bNvmGjjcmT@109.61.89.1:12219',
    'temirlantokaev6:bNvmGjjcmT@109.61.89.1:12220',

]


selected_proxy = proxies_list[0]


proxy_parts = selected_proxy.split('@')
username_password, ip_port = proxy_parts


username, password = username_password.split(':')


proxies = {
    'http': f'http://{username}:{password}@{ip_port}',
    'https': f'http://{username}:{password}@{ip_port}',
}


user_agent = 'Instagram 201.0.0.32.120 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16E148'



def user_info_parser(owner_id):
    try:
        print(owner_id)
        user_name = get_username_by_owner_id(owner_id)
        user_data = None  

        for proxy_str in proxies_list:
            proxy_parts = proxy_str.split('@')
            username_password, ip_port = proxy_parts
            username, password = username_password.split(':')

            proxies = {
                'http': f'http://{username}:{password}@{ip_port}',
                'https': f'http://{username}:{password}@{ip_port}',
            }

            url = f'https://www.instagram.com/api/v1/users/web_profile_info/?username={user_name}'
            headers = {'User-Agent': user_agent}

            response = requests.get(url, headers=headers, proxies=proxies)

            if response.status_code == 200:
                try:
                    json_data = response.json()
                except json.JSONDecodeError as e:
                    print(f'Ошибка при разборе JSON: {e}')
                    logging.error(f'Ошибка при разборе JSON: {str(e)},{owner_id},{user_name},{response},{response.text},{datetime.datetime.now()}')
                    continue 
                json_str = json.dumps(json_data, indent=4, ensure_ascii=False)

                user_data = json_data.get('data', {}).get('user') 

                if user_data is not None:
                    keys_to_exclude = [
                        'edge_felix_video_timeline',
                        'edge_owner_to_timeline_media',
                        'edge_saved_media',
                        'edge_media_collections',
                        'edge_related_profiles',
                    ]

                    filtered_user_data = {key: value for key, value in user_data.items() if key not in keys_to_exclude}
                    return filtered_user_data
            else:
                print(f'Ошибка запроса через прокси {ip_port}. Код ошибки: {response.status_code} user_info_parser')
    
        if user_data is None:
            print('Не удалось выполнить запрос через ни один прокси.')
        return None
    except Exception as e:
        logging.error(f'Error in user_info_parser: {str(e)},{owner_id},{user_name},{response},{response.text},{datetime.datetime.now()}')

def get_username_by_owner_id(owner_id):
    try:
        print(owner_id)
        for proxy_str in proxies_list:
            proxy_parts = proxy_str.split('@')
            username_password, ip_port = proxy_parts
            username, password = username_password.split(':')

            proxies = {
                'http': f'http://{username}:{password}@{ip_port}',
                'https': f'http://{username}:{password}@{ip_port}',
            }

            url = f'https://i.instagram.com/api/v1/users/{owner_id}/info/'

            headers = {'User-Agent': user_agent}

            response = requests.get(url, headers=headers, proxies=proxies)

            if response.status_code == 200:
                json_data = response.json()
                username = json_data['user']['username']
                print(f'Успешный запрос через прокси {ip_port}. Username: {username}')
                return username
            else:
                print(f'Ошибка запроса через прокси {ip_port}. Код ошибки: {response.status_code} get_username_by_owner_id')
    except Exception as e:
        logging.error(f'Error in get_username_by_owner_id: {str(e)},{owner_id},{response},{response.text},{datetime.datetime.now()}')




            

if __name__ == "__main__":
    print(user_info_parser(2054925448))
 #rint(user_info_parser_for_subscription('zhumabaev.mz'))
