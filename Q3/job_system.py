import sys
from collections import defaultdict

input = sys.stdin.read
data = input().splitlines()

line = 0
s = int(data[line])
line += 1
allowed_skills = set(data[line].split())
line += 1
q = int(data[line])
line += 1

jobs = [None]  # index 0 unused
users = [None]  # index 0 unused
job_counter = 0
user_counter = 0

timetypes = {'FULLTIME', 'PARTTIME', 'PROJECT'}

time_table = {
    'FULLTIME': {'FULLTIME': 10, 'PARTTIME': 5, 'PROJECT': 4},
    'PARTTIME': {'FULLTIME': 5, 'PARTTIME': 10, 'PROJECT': 5},
    'PROJECT': {'FULLTIME': 4, 'PARTTIME': 5, 'PROJECT': 10},
}

def is_valid_name(name):
    if not (1 <= len(name) <= 10):
        return False
    return all(c.isalpha() for c in name)

def is_valid_age(age):
    return 0 <= age <= 200

def is_valid_age_interval(minage, maxage):
    return minage <= maxage

def is_valid_timetype(timetype):
    return timetype in timetypes

def is_valid_salary(salary):
    return 0 <= salary < 1000000000 and salary % 1000 == 0

for _ in range(q):
    query = data[line].split()
    line += 1
    cmd = query[0]

    if cmd == 'ADD-JOB':
        name, minage_str, maxage_str, timetype, salary_str = query[1:]
        minage = int(minage_str)
        maxage = int(maxage_str)
        salary = int(salary_str)

        if not is_valid_name(name):
            print('invalid name')
            continue
        if not (is_valid_age(minage) and is_valid_age(maxage) and is_valid_age_interval(minage, maxage)):
            print('invalid age interval')
            continue
        if not is_valid_timetype(timetype):
            print('invalid timetype')
            continue
        if not is_valid_salary(salary):
            print('invalid salary')
            continue

        job_counter += 1
        jobs.append({
            'name': name,
            'minage': minage,
            'maxage': maxage,
            'timetype': timetype,
            'salary': salary,
            'skills': set(),
            'views': 0,
            'skill_views': defaultdict(int)
        })
        print(f'job id is {job_counter}')

    elif cmd == 'ADD-USER':
        name, age_str, timetype, salary_str = query[1:]
        age = int(age_str)
        salary = int(salary_str)

        if not is_valid_name(name):
            print('invalid name')
            continue
        if not is_valid_age(age):
            print('invalid age')
            continue
        if not is_valid_timetype(timetype):
            print('invalid timetype')
            continue
        if not is_valid_salary(salary):
            print('invalid salary')
            continue

        user_counter += 1
        users.append({
            'name': name,
            'age': age,
            'timetype': timetype,
            'salary': salary,
            'skills': set(),
            'skill_views': defaultdict(int)
        })
        print(f'user id is {user_counter}')

    elif cmd == 'ADD-JOB-SKILL':
        job_id_str, skill = query[1:]
        job_id = int(job_id_str)

        if not (1 <= job_id < len(jobs)):
            print('invalid index')
            continue
        if skill not in allowed_skills:
            print('invalid skill')
            continue
        if skill in jobs[job_id]['skills']:
            print('repeated skill')
            continue

        jobs[job_id]['skills'].add(skill)
        print('skill added')

    elif cmd == 'ADD-USER-SKILL':
        user_id_str, skill = query[1:]
        user_id = int(user_id_str)

        if not (1 <= user_id < len(users)):
            print('invalid index')
            continue
        if skill not in allowed_skills:
            print('invalid skill')
            continue
        if skill in users[user_id]['skills']:
            print('repeated skill')
            continue

        users[user_id]['skills'].add(skill)
        print('skill added')

    elif cmd == 'VIEW':
        user_id_str, job_id_str = query[1:]
        user_id = int(user_id_str)
        job_id = int(job_id_str)

        if not (1 <= user_id < len(users) and 1 <= job_id < len(jobs)):
            print('invalid index')
            continue

        print('tracked')
        job = jobs[job_id]
        user = users[user_id]
        job['views'] += 1
        for sk in job['skills']:
            if sk in user['skills']:
                job['skill_views'][sk] += 1
        for sk in user['skills']:
            if sk in job['skills']:
                user['skill_views'][sk] += 1

    elif cmd == 'JOB-STATUS':
        job_id_str = query[1]
        job_id = int(job_id_str)

        if not (1 <= job_id < len(jobs)):
            print('invalid index')
            continue

        job = jobs[job_id]
        print(job['name'] + '-' + str(job['views']) + '-', end='')
        sorted_sk = sorted(job['skills'], key=lambda sk: (job['skill_views'][sk], sk))
        for sk in sorted_sk:
            print('(' + sk + ',' + str(job['skill_views'][sk]) + ')', end='')
        print()

    elif cmd == 'USER-STATUS':
        user_id_str = query[1]
        user_id = int(user_id_str)

        if not (1 <= user_id < len(users)):
            print('invalid index')
            continue

        user = users[user_id]
        print(user['name'] + '-', end='')
        sorted_sk = sorted(user['skills'], key=lambda sk: (user['skill_views'][sk], sk))
        for sk in sorted_sk:
            print('(' + sk + ',' + str(user['skill_views'][sk]) + ')', end='')
        print()

    elif cmd == 'GET-JOBLIST':
        user_id_str = query[1]
        user_id = int(user_id_str)

        if not (1 <= user_id < len(users)):
            print('invalid index')
            continue

        user = users[user_id]
        scores = []
        for jid in range(1, len(jobs)):
            job = jobs[jid]
            # age score
            x = user['age']
            l = job['minage']
            r = job['maxage']
            if l <= x <= r:
                age_s = min(r - x, x - l)
            elif x < l:
                age_s = x - l
            else:
                age_s = r - x
            inter = len(user['skills'] & job['skills'])
            diff = len(job['skills'] - user['skills'])
            skill_s = 3 * inter - diff
            time_s = time_table[user['timetype']][job['timetype']]
            x_sal = user['salary']
            y_sal = job['salary']
            div = max(abs(x_sal - y_sal), 1)
            sal_s = (1000 // div) * 1000
            base = age_s + skill_s + time_s + sal_s
            total = base * 1000 + jid
            scores.append((total, jid))

        sorted_scores = sorted(scores, reverse=True)[:5]
        for total, jid in sorted_scores:
            print(f'({jid},{total})', end='')
        print()