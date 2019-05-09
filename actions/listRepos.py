#!/usr/bin/python -B
import argparse
import requests
import json
import sys


url="https://api.github.com"

def getOpts () :
	parser = argparse.ArgumentParser(description='github api caller')
        parser.add_argument('-t', '--tokenfile', help="github API token")
        parser.add_argument('-o', '--org', help="repo owner")
	args = parser.parse_args()
	return args

def listRepos (org, head):
    """ Returns github group id when provided a github group slug
        Requires org to search, github group slug, and the headers (with token embedded)"""
    repos = requests.get(url + "/repos/" + org + "/repos?per_page=500", headers=head).json()
    return repos

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

    # Group we've chosen to grant read write access to for the new org.
    if not args.org:
        print "no github org provided"
        # INVOCATION ERROR
        sys.exit(1)

    repos = listRepos(args.org, head)
    print repos
    return repos

if __name__ == "__main__":
    main()
