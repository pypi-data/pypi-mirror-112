from data import columns
from custom_git import for_each_ref, log

def commit_author_time_and_branch_ref(run, master_branch):
    get_refs = for_each_ref('refs/remotes/origin/**', format='%(refname:short) %(authordate:unix)')
    with run(get_refs) as program:
        for branch, t in columns(program.stdout):
            get_time = log(f"{master_branch}..{branch}", format='%at')
            with run(get_time) as inner_program:
                for author_time, in columns(inner_program.stdout):
                    yield int(author_time), branch


def get_branches(run):
    with run(for_each_ref(format='%(refname)')) as cmd:
        for line in cmd.stdout:
            yield line.strip()
