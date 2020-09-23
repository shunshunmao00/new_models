#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
import shutil
import sys
import math
import datetime
import argparse
import uuid
import hashlib
import tempfile
import os
import re
import json
import stat

from git import Repo
from git import NULL_TREE
# from truffleHogRegexes.regexChecks import regexes
from core.model_data.regexChecks import regexes

import asyncio
from core.global_data import g


class ModelCore(object):
    # 声明对外公开可通过API接口访问的方法。如public_methods未声明或值为None则默认本class中定义的所有方法都对外公开。
    public_methods = ('find_secret')

    def __init__(self):
        os.system('apt-get install -y git')


    def find_secret(self, git_url, ws_topic=None):
        # git_url = 'https://gitee.com/mirrors/CubeAI.git'

        since_commit = None
        do_entropy = False
        max_depth = 1000000
        printJson = False
        do_regex = True
        surpress_output = True
        custom_regexes = {}
        branch = None
        repo_path = None
        path_inclusions = None
        path_exclusions = None
        rules = {}
        # read & compile path inclusion/exclusion patterns

        output = find_strings(git_url, since_commit, max_depth, printJson, do_regex, do_entropy,
                surpress_output=False, branch=branch, repo_path=repo_path, path_inclusions=path_inclusions, path_exclusions=path_exclusions, ws_topic=ws_topic)
        project_path = output["project_path"]

        clean_up(output)
        return output


    def process_websocket_message(self, websocket, msg):
        if g.event_loop is None:
            g.event_loop = asyncio.get_event_loop()

        if msg.get('type') == 'subscribe_findSecret':
            topic = msg.get('content')
            if isinstance(topic, str):
                if g.ws_connections.get(topic) is not None:
                    g.ws_connections.pop(topic)
                g.ws_connections[topic] = websocket


def str2bool(v):
    if v == None:
        return True
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


BASE64_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
HEX_CHARS = "1234567890abcdefABCDEF"

def del_rw(action, name, exc):
    os.chmod(name, stat.S_IWRITE)
    os.remove(name)

def shannon_entropy(data, iterator):
    """
    Borrowed from http://blog.dkbza.org/2007/05/scanning-data-for-entropy-anomalies.html
    """
    if not data:
        return 0
    entropy = 0
    for x in iterator:
        p_x = float(data.count(x))/len(data)
        if p_x > 0:
            entropy += - p_x*math.log(p_x, 2)
    return entropy


def get_strings_of_set(word, char_set, threshold=20):
    count = 0
    letters = ""
    strings = []
    for char in word:
        if char in char_set:
            letters += char
            count += 1
        else:
            if count > threshold:
                strings.append(letters)
            letters = ""
            count = 0
    if count > threshold:
        strings.append(letters)
    return strings

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def clone_git_repo(git_url):
    project_path = tempfile.mkdtemp()
    Repo.clone_from(git_url, project_path)
    return project_path

def send_results(issue, ws_topic):
    result = ''
    result += 'commit_time: '+ issue['date'] + '\n'
    result += 'branch_name: ' + issue['branch'] + '\n'
    result += 'prev_commit: ' + issue['commit'] + '\n'
    result += 'printableDiff: ' + issue['printDiff'] + '\n'
    result += 'commitHash: ' + issue['commitHash'] + '\n'
    result += 'reason: ' + issue['reason'] + '\n'
    result += 'path: ' + issue['path']

    print('result', result)
    if ws_topic is not None:
        print('ws_topic', ws_topic)
        asyncio.set_event_loop(g.event_loop)
        websocket = g.ws_connections.get(ws_topic)
        if websocket is not None:
            websocket.write_message({
                'topic': ws_topic,
                'type': 'data',
                'content': result,
            })

