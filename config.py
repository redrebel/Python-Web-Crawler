import configparser


class Config:
    # default = None
    def load(config_file):
        _config = configparser.ConfigParser()
        _config.read(config_file)
        default = 'Default'
        Config.mode = _config.get(default, 'mode')
        _mode = Config.mode
        Config.section = _config.get(default, 'section')
        _section = Config.section
        Config.source_type = _config.get(default, 'type')
        _source_type = Config.source_type
        if _source_type == 'RSS':
            _list_file = 'feed_list_file'
        elif _source_type == 'EGLOOS':
            _list_file = 'egloos_list_file'
        elif _source_type == 'HTML':
            _list_file = 'html_list_file'
        elif _source_type == 'TEXT':
            _list_file = 'text_list_file'
        else:
            print('Unknown source type')
            exit()

        Config.list_file = _list_file
        try:
            Config.file_path = _config.get(_mode, _section + '.' + _list_file)
        except (configparser.NoOptionError, configparser.NoSectionError) as e:
            # 소스리스트파일이 없는 경우
            print(str(e))
            exit()


if __name__ == "__main__":
    Config.load('config.conf')
    print(Config.file_path)
    Config.default2 = 'False'
    print(Config.default2)
