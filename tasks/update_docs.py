import logging

from services import template_service, publish_service

logging.basicConfig(level=logging.DEBUG)


def main():
    template_service.make_readme_md_file()
    publish_service.update_docs()


if __name__ == '__main__':
    main()