def print_results(printJson, issue):
    commit_time = issue['date']
    branch_name = issue['branch']
    prev_commit = issue['commit']
    printableDiff = issue['printDiff']
    commitHash = issue['commitHash']
    reason = issue['reason']
    path = issue['path']

    if printJson:
        print(json.dumps(issue, sort_keys=True))
    else:
        print("~~~~~~~~~~~~~~~~~~~~~")
        reason = "{}Reason: {}{}".format(bcolors.OKGREEN, reason, bcolors.ENDC)
        print(reason)
        dateStr = "{}Date: {}{}".format(bcolors.OKGREEN, commit_time, bcolors.ENDC)
        print(dateStr)
        hashStr = "{}Hash: {}{}".format(bcolors.OKGREEN, commitHash, bcolors.ENDC)
        print(hashStr)
        filePath = "{}Filepath: {}{}".format(bcolors.OKGREEN, path, bcolors.ENDC)
        print(filePath)

        if sys.version_info >= (3, 0):
            branchStr = "{}Branch: {}{}".format(bcolors.OKGREEN, branch_name, bcolors.ENDC)
            print(branchStr)
            commitStr = "{}Commit: {}{}".format(bcolors.OKGREEN, prev_commit, bcolors.ENDC)
            print(commitStr)
            print(printableDiff)
        else:
            branchStr = "{}Branch: {}{}".format(bcolors.OKGREEN, branch_name.encode('utf-8'), bcolors.ENDC)
            print(branchStr)
            commitStr = "{}Commit: {}{}".format(bcolors.OKGREEN, prev_commit.encode('utf-8'), bcolors.ENDC)
            print(commitStr)
            print(printableDiff.encode('utf-8'))
        print("~~~~~~~~~~~~~~~~~~~~~")

def find_entropy(printableDiff, commit_time, branch_name, prev_commit, blob, commitHash):
    stringsFound = []
    lines = printableDiff.split("\n")
    for line in lines:
        for word in line.split():
            base64_strings = get_strings_of_set(word, BASE64_CHARS)
            hex_strings = get_strings_of_set(word, HEX_CHARS)
            for string in base64_strings:
                b64Entropy = shannon_entropy(string, BASE64_CHARS)
                if b64Entropy > 4.5:
                    stringsFound.append(string)
                    printableDiff = printableDiff.replace(string, bcolors.WARNING + string + bcolors.ENDC)
            for string in hex_strings:
                hexEntropy = shannon_entropy(string, HEX_CHARS)
                if hexEntropy > 3:
                    stringsFound.append(string)
                    printableDiff = printableDiff.replace(string, bcolors.WARNING + string + bcolors.ENDC)
    entropicDiff = None
    if len(stringsFound) > 0:
        entropicDiff = {}
        entropicDiff['date'] = commit_time
        entropicDiff['path'] = blob.b_path if blob.b_path else blob.a_path
        entropicDiff['branch'] = branch_name
        entropicDiff['commit'] = prev_commit.message
        entropicDiff['diff'] = blob.diff.decode('utf-8', errors='replace')
        entropicDiff['stringsFound'] = stringsFound
        entropicDiff['printDiff'] = printableDiff
        entropicDiff['commitHash'] = prev_commit.hexsha
        entropicDiff['reason'] = "High Entropy"
    return entropicDiff

def regex_check(printableDiff, commit_time, branch_name, prev_commit, blob, commitHash, custom_regexes={}):
    if custom_regexes:
        secret_regexes = custom_regexes
    else:
        secret_regexes = regexes
    regex_matches = []
    for key in secret_regexes:
        found_strings = secret_regexes[key].findall(printableDiff)
        for found_string in found_strings:
            found_diff = printableDiff.replace(printableDiff, bcolors.WARNING + found_string + bcolors.ENDC)
        if found_strings:
            foundRegex = {}
            foundRegex['date'] = commit_time
            foundRegex['path'] = blob.b_path if blob.b_path else blob.a_path
            foundRegex['branch'] = branch_name
            foundRegex['commit'] = prev_commit.message
            foundRegex['diff'] = blob.diff.decode('utf-8', errors='replace')
            foundRegex['stringsFound'] = found_strings
            foundRegex['printDiff'] = found_diff
            foundRegex['reason'] = key
            foundRegex['commitHash'] = prev_commit.hexsha
            regex_matches.append(foundRegex)
    return regex_matches

def diff_worker(diff, curr_commit, prev_commit, branch_name, commitHash, custom_regexes, do_entropy, do_regex, printJson, surpress_output, path_inclusions, path_exclusions, ws_topic):
    issues = []
    for blob in diff:
        printableDiff = blob.diff.decode('utf-8', errors='replace')
        if printableDiff.startswith("Binary files"):
            continue
        if not path_included(blob, path_inclusions, path_exclusions):
            continue
        commit_time =  datetime.datetime.fromtimestamp(prev_commit.committed_date).strftime('%Y-%m-%d %H:%M:%S')
        foundIssues = []
        if do_entropy:
            entropicDiff = find_entropy(printableDiff, commit_time, branch_name, prev_commit, blob, commitHash)
            if entropicDiff:
                foundIssues.append(entropicDiff)
        if do_regex:
            found_regexes = regex_check(printableDiff, commit_time, branch_name, prev_commit, blob, commitHash, custom_regexes)
            foundIssues += found_regexes
        if not surpress_output:
            for foundIssue in foundIssues:
                send_results(foundIssue, ws_topic)
                # print_results(printJson, foundIssue)
        issues += foundIssues
    return issues

