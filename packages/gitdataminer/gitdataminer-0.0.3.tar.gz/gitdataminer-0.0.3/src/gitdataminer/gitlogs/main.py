import os
import pandas as pd

COMMIT_LOG = os.path.join(os.path.abspath(""), "logs/react-git.log")


def parser(commit_log):
    try:
        commits = pd.read_csv(commit_log, sep="\u0012", header=None, names=["raw"])
    except FileNotFoundError:
        raise FileNotFoundError("No such file")
    commit_marker = commits[commits["raw"].str.startswith("--", na=False)]
    commit_info = commit_marker["raw"].str.extract(
        r"^--(?P<SHA>.*?)--(?P<Timestamp>.*?)--(?P<Author>.*?)$", expand=True
    )
    # Every row that is not a commit info row is a file statistics row.
    # reuse the index of our already prepared commit_info DataFrame to get all
    # the other data by saying “give me all commits that are not in the index
    # of the commit_info‘s DataFrame“.
    file_stats_marker = commits[~commits.index.isin(commit_info.index)]
    file_stats = file_stats_marker["raw"].str.split("\t", expand=True)
    file_stats = file_stats.rename(
        columns={0: "Insertion", 1: "Deletion", 2: "File path"}
    )
    file_stats["Insertion"] = pd.to_numeric(
        file_stats["Insertion"], errors="coerce"
    )  #  invalid parsing will be set as NaN.
    file_stats["Deletion"] = pd.to_numeric(file_stats["Deletion"], errors="coerce")

    commit_data = commit_info.reindex(commits.index).fillna(
        method="ffill"
    )  # ffill Propagate last valid observation forward to next valid.
    commit_data = commit_data[~commit_data.index.isin(commit_info.index)]
    commit_data = commit_data.join(file_stats)
    return commit_data


