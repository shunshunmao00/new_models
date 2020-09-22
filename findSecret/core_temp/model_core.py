# -*-coding:utf-8-*-
#  trufflehog --regex --entropy=False https://github.com/cube-ai/cubeai.git
import tempfile
import hashlib
import asyncio
from git import Repo
from core_temp import util
from core_temp.global_data import g
from git import NULL_TREE


class ModelCore(object):

    def __init__(self):
        pass

    def find_secret(self, git_url, ws_topic):
        print('start find secret')
        # rules = {}
        # read & compile path inclusion/exclusion patterns
        output = self.find_strings(git_url, ws_topic)
        # project_path = output["project_path"]


    def find_strings(self, git_url, ws_topic):

        since_commit = None
        do_entropy = False
        max_depth=1000000
        printJson=False
        do_regex=True
        surpress_output=True
        custom_regexes={}
        branch=None
        repo_path=None
        path_inclusions=None
        path_exclusions=None

        output = {"foundIssues": []}
        project_path = util.clone_git_repo(git_url)
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
            print('-------------------------')
            print(branch_name)
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
                foundIssues = util.diff_worker(diff, curr_commit, prev_commit, branch_name, commitHash, custom_regexes,
                                          do_entropy, do_regex, printJson, surpress_output, ws_topic)
                # output = util.handle_results(output, output_dir, foundIssues)
                prev_commit = curr_commit
            # Handling the first commit
            diff = curr_commit.diff(util.NULL_TREE, create_patch=True)
            foundIssues = util.diff_worker(diff, curr_commit, prev_commit, branch_name, commitHash, custom_regexes,
                                      do_entropy, do_regex, printJson, surpress_output, ws_topic)
        print('finish searching')
        util.clean_up(output_dir)
        #     output = util.handle_results(output, output_dir, foundIssues)
        # output["project_path"] = project_path
        # output["clone_uri"] = git_url
        # output["issues_path"] = output_dir
        # if not repo_path:
        #     shutil.rmtree(project_path, onerror=util.del_rw)
        # return output


    def process_websocket_message(self, websocket, msg):
        if g.event_loop is None:
            g.event_loop = asyncio.get_event_loop()

        if msg.get('type') == 'subscribe_findSecret':
            topic = msg.get('content')
            if isinstance(topic, str):
                if g.ws_connections.get(topic) is not None:
                    g.ws_connections.pop(topic)
                g.ws_connections[topic] = websocket
