from miquido_gitlab_releaser import create_release
import fileinput


class StdInReader:
    @staticmethod
    def read():
        desc = ''
        for line in fileinput.input():
            desc += line
        return desc


if __name__ == '__main__':
    print(create_release(StdInReader()))
