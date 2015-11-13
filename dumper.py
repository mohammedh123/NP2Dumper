import requests
import json
import time
import sys
import os

# Returns log in responses' cookies
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


if len(sys.argv) < 5:
    print "Usage: python dumper.py username password refresh_seconds game_number"
    sys.exit(1)

username = sys.argv[1]
password = sys.argv[2]
refresh_seconds = sys.argv[3]
game_number = sys.argv[4]

cookies = log_in(username, password)

while True:
    state = get_game_state(cookies, game_number)
    dump_file(state)

    print "Waiting {0} seconds until next bowel movement...".format(refresh_seconds)
    time.sleep(float(refresh_seconds))
