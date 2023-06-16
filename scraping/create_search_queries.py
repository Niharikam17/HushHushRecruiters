from database.util import add_job_profile


def execute():
    cities_file = open('Text_Files/cities.txt', 'r')
    cities = cities_file.readlines()

    job_profile_files = open('Text_Files/job_profiles.txt', 'r')
    job_profiles = job_profile_files.readlines()

    index = 97
    for c in cities:
        for jp in job_profiles:
            url = f'site:stackoverflow.com/users/ AND "{jp.strip()}" AND "{c.strip()}"'

            add_job_profile(index, c, jp, url, False)

            index += 1


if __name__ == '__main__':
    execute()
