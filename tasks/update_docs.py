import logging

from services import info_service, publish_service

logging.basicConfig(level=logging.DEBUG)


def main():
    info_service.make_readme_md_file()
    publish_service.update_docs()


if __name__ == '__main__':
    main()
