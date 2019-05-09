#!/usr/bin/python -B
import argparse
import requests
import json
import sys
from getGroup import slugInOrg as gio
url="https://api.github.com"
def getOpts () :
	parser = argparse.ArgumentParser(description='github api caller')
        parser.add_argument('-d', '--dest', help="New repository owner")
        parser.add_argument('-v', '--victim', help="New repository owner")
        parser.add_argument('-o', '--origin', help="original repo owner")
        parser.add_argument('-n', '--newname', help="name of repository under new owner")
	parser.add_argument('-t', '--tokenfile', help='token file')
        parser.add_argument('-s', '--slug', help='team with access to new repo')
	args = parser.parse_args()
	return args

def transferRepo (victim, dest, origin, gh_id, head):
    """ Transfer the repository <victim> from <origin> to <dest> with ID as the team with perms for the repo.
        requires: victim repository, destination org, origin org, groupID in destination, and headers with token embedded"""
        
    head['Accept']='application/vnd.github.nightshade-preview+json'
    transfer_data = {
        'new_owner': dest,
        'team_ids': [
            gh_id
        ]
    }
    r = requests.post(url + "/repos/" + origin +"/" + victim + "/transfer", headers=head, data=json.dumps(transfer_data)).json()

def main () :
    args = getOpts()

    # Check token
    if not args.tokenfile: 
        print "No token provided"
        sys.exit(1)
    token_file = open(args.tokenfile,"r")
    my_token = token_file.readlines()[0].rstrip()
    head={ 'Authorization': 'token ' + my_token }

    # Sanity checking other (but not lesser) args
    if not args.victim:
        print "no repo victim provided"
        sys.exit(1)

    if not args.origin:
        print "no repo origin provided"
        sys.exit(1)

    if not args.dest:
        print "no repo destination provided"
        sys.exit(1)
    gh_id = gio(args.dest, args.slug, head)

    print gh_id

    transferRepo(args.victim, args.dest, args.origin, gh_id.get('id'), head)
    
if __name__ == "__main__":
    main()
