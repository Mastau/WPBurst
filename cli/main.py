from core.enumeration import WPEnumerator
import argparse

def main():
    parser = argparse.ArgumentParser(prog="WPBurst", usage='%(prog)s [options]')
    parser.add_argument("url", help="Wordpress URL : http://example.org")
    parser.print_help()
    args = parser.parse_args()

    wp = WPEnumerator(args.url)

    print("[*] Start enumerate")
    wp.detect_wordpress()
    wp.get_version()
    wp.enumerate_plugins("test.txt")
    wp.enumerate_rest_api()
    wp.enumerate_themes()
    wp.enumerate_users()

if __name__ == "__main__":
    main()

