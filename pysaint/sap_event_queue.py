"""
    make SAP Event data and return

"""


def get_login_data(j_salt, j_username, j_password):
    data = {
            'login_submit': 'on',
            'login_do_redirect': 1,
            'no_cert_storing': 'on',
            'j_salt': j_salt,
            'j_username': j_username,
            'j_password': j_password,
    }

    return data


def combo_select(key_id, skey, sap_wd_secure_id):
    data = {
        'sap-charset': 'utf-8',
        'sap-wd-secure-id': sap_wd_secure_id,
        '_stateful_': 'X',
        'SAPEVENTQUEUE': 'ComboBox_Select~E002Id' +
                         '~E004{}~E005Key'.format(key_id) +
                         '~E004{skey}~E005ByEnter'.format(skey=skey) +  # ~E004xxx 에서 xxx에 sKey 대입
                         '~E004false~E003' +
                         '~E002ResponseData' +
                         '~E004delta' +
                         '~E005ClientAction' +
                         '~E004submit' +
                         '~E003~E002~E003',
    }

    return data


def button_press(button_id, sap_wd_secure_id):
    data = {
        'sap-charset': 'utf-8',
        'sap-wd-secure-id': sap_wd_secure_id,
        '_stateful_': 'X',
        'SAPEVENTQUEUE': 'Button_Press~E002Id' +
                         '~E004{}'.format(button_id) +
                         '~E003' +
                         '~E002ResponseData' +
                         '~E004delta' +
                         '~E005ClientAction' +
                         '~E004submit' +
                         '~E003' +
                         '~E002' +
                         '~E003'
    }

    return data


def combo_select_with_button_press(key_id, skey, button_id, sap_wd_secure_id):
    data = {
        'sap-charset': 'utf-8',
        'sap-wd-secure-id': sap_wd_secure_id,
        '_stateful_': 'X',
        'SAPEVENTQUEUE': 'ComboBox_Select' +
                         '~E002Id' +
                         '~E004{}'.format(key_id) +
                         '~E005Key' +
                         '~E004{}'.format(skey) +
                         '~E005ByEnter' '+'
                         '~E004false' +
                         '~E003' +
                         '~E002ResponseData' +
                         '~E004delta' +
                         '~E005EnqueueCardinality' +
                         '~E004single' +
                         '~E003' +
                         '~E002' +
                         '~E003' +
                         '~E001Button_Press' +
                         '~E002Id' +
                         '~E004{}'.format(button_id) +
                         '~E003' +
                         '~E002ResponseData' +
                         '~E004delta' +
                         '~E005ClientAction' +
                         '~E004submit' +
                         '~E003' +
                         '~E002' +
                         '~E003'
    }
    return data


def tab_select(section_id, tab_id, item_index, sap_wd_secure_id):
    """
    :param section_id:
    result of get_section_id() method
    :param tab_id:
    result of get_tab_id() method
    :param item_index:
    result of get_tab_item_index() method
    :param sap_wd_secure_id:
    Saint.sap_wd_secure_id
    :return:
    """
    data = {
        'sap-charset': 'utf-8',
        'sap-wd-secure-id': sap_wd_secure_id,
        '_stateful_': 'X',
        "SAPEVENTQUEUE": "TabStrip_TabSelect" +
                         "~E002Id" +
                         "~E004{}".format(section_id) +
                         "~E005ItemId" +
                         "~E004{}".format(tab_id) +
                         "~E005ItemIndex" +
                         "~E004{}".format(item_index) +
                         "~E005FirstVisibleItemIndex" +
                         "~E004{}".format(-1) +
                         "~E003" +
                         "~E002ResponseData" +
                         "~E004delta" +
                         "~E005ClientAction" +
                         "~E004submit" +
                         "~E003" +
                         "~E002" +
                         "~E003"
    }
    return data
