import getopt
import json
import os
import requests
import sys
import time


# Returns login response's cookies
def log_in(username, password):
    print "Preparing to take a dump by logging in..."

    login_data = { "type": "login", "alias": username, "password": password }
    login_resp = requests.post("http://np.ironhelmet.com/arequest/login", data=login_data)

    if login_resp.status_code != 200 or not login_resp.cookies:
        print "Failed to log in correctly. Check your credentials."
        sys.exit(1)

    print "Logged in!"
    return login_resp.cookies


# Returns the current game state as json
def get_game_state(cookies, game_number):
    print "Getting game state to dump..."

    get_state_data = { "type": "order", "order": "full_universe_report", "version": "7", "game_number": game_number }
    get_state_resp = requests.post("http://np.ironhelmet.com/grequest/order", data=get_state_data, cookies=cookies)

    if get_state_resp.status_code != 200:
        print "Failed to get game state. Bother Mohammed, but not until the game is over."
        sys.exit(1)

    print "Game state received!"
    return get_state_resp.text


def dump_file(state_json_str):
    state_json = json.loads(state_json_str)
    tick = state_json['report']['tick']
    player = state_json['report']['player_uid']

    filename = "gamestate_{0:02d}_{0:08d}.json".format(player, tick)
    print "Taking a dump on {}/{}...".format('dumps', filename)

    if not os.path.exists('dumps'):
        os.makedirs('dumps')

    with open('dumps/' + filename, 'w') as dump_file:
        dump_file.write(state_json_str)

    print "Finished taking dump."


def print_usage():
    print "Usage: python {0} -u username -p password -g game_number [-t refresh_interval]".format(sys.argv[0])
    print "Note:  refresh interval is measured in seconds and defaults to 60"


def parse_args(args):
    dic = {}
    
    if (len(args) == 0):
        return dic
    
    opts = getopt.getopt(args, 'hu:p:g:t:')
    
    for o,a in opts[0]:
        if o == '-h':
            dic['help'] = True
            break
        elif o == '-u':
            dic['username'] = a
        elif o == '-p':
            dic['password'] = a
        elif o == '-g':
            dic['game_number'] = a
        elif o == '-t':
            dic['refresh_interval'] = a
    
    return dic


def validate_args(dic):
    if 'help' in dic:
        print_usage()
        sys.exit(0)
    
    if 'username' not in dic or dic['username']=='':
        print "Error: username was not specified; exiting..."
        print_usage()
        sys.exit(1)
    
    if 'password' not in dic or dic['password']=='':
        print "Error: password was not specified; exiting..."
        print_usage()
        sys.exit(1)
    
    if 'game_number' not in dic or dic['game_number']=='':
        print "Error: game number was not specified; exiting..."
        print_usage()
        sys.exit(1)
    
    if 'refresh_interval' not in dic or dic['refresh_interval']=='':
        dri = 60 # default refresh interval
        dic['refresh_interval'] = dri
        print "Info:  refresh interval was not specified; defaulting to {0} seconds...".format(dri)


def main():
    args = [] if len(sys.argv)==1 else sys.argv[1:]
    dic = parse_args(args)
    validate_args(dic)

    cookies = log_in(dic['username'], dic['password'])
    refresh_interval = dic['refresh_interval']

    while True:
        state = get_game_state(cookies, dic['game_number'])
        dump_file(state)

        print "Waiting {0} seconds until next bowel movement...".format(refresh_interval)
        time.sleep(float(refresh_interval))


if __name__ == '__main__':
    main()
