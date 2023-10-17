from dataset_func import DataBase
from user_info_parser import user_info_parser
from user_following_parser_old import get_user_following
import json
import time
import logging


logging.basicConfig(filename='logging/debug_base_model.log', level=logging.ERROR)



database = DataBase()


#16730109633


def main():
    for result in database.select_user_source_res_id():

        try:
            res_id, source_id = result
            json_data = user_info_parser(source_id)
            if json_data is not None:
                json_data_str = json.dumps(json_data, ensure_ascii=False)
                database.insert_source_user_profile(
                    res_id=res_id,
                    username=json_data.get('username', ''),
                    deactivated=None,
                    is_closed=(1 if json_data.get('is_private', False) else 0),
                    sex=None,
                    birth_date=None,
                    profile_image=json_data.get('profile_pic_url', ''),
                    info_json=json_data_str
                )
                print(f'Данные пользователя {json_data.get("username", "")} записаны.')

                if not json_data['is_private']:
                    following_parser(res_id, source_id, int(json_data['edge_follow']['count']))
            else:
                database.insert_source_user_profile(
                    res_id=res_id,
                    username='None',
                    deactivated='deleted',
                    is_closed=1,
                    sex=None,
                    birth_date=None,
                    profile_image=None,
                    info_json=None
                )
                print(f'Данные пользователя {res_id} {source_id} не записаны, аккаунт удален или забанен')
        except Exception as e:
            logging.error(f'Error in main: {str(e)}')
            continue
        time.sleep(60)

def following_parser(user_res_id, owner_id, following_count):
    print(owner_id, following_count)

    json_data = get_user_following(owner_id, following_count)
    print(json_data)

    for index, user in enumerate(json_data, start=1):
        owner_id_followings = int(user['pk'])
        username = str(user['username'])
        print(index, username)
        database.insert_source_info(owner_id_followings)
        res_id_followings = database.get_source_id(owner_id_followings)
        database.insert_source_user_subscription(user_res_id, res_id_followings)
        print(owner_id_followings, username,res_id_followings)
        
        print('user:' ,user)
        
        try:
            if json_data is not None:
                json_data_str = json.dumps(user, ensure_ascii=False)
                print(json_data_str, user.get('full_name', ''),user.get('is_private',''),user.get('profile_pic_url', ''))
                database.insert_source_subscription_profile(
                    res_id=res_id_followings,
                    subscription_name=user.get('full_name', ''),
                    deactivated=None,
                    is_closed=(1 if user.get('is_private', False) else 0),
                    members_count=None,
                    profile_image=user.get('profile_pic_url', ''),
                    info_json=json_data_str
                )
            else:
                database.insert_source_subscription_profile(
                    res_id=res_id_followings,
                    subscription_name=None,
                    deactivated='deleted',
                    is_closed=1,
                    members_count=None,
                    profile_image=None,
                    info_json=None
                )
                print(f'Данные пользователя {username} не записаны, аккаунт удален или забанен')
            if index < len(following_users):
                time.sleep(1)
        except Exception as e:
            logging.error(f'Error in following_parser: {str(e)}')




if __name__ == "__main__":
    main()

