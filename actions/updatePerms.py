#!/usr/bin/python -B
import argparse
import requests
import json
import sys
from getRepo import repoInOrg as rio
from getGroup import slugInOrg as sio

url="https://api.github.com"
def getOpts () :
    parser = argparse.ArgumentParser(description='github api caller')
    parser.add_argument('-v', '--victim', help="New repository owner")
    parser.add_argument('-o', '--org', help="repo owner")
    parser.add_argument('-t', '--tokenfile', help='token file')
    parser.add_argument('-s', '--slug', help='team with access to new repo')

    # Permissions Levels
    parser.add_argument('-r', '--read',action='store_true', help='readonly')
    parser.add_argument('-w', '--write',action='store_true', help='write perms')
    parser.add_argument('-a', '--admin',action='store_true',help='administrative perms')
    args = parser.parse_args()
    return args

def updatePerms (victim, gh_id, perms, org, head):
    """ Update Permissions to the repositories
        requires: victim repository, group id, permission level as string (pull, push, admin), organization, and headers (with token embedded)"""
    head['Accept']="application/vnd.github.inertia-preview+json"
    #head['Accept']="application/vnd.github.hellcat-preview+json"
    perms_data = { 'permission': perms } 
    new_url = url + "/teams/" + str(gh_id.get('id')) + "/repos/" + org + "/" + victim.get('name')
    try:
        r = requests.put(new_url, headers=head, data=json.dumps(perms_data)).json()
    except ValueError:
        sys.exit(0)
def main () :
    args = getOpts()

    # Check token and cram it in a Header
    if not args.tokenfile: 
        print "No token provided"
        sys.exit(1)
    token_file = open(args.tokenfile,"r")
    my_token = token_file.readlines()[0].rstrip()
    head={ 'Authorization': 'token ' + my_token }

    # Sanity checking other (but not lesser) args
    if not args.slug:
        print "no github groups provided"
        sys.exit(1)
    
    if not args.victim:
        print "no repo victim provided"
        sys.exit(1)

    if not args.org:
        print "no repo org provided"
        sys.exit(1)

    if args.read:
        perm = "pull"
    elif args.write:
        perm = "push"
    elif args.admin:
        perm = "admin"
    else:
        perm = "pull"

    updatePerms(rio(args.org, args.victim, head), sio(args.org, args.slug, head), perm, args.org, head)
    
if __name__ == "__main__":
    main()
