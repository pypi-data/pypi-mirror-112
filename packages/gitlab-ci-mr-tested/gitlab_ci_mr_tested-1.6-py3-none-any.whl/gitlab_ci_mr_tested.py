import os
import re
import sys
import click
import gitlab
import urllib.parse


default_branch = os.environ.get(
    'CI_MERGE_REQUEST_SOURCE_BRANCH_NAME',
    os.environ.get('CI_COMMIT_BRANCH',
    os.environ.get('CI_COMMIT_REF_NAME',
    "")
    )
)


@click.command()
@click.option('--server', default=os.environ.get("CI_PROJECT_URL"), type=str, help='Gitlab server url')
@click.option('--token', default=os.environ.get("PRIVATE_TOKEN"), type=str, help='Gitlab auth token')
@click.option('--label', default="tested", type=str, help='Gitlab label name to check for')
@click.option('--project-id', default=os.environ.get("CI_PROJECT_ID"), type=str, help='Gitlab project id')
@click.option('--branch', default=default_branch, type=str, help='Branch name of build to find matching MR')
@click.option('--commit-hash', default=os.environ.get("CI_COMMIT_SHA"), type=str, help='Git commit reference')
@click.option('--add-untested', default=None, help='If specified, this label will be added if not tested, removed when tested')
def mr_tested(server, token, label, project_id, branch, commit_hash, add_untested):

    sparts = urllib.parse.urlparse(server)
    server = "%s://%s" % (sparts.scheme, sparts.netloc)
    gl = gitlab.Gitlab(server, private_token=token)
    gl.auth()

    project = gl.projects.get(project_id, lazy=True)

    try:
        br = project.branches.get(branch)
        mrs = br.merge_requests()
    except gitlab.exceptions.GitlabGetError:
        commit = project.commits.get(commit_hash)
        mrs = commit.merge_requests()

    is_tested = len(mrs) > 0

    print("""
  --------------
  Merge Requests
  --------------""")
    for mr in mrs:
        str_tested = ""
        found_instructions = False
        pmr = project.mergerequests.get(mr['iid'], lazy=False)
        if label in pmr.labels:
            print(f'  * !{mr["iid"]}: {mr["title"]} already marked "{label}"')
            continue

        for note in pmr.notes.list(all=True):
            if note.body == f"~{label}":
                str_tested = f": UNDOCUMENTED\n  > please describe what was tested in the comment marked ~{label}\n"
                found_instructions = True
            elif re.match(f"(^|\W)~{label}\W.+", note.body, flags=re.DOTALL):
                found_instructions = True
                str_tested = ": TESTED"
                if add_untested and add_untested in pmr.labels:
                    pmr.labels = [l for l in pmr.labels if l != add_untested]
                    str_tested = f", removing {add_untested} label"

                if label not in pmr.labels:
                    pmr.labels.append(label)
                    str_tested = f", adding {label} label"
                pmr.save()

        if not found_instructions:
            is_tested = False
            str_tested = ": UNTESTED\n  > please test feature and add method starting with the text '~tested' as comment to MR\n"
            if add_untested:
                if not is_tested and add_untested not in pmr.labels:
                    pmr.labels.append(add_untested)
                    pmr.save()

        print(f"  * !{mr['iid']}: {mr['title']}{str_tested}")

    sys.exit(0 if is_tested else 1)


if __name__ == '__main__':
    mr_tested()
