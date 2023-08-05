import csv
import sys
from fnmatch import fnmatch
import os
import statistics
import time
from functools import partial
import logging

from src.release_lead_time import commit_author_time_tag_author_time_and_from_to_tag_name, \
    fetch_tags_and_author_dates, fetch_tags_and_sha
from src.process import mk_run
from src.recovery_time import Deployment, find_is_patch, find_outages

def datetime_to_int(dt):
    return time.mktime(time.strptime(f'{dt} 00:00:00', '%d-%m-%Y %H:%M:%S'))

"""DYNAMIC VARIABLES  """
PATH_TO_GIT_REPO = "/home/aishmn/projects/codolytics/four-metrics/projects/react/.git"
START_DATE= datetime_to_int("2-2-2020")
END_DATE=""
DEPLOY_PATTERN= "*"
PATCH_PATTERN="*"
REPO_NAME="react"

# LOG REPORT
def configure_logging():
    logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M',
                    filename='metrics.log',
                    filemode='w')
configure_logging()
log = logging.getLogger("metrics")


def main():
    now = int(time.time())
    lead_time = calculate_lead_time(PATH_TO_GIT_REPO, DEPLOY_PATTERN, START_DATE)
    interval = calculate_deploy_interval(PATH_TO_GIT_REPO, DEPLOY_PATTERN, START_DATE, now)
    change_fail_rate = calculate_change_fail_rate(PATH_TO_GIT_REPO, DEPLOY_PATTERN, PATCH_PATTERN, START_DATE)
    MTTR = calculate_MTTR(PATH_TO_GIT_REPO, DEPLOY_PATTERN, PATCH_PATTERN, START_DATE)
    data = [lead_time, interval, change_fail_rate, MTTR, REPO_NAME]
    print("writing csv file: [R] .........")
    write_four_metrics_csv_file(map(lambda d: str(d), data))
    print("writing csv file: [C] completed")
    print([lead_time, interval, change_fail_rate, MTTR, REPO_NAME])
    return data
    
def calculate_MTTR(PATH_TO_GIT_REPO, DEPLOY_PATTERN, PATCH_PATTERN, START_DATE):
    run = mk_run(PATH_TO_GIT_REPO)
    match_deploy = partial(fnmatch, pat=DEPLOY_PATTERN)
    match_patch = partial(fnmatch, pat=PATCH_PATTERN)
    deploy_tags_author_date = fetch_tags_and_author_dates(
        run,
        match_deploy,
        START_DATE,
    )
    deploy_tags_commit_date = dict(fetch_tags_and_sha(run, match_deploy))
    patch_dates = set(
        date
        for _tag, date
        in fetch_tags_and_sha(run, match_patch)
    )
    deployments = []
    for deploy_tag, deploy_date in deploy_tags_author_date:
        is_patch = find_is_patch(deploy_tag, deploy_tags_commit_date, patch_dates)
        deployments.append(Deployment(is_patch, deploy_date))
    outages = find_outages(deployments)
    log.info("calculating downtime metrics from outages: %s", outages)
    downtime = [end.time - start.time for start, end in outages]
    return statistics.mean(downtime) if downtime else "N/A"


def calculate_change_fail_rate(PATH_TO_GIT_REPO, DEPLOY_PATTERN, PATCH_PATTERN, START_DATE):
    run = mk_run(PATH_TO_GIT_REPO)
    deploy_tags = list(fetch_tags_and_author_dates(
        run,
        partial(fnmatch, pat=DEPLOY_PATTERN),
        START_DATE,
    ))
    patch_tags = list(fetch_tags_and_author_dates(
        run,
        partial(fnmatch, pat=PATCH_PATTERN),
        START_DATE,
    ))
    log.info("calculating change fail rate from patches: %s and deploys: %s", patch_tags, deploy_tags)
    return len(patch_tags) / len(deploy_tags) * 100 if deploy_tags else "N/A"


def calculate_deploy_interval(PATH_TO_GIT_REPO, pattern, START_DATE, now):
    run = mk_run(PATH_TO_GIT_REPO)
    deployments = list(fetch_tags_and_author_dates(
        run,
        partial(fnmatch, pat=pattern),
        START_DATE,
    ))
    log.info("calculating deploy interval from deployments %s", deployments)
    deployment_data = set(tat for tag, tat in deployments)
    interval_seconds = (now - START_DATE) / len(deployment_data) if deployment_data else "N/A"
    return interval_seconds


def calculate_lead_time(PATH_TO_GIT_REPO, pattern, START_DATE):
    run = mk_run(PATH_TO_GIT_REPO)
    deployment_data = list(commit_author_time_tag_author_time_and_from_to_tag_name(
        run,
        partial(fnmatch, pat=pattern),
        START_DATE,
    ))
    deployment_tag_pairs = set(["%s..%s" % (old_tag, tag) for cat, tat, old_tag, tag in deployment_data])
    log.info("calculating lead time data from deployments %s", deployment_tag_pairs)
    lead_time_data = [(tat - cat) for cat, tat, old_tag, tag in deployment_data]
    return statistics.mean(lead_time_data) if lead_time_data else "N/A"
    

def write_four_metrics_csv_file(data):
    writer = csv.writer(open("/home/aishmn/projects/codolytics/four-metrics/react_metrics.csv","w"), delimiter=',', lineterminator='\n')
    writer.writerow(("deploy lead time", "deploy interval", "change fail rate", "mean time to recover", "repo name"))
    writer.writerow(data)


if __name__ == "__main__":
    main()
