import argparse
import json
import math
import sys
import time

import fastparquet as fp
import pandas
import s3fs

import GithubApi
from logger_conf import get_module_logger

logger = get_module_logger(__name__)

MAX_GITHUB_SUPPORTED_PAGE_IN_A_TRANSACTION = 100  # limitation from Github


# to flatten the dict
def flatten_dict(dd, separator='_', prefix=''):
    return {prefix + separator + k if prefix else k: v
            for kk, vv in dd.items()
            for k, v in flatten_dict(vv, separator, kk).items()
            } if isinstance(dd, dict) else {prefix: dd}


# function to write to s3 using fastparquet
def write_to_s3(s3_path, df, partition_cols=None, file_scheme='hive'):
    print(df.dtypes)
    if partition_cols:
        fp.write(s3_path, df, file_scheme=file_scheme, partition_on=partition_cols, open_with=s3fs.S3FileSystem().open)
    else:
        fp.write(s3_path, df, file_scheme=file_scheme, open_with=s3fs.S3FileSystem().open)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--configs', type=str, required=True)

    args = parser.parse_args()
    logger.debug("Done with all the config collection")

    config = json.loads(args.configs)
    password = config.get("password")
    repo_name = config.get("repo_name")
    username = config.get("username")
    s3_output_location = config.get("s3_output_location")

    githubapi = GithubApi.GithubApi(username, password)
    logger.debug("Successful: GithubApi object created")
    try:
        star_count = githubapi.repoDetails('{}'.format(repo_name))
        star_count = star_count['stargazers_count']

        logger.info("Total star count of repo %s is %s", repo_name, star_count)

        # finding the number of iteration
        pages = math.ceil(star_count / 100)
        logger.info("Total Iteration we need is  %s", pages)
        stargazer_details = []
    except:
        logger.error("Are you sure the credential and the repo_name is correct? Please check.")
        sys.exit()

    # if the details are correct then proceed or else exit.
    for page in range(pages):
        star_details = githubapi.starGazerDetails(
            '{}/stargazers?per_page={}&page={}'.format(repo_name, MAX_GITHUB_SUPPORTED_PAGE_IN_A_TRANSACTION,
                                                       page + 1))
        for stargazer_detail in star_details:
            stargazer_details.append(flatten_dict(stargazer_detail))
    logger.debug("Creating the DF from the output")
    df = pandas.DataFrame(stargazer_details)
    df['repo_name'] = repo_name

    s3_path = s3_output_location
    write_to_s3(s3_path, df)


if __name__ == '__main__':
    # Creating an object
    start_time = time.time()
    main()
    logger.info("Total time taken for the operation: %s seconds." % (time.time() - start_time))
