"""
The script reads membership CSV files located in raw-data folder
and transforms the dataset into preferred format in processed-data folder.
By default, the script only processes CSV files modified in the last hour.
Pass in parameter -a to process all CSV files.
"""

import argparse
import glob
import hashlib
import os
import re

import arrow
import pandas as pd


parser = argparse.ArgumentParser(description=("Process membership raw CSV files."))
parser.add_argument(
    "-a",
    "--all",
    dest="all",
    default=False,
    action="store_true",
    help="Process all files.",
)


class MembershipProcessor:
    def __init__(self):
        self.successful = pd.DataFrame()
        self.unsuccessful = pd.DataFrame()

    def process_raw_files(self, all: bool) -> None:
        """
        Process raw CSV files modified in the last hour
        or all raw CSV files if all parameter is specified
        """
        one_hour_ago = arrow.now().shift(hours=-1)
        file_names = glob.glob("raw-data/*.csv")
        for file_name in file_names:
            modified = arrow.get(os.stat(file_name).st_mtime)
            if all or modified > one_hour_ago:
                self.process_raw_file(file_name)
        self.store_processed_applications()

    def process_raw_file(self, file_name: str) -> None:
        """
        Process one raw CSV file
        Update self.successful and self.unsuccessful dataframes
        """
        df = pd.read_csv(file_name)

        # Remove salutations
        df.name = df.name.replace(
            [
                "Mr. ",
                "Mrs. ",
                "Ms. ",
                "Miss ",
                "Dr. ",
                " MD",
                " DDS",
                " PhD",
                " DVM",
                " I",
                " II",
                " III",
                " Jr.",
            ],
            "",
            regex=True,
        )
        df.name = df.name.str.strip()

        # Remove middle space in mobile_no
        df.mobile_no = df.mobile_no.replace(" ", "", regex=True)

        # Split name into first and last name
        df[["first_name", "last_name"]] = df.name.str.split(" ", n=1, expand=True)
        df.drop(["name"], axis=1, inplace=True)

        # Format birthday field into YYYYMMDD
        df.date_of_birth = df.date_of_birth.apply(self.format_date)

        # Add above_18 field
        df["above_18"] = df.apply(lambda x: self.is_above_18(x.date_of_birth), axis=1)

        # Validate last_name
        invalid_last_name = df[df.last_name.isnull()]
        self.unsuccessful = pd.concat([self.unsuccessful, invalid_last_name])
        df.drop(index=invalid_last_name.index, inplace=True)

        # Validate mobile_no
        invalid_mobile_no = df[~df.mobile_no.str.match("\d{8}")]
        self.unsuccessful = pd.concat([self.unsuccessful, invalid_mobile_no])
        df.drop(index=invalid_mobile_no.index, inplace=True)

        # Validate above_18
        invalid_above_18 = df[df.above_18 == "N"]
        self.unsuccessful = pd.concat([self.unsuccessful, invalid_above_18])
        df.drop(index=invalid_above_18.index, inplace=True)

        # Validate email
        invalid_email = df[~df.email.str.match("\S+@\S+(\.net|\.com)")]
        self.unsuccessful = pd.concat([self.unsuccessful, invalid_email])
        df.drop(index=invalid_email.index, inplace=True)

        # Add membership_id for successful applications
        df["membership_id"] = df.apply(
            lambda x: f"{x.last_name}_{hashlib.sha256(x.date_of_birth.encode()).hexdigest()[:5]}",
            axis=1,
        )
        self.successful = pd.concat([self.successful, df])

    def format_date(self, date_string: str) -> str:
        """
        Format date string into YYYYMMDD
        """
        output_format = "YYYYMMDD"
        if re.match("\d{2}/\d{2}/\d{4}", date_string):
            date_split = date_string.split("/")
            return arrow.get(
                month=int(date_split[0]),
                day=int(date_split[1]),
                year=int(date_split[2]),
            ).format(output_format)
        elif re.match("\d{2}-\d{2}-\d{4}", date_string):
            date_split = date_string.split("-")
            return arrow.get(
                day=int(date_split[0]),
                month=int(date_split[1]),
                year=int(date_split[2]),
            ).format(output_format)
        return arrow.get(date_string).format(output_format)

    def is_above_18(self, date_of_birth: str) -> str:
        """
        Check if applicant is above 18 years old as of 1 Jan 2022
        Output: Y or N
        """
        eighteen_years_ago = arrow.get("2022-01-01").shift(years=-18)
        if arrow.get(date_of_birth) <= eighteen_years_ago:
            return "Y"
        return "N"

    def store_processed_applications(self) -> None:
        """
        Store processed applications into processed-data folder
        split by successful and unsuccessful applications
        """
        date_now = arrow.now()
        self.successful.to_csv(
            f"processed-data/successful/successful_applications_{date_now}.csv",
            index=False,
        )
        self.unsuccessful.to_csv(
            f"processed-data/unsuccessful/unsuccessful_applications_{date_now}.csv",
            index=False,
        )


if __name__ == "__main__":
    args = parser.parse_args()
    MembershipProcessor().process_raw_files(args.all)
