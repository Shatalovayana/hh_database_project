from utils import save_data_to_database, config


def main():
    params = config()
    save_data_to_database(database_name='HeadHunter', params=params)


if __name__ == '__main__':
    main()