class CommitAnalyzer(object):
    def __init__(self, commit_log) -> None:
        self.commit_df = parser(commit_log)

    def timed_commits(self):
        timed_commits = (
            self.commit_df.set_index(pd.DatetimeIndex(self.commit_df["Date"]))[
                ["Insertion", "Deletion"]
            ]
            .resample("1D")
            .sum()
        )
        return timed_commits

    def total_commit_counts(self):
        return self.commit_df["SHA"].nunique()

    # list of all developers
    def list_all_authors(self):
        return pd.unique(self.commit_df["Author"])

    # total number of developers
    def total_authors(self):
        len(pd.unique(self.commit_df["Author"]))

    # listing top authors
    def top_authors(self, topby=10):
        topauthors = (
            self.commit_df.groupby(by=["Author"])["SHA"].nunique().nlargest(topby)
        )
        return topauthors

    # total commits by particular author
    def total_commits_by_author(self, author):
        """
        this works with git shortlog -s -n --all --no-merges
        """
        commits = (
            self.commit_df[self.commit_df["Author"] == author]
            .groupby(by=["Author"])["SHA"]
            .nunique()
        )
        return commits

    # coding days of particular author
    def coding_days_per_author(self, author):
        coding_days = self.commit_df[
            (self.commit_df["Author"] == author)
            & (self.commit_df["Date"] > "2021-05-20")
            & (self.commit_df["Date"] < "2021-06-25")
        ]
        grouped_coding_days = coding_days.groupby(by=["Date", "SHA"])[
            ["Insertion", "Deletion", "Churn"]
        ].sum()
        grouped_coding_days["Commit count"] = coding_days.groupby(
            ["Date", "SHA"]
        ).size()
        grouped_coding_days.reset_index()
        return grouped_coding_days

    # sort author by total insertion
    def author_list_by_total_insertion(self):
        sorted_author_by_total_insertion = (
            self.commit_df.groupby("Author")
            .sum()[["Insertion"]]
            .sort_values(by="Insertion", ascending=False)
        )
        return sorted_author_by_total_insertion

    def author_list_by_total_deletion(self):
        sorted_author_by_total_deletion = (
            self.commit_df.groupby("Author")
            .sum()[["Deletion"]]
            .sort_values(by="Deletion", ascending=False)
        )
        return sorted_author_by_total_deletion

    def commits_per_hour(self):
        commits_per_hour = self.commit_df.Date.dt.hour.value_counts(sort=False)
        print(commits_per_hour.head())
        return commits_per_hour

    def commits_per_weekday(self):
        commits_per_weekday = self.commit_df.Date.dt.weekday.value_counts(sort=False)
        return commits_per_weekday

    def commit_history(self):
        # number of commits over the last years
        git_timed = self.commit_df.set_index("Date").Author
        return git_timed

    def commits_history_per_hour(self):
        """
        group values according to certain time units such as days (D) using
        resample(<"time_unit">). To combined individual values based on time
        unit we use count to count the number of commits
        """
        commits_per_day = self.commit_history().resample("H").count()
        return commits_per_day

    def commits_per_day(self):
        """
        group values according to certain time units such as days (D) using
        resample(<"time_unit">). To combined individual values based on time
        unit we use count to count the number of commits
        """
        commits_per_day = self.commit_history().resample("D").count()
        return commits_per_day

    def commits_per_month(self):
        """
        group values according to certain time units such as days (D) using
        resample(<"time_unit">). To combined individual values based on time
        unit we use count to count the number of commits
        """
        commits_per_day = self.commit_history().resample("M").count()
        return commits_per_day

    def commit_history_over_the_years(self):
        commits_per_day_cumulative = self.commits_per_day.cumsum()
        return commits_per_day_cumulative

    def commit_range(self, before="2021-06-25", after="2021-05-25"):
        filter = self.commit_df[
            (self.commit_df["Date"] > after) & (self.commit_df["Date"] < before)
        ]
        return filter

    def insertion_count_per_author(self, author):
        insertion_count = self.commit_df[self.commit_df["Author"].str.match(author)][
            "Insertion"
        ].sum()
        return insertion_count

    def deletion_count_per_author(self, author):
        deletion_count = self.commit_df[self.commit_df["Author"].str.match(author)][
            "Deletion"
        ].sum()
        return deletion_count

    def mean_of_insertion_of_all_authors(self):
        self.commit_df.groupby(by=["Author"]).mean()["Insertion"]

    def mean_of_deletion_of_all_authors(self):
        self.commit_df.groupby(by=["Author"]).mean()["Deletion"]

    def initial_commit(self):
        initial_commit_date = self.commit_df[-1:]
        return initial_commit_date

    # total coding hours
    def total_coding_hours_of_all_author(self):
        """
        get the hours estimate for this repository (using 30 mins per commit)
        of time indicated by limit/extensions/days/etc.
        For each author in the commit history, do the following:
            1. Go through all commits and compare the difference between them in time.
            2. If the difference is smaller or equal then a given threshold, group the
            commits to a same coding session.(Time between commits < 1h yes then group
            those commits as same coding session)
            3. If the difference is bigger than a given threshold, the coding session
            is finished.
            4. To compensate the first commit whose work is unknown, we add extra hours
            to the coding session.
            5. Continue until we have determined all coding sessions and sum the hours
            made by individual authors

        """
        # the threhold for how close two commits need to be to consider them
        # part of one coding session
        grouping_window = 0.5
        single_commit_hours = 0.5  # the time range to associate with one single commit
        # Maximum time diff between 2 subsequent commits in minutes which are
        # counted to be in the same coding "session"
        max_commit_diff_in_minutes = grouping_window * 60.0
        first_commit_addition_in_minutes = single_commit_hours * 60.0
        people = set(self.commit_df["Author"].values)
        ds = []
        commit_df_copy = self.commit_df.loc[:]
        commit_df_copy.set_index(keys=["Date"], drop=True, inplace=True)
        for person in people:
            commits = commit_df_copy[commit_df_copy["Author"] == person]
            commits_ts = [x * 10e-10 for x in sorted(commits.index.values.tolist())]
            if len(commits_ts) < 2:
                ds.append([person, 0])
                continue

            def estimate(index, date):
                next_ts = commits_ts[index + 1]
                diff_in_minutes = next_ts - date
                diff_in_minutes /= 60.0
                # steps 2 - Check if commits are counted to be in same coding session.
                if diff_in_minutes < max_commit_diff_in_minutes:
                    return diff_in_minutes / 60.0
                # The work of first commit of a session cannot be seen in git history,
                # so we make a blunt estimate of it
                return first_commit_addition_in_minutes / 60.0

            hours = [estimate(a, b) for a, b in enumerate(commits_ts[:-1])]
            hours = sum(hours)
            ds.append([person, hours])
        df = pd.DataFrame(ds, columns=["Author", "hours"])
        df.sort_values(by="hours", ascending=False)

    # age of commit
    def commit_age(self):
        commit_df_copy = self.commit_df.loc[:]  # self.commit_df.copy()
        commit_df_copy["Today"] = pd.to_datetime("today", utc=True)
        commit_df_copy["Age"] = commit_df_copy["Date"] - commit_df_copy["Today"]
        return commit_df_copy

    # highest insertion, lowest insertion, average insertion
    def insertion_overall_stats(self):
        insertion_stats = self.commit_df["Insertion"].describe()
        return insertion_stats

    # highest deletion, lowest deletion, average deletion
    def deletion_overall_stats(self):
        deletion_stats = self.commit_df["Deletion"].describe()
        return deletion_stats

    # commits of more than 100 lins of code written
    def commits_greater_than_100_loc(self):
        commits_greater_than_100_code_insertion = self.commit_df[
            self.commit_df["Insertion"] > 100.0
        ]
        return commits_greater_than_100_code_insertion

    # lines of code metrics
    def lines_of_code_changes(self):
        insertion_count = self.commit_df[
            self.commit_df["Author"].str.match("Dan Abramov")
        ]["Insertion"].sum()
        deletion_count = self.commit_df[
            self.commit_df["Author"].str.match("Dan Abramov")
        ]["Deletion"].sum()
        files_changed = self.commit_df[
            self.commit_df["Author"].str.match("Dan Abramov")
        ]["File path"].count()
        total_lines = insertion_count - deletion_count
        add_del_ratio = deletion_count / insertion_count  # 1: n
        return (
            files_changed,
            insertion_count,
            deletion_count,
            total_lines,
            add_del_ratio,
        )

    def efficiency_per_author(self, author):
        # TODO :: Need to check churn reliability.
        total_insertions = self.commit_df[self.commit_df["Author"] == author][
            "Insertion"
        ]
        total_deletions = self.commit_df[self.commit_df["Author"] == author]["Deletion"]
        total_work = total_insertions + total_deletions
        churn_work = self.commit_df[self.commit_df["Author"] == author]["Churn"]
        productive_work = total_work - churn_work
        efficiency = (productive_work / total_work) * 100
        return efficiency

    def productive_throughput_per_author(self, author):
        total_insertions = self.commit_df[self.commit_df["Author"] == author][
            "Insertion"
        ]
        total_deletions = self.commit_df[self.commit_df["Author"] == author]["Deletion"]
        total_work = total_insertions + total_deletions
        churn_work = self.commit_df[self.commit_df["Author"] == author]["Churn"]
        productive_throughput = total_work - churn_work
        return productive_throughput

    def most_productive_day_per_week_per_author(self, author):
        most_productive_day_per_week = self.commit_df[
            self.commit_df["Author"] == author
        ].Date.dt.weekday.max()
        return most_productive_day_per_week

    def least_productive_day_per_week_per_author(self, author):
        least_productive_day_per_week = self.commit_df[
            self.commit_df["Author"] == author
        ].Date.dt.weeekday.min()
        return least_productive_day_per_week

    def most_productive_day_per_project(self):
        most_productive_day_per_project = (
            self.commits_df.Date.dt.weekday.value_counts().max()
        )
        return most_productive_day_per_project

    def least_productive_day_per_project(self):
        most_productive_day_per_project = (
            self.commits_df.Date.dt.weekday.value_counts().min()
        )
        return most_productive_day_per_project

    def files_per_commit(self):
        files_history_per_commit = self.commit_df.groupby(by=["Author", "SHA"])[
            "File path"
        ]
        return files_history_per_commit.count()

    def maximum_files_commited_together(self):
        return self.files_per_commit().max()

    def minimum_files_commited_together(self):
        return self.files_per_commit().min()

    def average_files_commited_together(self):
        return self.files_per_commit().mean()

    def files_per_commit_per_author(self, author):
        files_history_per_commit_per_author = self.commit_df[
            self.commit_df["Author"] == author
        ].groupby(by=["Author", "SHA"])["File path"]
        return files_history_per_commit_per_author.count()

    def maximum_files_commited_together_per_author(self):
        return self.files_per_commit_per_author().max()

    def minimum_files_commited_together_per_author(self):
        return self.files_per_commit_per_author().min()

    def average_files_commited_together_per_author(self):
        return self.files_per_commit_per_author().mean()


if __name__ == "__main__":
    analyzer = CommitAnalyzer(COMMIT_LOG)
