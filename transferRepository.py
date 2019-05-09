#!/usr/bin/python -B

import sys

sys.path.append("/home/warwalrux/scripts/github_api_scripts/github_api_scripts/actions")

import argparse
import requests
import json

from getGroup import slugInOrg as gio
from getRepo import repoInOrg as rio
from renameRepo import renameRepo as rr
from transferRepo import transferRepo as tr
from updatePerms import updatePerms as perms

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

def main():
    args = getOpts()
    if not args.tokenfile:
        print "No github token specified"
        sys.exit(1)
    else:
        token_file = open(args.tokenfile,"r")
        my_token = token_file.readlines()[0].rstrip()
        head={ 'Authorization': 'token ' + my_token }
    if not args.victim:
        print "No victim repo specified"
        sys.exit(1)
    if not args.origin:
        print "No repo origin specified"
        sys.exit(1)
    # Only continue if the $org/$repo combination is valid
    has_repo = rio(args.origin, args.victim, head)
    if has_repo.get('message'):
        print "Requested repo: " + args.victim + " does not exist in the specified origin"
        sys.exit(2)

    if not args.dest:
        print "No victim destination specified"
        sys.exit(1)

    if not args.slug:
        print "No group specified for permissions"
        sys.exit(1)
    if not args.newname:
        newname=args.victim
    
    has_group = gio(args.dest, args.slug, head)
    if not has_group.get('id'):
        print "No group named: " + args.slug + " exists in the specified destination org"
        sys.exit(2)

    tr(args.victim, args.dest, args.origin, has_group.get('id'), head)
    rr(args.victim, newname, args.origin, head)
    perms(has_repo, has_group, "write", args.dest, head)

if __name__ == "__main__":
        main()