def handle_results(output, output_dir, foundIssues):
    for foundIssue in foundIssues:
        result_path = os.path.join(output_dir, str(uuid.uuid4()))
        with open(result_path, "w+") as result_file:
            result_file.write(json.dumps(foundIssue))
        output["foundIssues"].append(result_path)
    return output

def path_included(blob, include_patterns=None, exclude_patterns=None):
    """Check if the diff blob object should included in analysis.

    If defined and non-empty, `include_patterns` has precedence over `exclude_patterns`, such that a blob that is not
    matched by any of the defined `include_patterns` will be excluded, even when it is not matched by any of the defined
    `exclude_patterns`. If either `include_patterns` or `exclude_patterns` are undefined or empty, they will have no
    effect, respectively. All blobs are included by this function when called with default arguments.

    :param blob: a Git diff blob object
    :param include_patterns: iterable of compiled regular expression objects; when non-empty, at least one pattern must
     match the blob object for it to be included; if empty or None, all blobs are included, unless excluded via
     `exclude_patterns`
    :param exclude_patterns: iterable of compiled regular expression objects; when non-empty, _none_ of the patterns may
     match the blob object for it to be included; if empty or None, no blobs are excluded if not otherwise
     excluded via `include_patterns`
    :return: False if the blob is _not_ matched by `include_patterns` (when provided) or if it is matched by
    `exclude_patterns` (when provided), otherwise returns True
    """
    path = blob.b_path if blob.b_path else blob.a_path
    if include_patterns and not any(p.match(path) for p in include_patterns):
        return False
    if exclude_patterns and any(p.match(path) for p in exclude_patterns):
        return False
    return True


def find_strings(git_url, since_commit=None, max_depth=1000000, printJson=False, do_regex=False, do_entropy=True, surpress_output=True,
                custom_regexes={}, branch=None, repo_path=None, path_inclusions=None, path_exclusions=None, ws_topic=None):
    output = {"foundIssues": []}
    if repo_path:
        project_path = repo_path
    else:
        project_path = clone_git_repo(git_url)
    repo = Repo(project_path)
    already_searched = set()
    output_dir = tempfile.mkdtemp()

    if branch:
        branches = repo.remotes.origin.fetch(branch)
    else:
        branches = repo.remotes.origin.fetch()

    for remote_branch in branches:
        since_commit_reached = False
        branch_name = remote_branch.name
        prev_commit = None
        for curr_commit in repo.iter_commits(branch_name, max_count=max_depth):
            commitHash = curr_commit.hexsha
            if commitHash == since_commit:
                since_commit_reached = True
            if since_commit and since_commit_reached:
                prev_commit = curr_commit
                continue
            # if not prev_commit, then curr_commit is the newest commit. And we have nothing to diff with.
            # But we will diff the first commit with NULL_TREE here to check the oldest code.
            # In this way, no commit will be missed.
            diff_hash = hashlib.md5((str(prev_commit) + str(curr_commit)).encode('utf-8')).digest()
            if not prev_commit:
                prev_commit = curr_commit
                continue
            elif diff_hash in already_searched:
                prev_commit = curr_commit
                continue
            else:
                diff = prev_commit.diff(curr_commit, create_patch=True)
            # avoid searching the same diffs
            already_searched.add(diff_hash)
            foundIssues = diff_worker(diff, curr_commit, prev_commit, branch_name, commitHash, custom_regexes, do_entropy, do_regex, printJson, surpress_output, path_inclusions, path_exclusions, ws_topic)
            output = handle_results(output, output_dir, foundIssues)
            prev_commit = curr_commit
        # Handling the first commit
        diff = curr_commit.diff(NULL_TREE, create_patch=True)
        foundIssues = diff_worker(diff, curr_commit, prev_commit, branch_name, commitHash, custom_regexes, do_entropy, do_regex, printJson, surpress_output, path_inclusions, path_exclusions, ws_topic)
        output = handle_results(output, output_dir, foundIssues)
    output["project_path"] = project_path
    output["clone_uri"] = git_url
    output["issues_path"] = output_dir
    if not repo_path:
        shutil.rmtree(project_path, onerror=del_rw)
    return output

def clean_up(output):
    print("Whhaat")
    issues_path = output.get("issues_path", None)
    if issues_path and os.path.isdir(issues_path):
        shutil.rmtree(output["issues_path"])

if __name__ == "__main__":
    model_core = ModelCore()
    model_core.find_secret('https://gitee.com/mirrors/CubeAI.git', 'xxx')
