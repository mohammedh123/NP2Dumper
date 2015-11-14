import ConfigParser
import getpass
import os

def main():
    dgn = "5274373517737984" # default game number
    dri = 60 # default refresh interval
    
    print "NP2 Dumper Config Setup"
    username = raw_input("Enter username: ")
    password = getpass.getpass("Enter password: ")
    game_number = raw_input("Enter game number [{0}]: ".format(dgn)) or dgn
    refresh_interval = raw_input("Enter refresh interval in seconds [{0}]: ".format(dri)) or dri

    config = ConfigParser.ConfigParser()
    config.add_section('config')
    config.set('config', 'username', username)
    config.set('config', 'password', password)
    config.set('config', 'game_number', game_number)
    config.set('config', 'refresh_interval', refresh_interval)
  
    ofilename = 'np2d-config.ini' 
    print "Writing config to {0}...".format(ofilename) 
    with open(ofilename, 'w') as config_file:
        config.write(config_file)
    
    print "Now you can run the dumper using the following command:"
    print "python dumper.py"


if __name__ == '__main__':
    main()

