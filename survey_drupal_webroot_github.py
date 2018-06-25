import inspect
import pprint
import sys

import github


def main():
    '''
    Usage: survey_drupal_webroot_github access_token
    Survey github for conventions involving drupal webroot
    '''

    access_token = None
    if len(sys.argv) == 2:
        access_token = sys.argv[1]
    elif len(sys.argv) == 1:
        access_token = load_access_token()
    if access_token is None:
        print(inspect.cleandoc(main.__doc__), file=sys.stderr)
        sys.exit(1)
    run(github.Github(
        access_token,
        per_page=100,
    ))
    sys.exit(0)


def load_access_token(filename='my_access_token.txt'):
    try:
        access_token = open(filename, 'r').readlines()[0].strip()
        return access_token
    except FileNotFoundError:
        return None


def run(apiobj):
    '''
    Perform the survey

    apiobj: github.Github object
    '''

    counts = {}
    esp = 'default.settings.php'
    sd = 'sites/default'
    suffix = f'/{sd}/{esp}'
    query = f'filename:{esp}'
    try:
        for result in apiobj.search_code(
            query,
            sort='indexed',
        ):
            if not result.path.endswith(suffix):
                next
            prefix = result.path[:-len(suffix)]
            if prefix not in counts:
                counts[prefix] = 0
            counts[prefix] += 1
    finally:
        pprint.pprint(counts)


if __name__ == '__main__':
    main()
