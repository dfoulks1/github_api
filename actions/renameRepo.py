#!/usr/bin/python -B
import argparse
import requests
import json
import sys

url="https://api.github.com"
def getOpts () :
    parser = argparse.ArgumentParser(description='github api caller')
    parser.add_argument('-v', '--victim', help='victim repository')
    parser.add_argument('-o', '--org', help="original repo owner")
    parser.add_argument('-n', '--newname', help='target repo name')
    parser.add_argument('-t', '--tokenfile', help='token file')
    args = parser.parse_args()
    return args

def renameRepo (victim, newname, org, head):
    """ Rename the repository
        requires reponame, newname, org, headers (with token embedded)"""
    rename_data={ "name": newname }
    uri=url + "/repos/" + org + "/" + victim
    requests.patch(uri, headers=head, data=json.dumps(rename_data)).json()

def main () :
    args = getOpts()

    # Check token stuffs
    if not args.tokenfile: 
        print "No token provided"
        # INVOCATION ERROR
        sys.exit(1)
    token_file = open(args.tokenfile,"r")
    my_token = token_file.readlines()[0].rstrip()
    head={ 'Authorization': 'token ' + my_token }

    # Repository exists in intermediate org (Access granted to this org as we see fit)
    if not args.victim:
        print "No victims today"
        # INVOCATION ERROR
        sys.exit(1)

    if not args.org:
        print "No org provided"
        sys.exit(1)

    if not args.newname:
        print "No new name provided"
        sys.exit(1)

    renameRepo(args.victim, args.newname, args.org, head)

if __name__ == "__main__":
    main()
