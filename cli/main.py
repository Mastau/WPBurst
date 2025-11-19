from core.enumeration import WPEnumerator
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="Wordpress URL : http://example.org")
    args = parser.parse_args()

    wp = WPEnumerator(args.url)

    print("[*] Lancement de l'énumération…")
    wp.detect_wordpress()
    wp.get_version()
    wp.enumerate_plugins()
    wp.enumerate_themes()
    wp.enumerate_users()

if __name__ == "__main__":
    main()

